#!/usr/bin/env python3
"""
Example integration script showing how to use the ground truth evaluation tools
with ORB-SLAM3 for forest mapping evaluation.
"""

import numpy as np
import csv
import os
from generate_ground_truth_map import parse_sdf_world, generate_ground_truth_map
from compare_slam_results import calculate_metrics, visualize_comparison

def extract_orb_slam3_landmarks(slam_output_file):
    """
    Example function to extract landmarks from ORB-SLAM3 output.

    This is a placeholder - you'll need to adapt this based on how ORB-SLAM3
    outputs its results (e.g., from a ROS topic, log file, etc.)
    """
    landmarks = []

    # Example: Reading from a CSV file that ORB-SLAM3 might generate
    if os.path.exists(slam_output_file):
        with open(slam_output_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                landmarks.append({
                    'x': float(row['x']),
                    'y': float(row['y']),
                    'confidence': float(row.get('confidence', 1.0))
                })

    return landmarks

def save_orb_slam3_results(landmarks, output_file):
    """
    Save ORB-SLAM3 landmarks in the expected format for comparison.
    """
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['x', 'y', 'confidence'])
        for landmark in landmarks:
            writer.writerow([landmark['x'], landmark['y'], landmark['confidence']])

def run_complete_evaluation(sdf_world_file, slam_results_file, output_dir='./evaluation'):
    """
    Run complete evaluation pipeline:
    1. Generate ground truth from SDF world
    2. Compare with ORB-SLAM3 results
    3. Generate evaluation report
    """

    print("=== ORB-SLAM3 Forest Mapping Evaluation ===")

    # Step 1: Generate ground truth from SDF world
    print("\n1. Generating ground truth from SDF world...")
    trees = parse_sdf_world(sdf_world_file)
    print(f"   Found {len(trees)} trees in the world")

    # Generate ground truth map
    generate_ground_truth_map(trees, output_dir)

    # Step 2: Load ORB-SLAM3 results
    print("\n2. Loading ORB-SLAM3 results...")
    slam_landmarks = extract_orb_slam3_landmarks(slam_results_file)
    print(f"   Found {len(slam_landmarks)} SLAM landmarks")

    # Step 3: Calculate evaluation metrics
    print("\n3. Calculating evaluation metrics...")
    metrics = calculate_metrics(trees, slam_landmarks, max_distance=5.0)

    # Step 4: Generate comparison visualization
    print("\n4. Generating comparison visualization...")
    comparison_file = os.path.join(output_dir, 'orb_slam3_comparison.png')
    visualize_comparison(trees, slam_landmarks, metrics, comparison_file)

    # Step 5: Print summary
    print("\n=== EVALUATION SUMMARY ===")
    print(f"Ground Truth Trees: {len(trees)}")
    print(f"SLAM Landmarks: {len(slam_landmarks)}")
    print(f"Precision: {metrics['precision']:.3f}")
    print(f"Recall: {metrics['recall']:.3f}")
    print(f"F1-Score: {metrics['f1_score']:.3f}")
    print(f"Mean Distance: {metrics['mean_distance']:.2f}m")
    print(f"Matched Pairs: {metrics['matched_pairs']}")
    print(f"False Positives: {metrics['false_positives']}")
    print(f"False Negatives: {metrics['false_negatives']}")

    return metrics

def example_orb_slam3_output_format():
    """
    Example of how ORB-SLAM3 might output landmark data.
    This shows the expected format for the comparison tools.
    """

    # Example: ORB-SLAM3 might output landmarks like this
    example_landmarks = [
        {'x': 29.5, 'y': 10.2, 'confidence': 0.95},
        {'x': 30.1, 'y': -9.8, 'confidence': 0.92},
        {'x': -29.8, 'y': 10.1, 'confidence': 0.88},
        # ... more landmarks
    ]

    # Save in the expected format
    save_orb_slam3_results(example_landmarks, 'example_orb_slam3_output.csv')
    print("Example ORB-SLAM3 output format saved to 'example_orb_slam3_output.csv'")

def main():
    """
    Main function demonstrating the complete evaluation workflow.
    """

    # Example usage
    print("ORB-SLAM3 Forest Mapping Evaluation Example")
    print("=" * 50)

    # Example 1: Show expected output format
    print("\n1. Example ORB-SLAM3 output format:")
    example_orb_slam3_output_format()

    # Example 2: Run evaluation with sample data
    print("\n2. Running evaluation with sample data:")

    # Use the sample data we created earlier
    sdf_file = "../worlds/z_my_forest.sdf"
    slam_file = "sample_slam_results.csv"

    if os.path.exists(sdf_file) and os.path.exists(slam_file):
        metrics = run_complete_evaluation(sdf_file, slam_file, "./complete_evaluation")
        print("\nEvaluation completed successfully!")
    else:
        print("Sample files not found. Please ensure the SDF world file and sample SLAM results exist.")

    print("\n" + "=" * 50)
    print("Integration Notes:")
    print("- Adapt extract_orb_slam3_landmarks() to your ORB-SLAM3 output format")
    print("- Ensure coordinate systems match between ground truth and SLAM results")
    print("- Consider filtering low-confidence landmarks before evaluation")
    print("- Adjust max_distance parameter based on your SLAM accuracy")

if __name__ == "__main__":
    main()
