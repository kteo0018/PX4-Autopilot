#!/usr/bin/env python3
"""
Compare ORB-SLAM3 results with ground truth map for evaluation.
This script helps evaluate the accuracy of SLAM mapping against known ground truth.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
import argparse
import os
import csv
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment

def load_ground_truth(ground_truth_file):
    """Load ground truth tree positions from CSV or numpy file."""
    if ground_truth_file.endswith('.csv'):
        trees = []
        with open(ground_truth_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                trees.append({
                    'x': float(row['x']),
                    'y': float(row['y']),
                    'type': row['type']
                })
        return trees
    elif ground_truth_file.endswith('.npy'):
        positions = np.load(ground_truth_file)
        trees = []
        for pos in positions:
            trees.append({
                'x': pos[0],
                'y': pos[1],
                'type': 'unknown'  # Type not available in numpy format
            })
        return trees
    else:
        raise ValueError("Ground truth file must be .csv or .npy format")

def load_slam_results(slam_file):
    """Load ORB-SLAM3 results from CSV or numpy file."""
    if slam_file.endswith('.csv'):
        landmarks = []
        with open(slam_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                landmarks.append({
                    'x': float(row['x']),
                    'y': float(row['y']),
                    'confidence': float(row.get('confidence', 1.0))
                })
        return landmarks
    elif slam_file.endswith('.npy'):
        positions = np.load(slam_file)
        landmarks = []
        for pos in positions:
            landmarks.append({
                'x': pos[0],
                'y': pos[1],
                'confidence': 1.0
            })
        return landmarks
    else:
        raise ValueError("SLAM results file must be .csv or .npy format")

def calculate_metrics(ground_truth, slam_results, max_distance=5.0):
    """Calculate evaluation metrics between ground truth and SLAM results."""

    if not ground_truth or not slam_results:
        return {
            'precision': 0.0,
            'recall': 0.0,
            'f1_score': 0.0,
            'mean_distance': float('inf'),
            'matched_pairs': 0,
            'false_positives': len(slam_results),
            'false_negatives': len(ground_truth)
        }

    # Extract positions
    gt_positions = np.array([[tree['x'], tree['y']] for tree in ground_truth])
    slam_positions = np.array([[landmark['x'], landmark['y']] for landmark in slam_results])

    # Calculate distance matrix
    distances = cdist(gt_positions, slam_positions)

    # Use Hungarian algorithm to find optimal matching
    gt_indices, slam_indices = linear_sum_assignment(distances)

    # Filter matches within max_distance
    valid_matches = []
    matched_gt = set()
    matched_slam = set()

    for gt_idx, slam_idx in zip(gt_indices, slam_indices):
        if distances[gt_idx, slam_idx] <= max_distance:
            valid_matches.append((gt_idx, slam_idx, distances[gt_idx, slam_idx]))
            matched_gt.add(gt_idx)
            matched_slam.add(slam_idx)

    # Calculate metrics
    true_positives = len(valid_matches)
    false_positives = len(slam_results) - len(matched_slam)
    false_negatives = len(ground_truth) - len(matched_gt)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    mean_distance = np.mean([match[2] for match in valid_matches]) if valid_matches else float('inf')

    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'mean_distance': mean_distance,
        'matched_pairs': len(valid_matches),
        'false_positives': false_positives,
        'false_negatives': false_negatives,
        'valid_matches': valid_matches,
        'matched_gt': matched_gt,
        'matched_slam': matched_slam
    }

def visualize_comparison(ground_truth, slam_results, metrics, output_file=None):
    """Visualize the comparison between ground truth and SLAM results."""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    # Determine plot limits
    all_x = [tree['x'] for tree in ground_truth] + [landmark['x'] for landmark in slam_results]
    all_y = [tree['y'] for tree in ground_truth] + [landmark['y'] for landmark in slam_results]

    x_min, x_max = min(all_x) - 5, max(all_x) + 5
    y_min, y_max = min(all_y) - 5, max(all_y) + 5

    # Plot 1: Ground Truth
    ax1.set_xlim(x_min, x_max)
    ax1.set_ylim(y_min, y_max)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.set_title('Ground Truth')
    ax1.set_xlabel('X (meters)')
    ax1.set_ylabel('Y (meters)')

    # Draw ground truth trees
    for tree in ground_truth:
        x, y = tree['x'], tree['y']
        tree_type = tree['type']

        if tree_type == 'oak':
            circle = plt.Circle((x, y), 2, color='darkgreen', alpha=0.8, edgecolor='black', linewidth=1)
            ax1.add_patch(circle)
        elif tree_type == 'pine':
            triangle = plt.Polygon([[x, y+1.5], [x-1, y-0.5], [x+1, y-0.5]],
                                  color='forestgreen', alpha=0.8, edgecolor='black', linewidth=1)
            ax1.add_patch(triangle)
        else:
            circle = plt.Circle((x, y), 1.5, color='gray', alpha=0.8, edgecolor='black', linewidth=1)
            ax1.add_patch(circle)

    # Plot 2: SLAM Results vs Ground Truth
    ax2.set_xlim(x_min, x_max)
    ax2.set_ylim(y_min, y_max)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    ax2.set_title('SLAM Results vs Ground Truth')
    ax2.set_xlabel('X (meters)')
    ax2.set_ylabel('Y (meters)')

    # Draw ground truth trees (grayed out)
    for tree in ground_truth:
        x, y = tree['x'], tree['y']
        circle = plt.Circle((x, y), 1.5, color='lightgray', alpha=0.5, edgecolor='gray', linewidth=1)
        ax2.add_patch(circle)

    # Draw SLAM landmarks
    for i, landmark in enumerate(slam_results):
        x, y = landmark['x'], landmark['y']
        confidence = landmark['confidence']

        # Color based on confidence
        if confidence > 0.8:
            color = 'red'
        elif confidence > 0.5:
            color = 'orange'
        else:
            color = 'yellow'

        circle = plt.Circle((x, y), 1, color=color, alpha=0.8, edgecolor='black', linewidth=1)
        ax2.add_patch(circle)

    # Draw matching lines
    if 'valid_matches' in metrics:
        for gt_idx, slam_idx, distance in metrics['valid_matches']:
            gt_pos = (ground_truth[gt_idx]['x'], ground_truth[gt_idx]['y'])
            slam_pos = (slam_results[slam_idx]['x'], slam_results[slam_idx]['y'])
            ax2.plot([gt_pos[0], slam_pos[0]], [gt_pos[1], slam_pos[1]], 'g-', alpha=0.6, linewidth=1)

    # Add legend
    legend_elements = [
        plt.Circle((0, 0), 0, color='lightgray', alpha=0.5, edgecolor='gray', linewidth=1, label='Ground Truth'),
        plt.Circle((0, 0), 0, color='red', alpha=0.8, edgecolor='black', linewidth=1, label='SLAM (High Conf)'),
        plt.Circle((0, 0), 0, color='orange', alpha=0.8, edgecolor='black', linewidth=1, label='SLAM (Med Conf)'),
        plt.Circle((0, 0), 0, color='yellow', alpha=0.8, edgecolor='black', linewidth=1, label='SLAM (Low Conf)'),
        plt.Line2D([0], [0], color='green', alpha=0.6, linewidth=1, label='Matches')
    ]
    ax2.legend(handles=legend_elements, loc='upper right')

    # Add metrics text
    metrics_text = f"""Metrics:
Precision: {metrics['precision']:.3f}
Recall: {metrics['recall']:.3f}
F1-Score: {metrics['f1_score']:.3f}
Mean Distance: {metrics['mean_distance']:.2f}m
Matched Pairs: {metrics['matched_pairs']}
False Positives: {metrics['false_positives']}
False Negatives: {metrics['false_negatives']}"""

    ax2.text(0.02, 0.98, metrics_text, transform=ax2.transAxes,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Comparison visualization saved to: {output_file}")

    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Compare ORB-SLAM3 results with ground truth')
    parser.add_argument('ground_truth', help='Path to ground truth file (.csv or .npy)')
    parser.add_argument('slam_results', help='Path to SLAM results file (.csv or .npy)')
    parser.add_argument('--output-dir', default='.', help='Output directory for results')
    parser.add_argument('--max-distance', type=float, default=5.0, help='Maximum distance for matching (meters)')
    parser.add_argument('--no-plot', action='store_true', help='Skip plotting')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Load data
    print(f"Loading ground truth from: {args.ground_truth}")
    ground_truth = load_ground_truth(args.ground_truth)
    print(f"Loaded {len(ground_truth)} ground truth trees")

    print(f"Loading SLAM results from: {args.slam_results}")
    slam_results = load_slam_results(args.slam_results)
    print(f"Loaded {len(slam_results)} SLAM landmarks")

    # Calculate metrics
    print(f"Calculating metrics with max distance: {args.max_distance}m")
    metrics = calculate_metrics(ground_truth, slam_results, args.max_distance)

    # Print results
    print("\n" + "="*50)
    print("EVALUATION RESULTS")
    print("="*50)
    print(f"Precision: {metrics['precision']:.3f}")
    print(f"Recall: {metrics['recall']:.3f}")
    print(f"F1-Score: {metrics['f1_score']:.3f}")
    print(f"Mean Distance: {metrics['mean_distance']:.2f}m")
    print(f"Matched Pairs: {metrics['matched_pairs']}")
    print(f"False Positives: {metrics['false_positives']}")
    print(f"False Negatives: {metrics['false_negatives']}")
    print("="*50)

    # Save metrics to file
    metrics_file = os.path.join(args.output_dir, 'evaluation_metrics.txt')
    with open(metrics_file, 'w') as f:
        f.write("ORB-SLAM3 Evaluation Metrics\n")
        f.write("="*30 + "\n")
        f.write(f"Ground Truth Trees: {len(ground_truth)}\n")
        f.write(f"SLAM Landmarks: {len(slam_results)}\n")
        f.write(f"Max Distance Threshold: {args.max_distance}m\n\n")
        f.write(f"Precision: {metrics['precision']:.3f}\n")
        f.write(f"Recall: {metrics['recall']:.3f}\n")
        f.write(f"F1-Score: {metrics['f1_score']:.3f}\n")
        f.write(f"Mean Distance: {metrics['mean_distance']:.2f}m\n")
        f.write(f"Matched Pairs: {metrics['matched_pairs']}\n")
        f.write(f"False Positives: {metrics['false_positives']}\n")
        f.write(f"False Negatives: {metrics['false_negatives']}\n")

    print(f"Metrics saved to: {metrics_file}")

    # Visualize comparison
    if not args.no_plot:
        comparison_file = os.path.join(args.output_dir, 'slam_comparison.png')
        visualize_comparison(ground_truth, slam_results, metrics, comparison_file)

if __name__ == "__main__":
    main()
