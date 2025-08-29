#!/usr/bin/env python3
"""
Generate ground truth 2D map from SDF world file for ORB-SLAM3 evaluation.
This script extracts tree positions and creates a top-down view map.
"""

import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
import argparse
import os

def parse_sdf_world(sdf_file):
    """Parse SDF world file and extract tree positions."""
    tree = ET.parse(sdf_file)
    root = tree.getroot()

    # Define namespace
    ns = {'sdf': 'http://schemas.ignitionrobotics.org/sdf/1.9'}

    trees = []

    # Find all include elements (try without namespace first)
    includes = root.findall('.//include')

    # Also try with namespace
    includes_ns = root.findall('.//sdf:include', ns)

    # Use the one that works
    includes_to_process = includes if includes else includes_ns

    for include in includes_to_process:
        uri_elem = include.find('uri')
        name_elem = include.find('name')
        pose_elem = include.find('pose')

        if uri_elem is not None and name_elem is not None and pose_elem is not None:
            uri = uri_elem.text
            name = name_elem.text
            pose = pose_elem.text

            # Check if it's a tree model (look for "Tree" in the URI)
            if 'Tree' in uri:
                # Parse pose (x y z roll pitch yaw)
                pose_values = [float(x) for x in pose.split()]
                x, y = pose_values[0], pose_values[1]

                # Determine tree type from URI
                tree_type = 'unknown'
                if 'Oak' in uri:
                    tree_type = 'oak'
                elif 'Pine' in uri:
                    tree_type = 'pine'

                trees.append({
                    'name': name,
                    'x': x,
                    'y': y,
                    'type': tree_type,
                    'uri': uri
                })

    return trees

def generate_ground_truth_map(trees, output_dir='.', map_size=100, resolution=0.5):
    """Generate ground truth 2D map from tree positions."""

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 12))

    # Set up the map area
    half_size = map_size / 2
    ax.set_xlim(-half_size, half_size)
    ax.set_ylim(-half_size, half_size)
    ax.set_aspect('equal')

    # Draw grass background
    grass_patch = patches.Rectangle((-half_size, -half_size), map_size, map_size,
                                   facecolor='lightgreen', alpha=0.3, edgecolor='none')
    ax.add_patch(grass_patch)

    # Draw trees
    oak_trees = []
    pine_trees = []

    for tree in trees:
        x, y = tree['x'], tree['y']
        tree_type = tree['type']

        if tree_type == 'oak':
            # Oak trees: larger, darker green circles
            circle = plt.Circle((x, y), 2.5, color='darkgreen', alpha=0.8, edgecolor='black', linewidth=1)
            ax.add_patch(circle)
            oak_trees.append((x, y))
        elif tree_type == 'pine':
            # Pine trees: smaller, lighter green triangles
            triangle = plt.Polygon([[x, y+2], [x-1.5, y-1], [x+1.5, y-1]],
                                  color='forestgreen', alpha=0.8, edgecolor='black', linewidth=1)
            ax.add_patch(triangle)
            pine_trees.append((x, y))

    # Add legend
    oak_legend = plt.Circle((0, 0), 0, color='darkgreen', alpha=0.8, edgecolor='black', linewidth=1)
    pine_legend = plt.Polygon([[0, 0], [0, 0], [0, 0]], color='forestgreen', alpha=0.8, edgecolor='black', linewidth=1)

    ax.legend([oak_legend, pine_legend],
              [f'Oak Trees ({len(oak_trees)})', f'Pine Trees ({len(pine_trees)})'],
              loc='upper right')

    # Add grid
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_title('Ground Truth Forest Map - Top Down View')

    # Add scale indicator
    scale_length = 10  # 10 meters
    ax.plot([-half_size+5, -half_size+5+scale_length], [-half_size+5, -half_size+5], 'k-', linewidth=3)
    ax.text(-half_size+5+scale_length/2, -half_size+3, f'{scale_length}m',
            ha='center', va='top', fontsize=10, weight='bold')

    # Save the map
    map_file = os.path.join(output_dir, 'ground_truth_forest_map.png')
    plt.savefig(map_file, dpi=300, bbox_inches='tight')
    print(f"Ground truth map saved to: {map_file}")

    # Save tree positions as CSV for further analysis
    csv_file = os.path.join(output_dir, 'tree_positions.csv')
    with open(csv_file, 'w') as f:
        f.write("name,x,y,type\n")
        for tree in trees:
            f.write(f"{tree['name']},{tree['x']},{tree['y']},{tree['type']}\n")
    print(f"Tree positions saved to: {csv_file}")

    # Save as numpy array for programmatic use
    np_file = os.path.join(output_dir, 'tree_positions.npy')
    tree_array = np.array([[tree['x'], tree['y']] for tree in trees])
    np.save(np_file, tree_array)
    print(f"Tree positions saved to: {np_file}")

    plt.show()

    return trees

def create_satellite_style_map(trees, output_dir='.', map_size=100):
    """Create a satellite-style map with more realistic appearance."""

    fig, ax = plt.subplots(figsize=(12, 12))

    half_size = map_size / 2
    ax.set_xlim(-half_size, half_size)
    ax.set_ylim(-half_size, half_size)
    ax.set_aspect('equal')

    # Create satellite-style background
    # Generate some texture for the ground
    x = np.linspace(-half_size, half_size, 200)
    y = np.linspace(-half_size, half_size, 200)
    X, Y = np.meshgrid(x, y)

    # Add some noise to simulate ground texture
    ground_texture = np.random.normal(0, 0.1, X.shape)
    ground_color = 0.6 + 0.2 * ground_texture  # Light green base

    # Create colormap for ground
    colors = ['#8FBC8F', '#90EE90', '#98FB98']  # Different shades of green
    ground_cmap = ListedColormap(colors)

    ax.contourf(X, Y, ground_color, levels=20, cmap=ground_cmap, alpha=0.7)

    # Draw trees with shadows
    for tree in trees:
        x, y = tree['x'], tree['y']
        tree_type = tree['type']

        # Draw shadow first
        shadow = plt.Circle((x+0.5, y-0.5), 2, color='black', alpha=0.3)
        ax.add_patch(shadow)

        if tree_type == 'oak':
            # Oak tree with more detail
            trunk = plt.Rectangle((x-0.3, y-1), 0.6, 2, color='brown', alpha=0.8)
            ax.add_patch(trunk)

            # Multiple circles for foliage
            for i in range(3):
                radius = 2.5 - i * 0.5
                alpha = 0.8 - i * 0.2
                foliage = plt.Circle((x, y+1), radius, color='darkgreen', alpha=alpha, edgecolor='black', linewidth=0.5)
                ax.add_patch(foliage)
        elif tree_type == 'pine':
            # Pine tree with triangular shape
            trunk = plt.Rectangle((x-0.2, y-1), 0.4, 1.5, color='brown', alpha=0.8)
            ax.add_patch(trunk)

            # Triangular foliage
            for i in range(3):
                height = 3 - i * 0.8
                width = 2 - i * 0.4
                y_offset = 1 + i * 0.5
                triangle = plt.Polygon([[x, y+y_offset+height],
                                       [x-width, y+y_offset],
                                       [x+width, y+y_offset]],
                                      color='forestgreen', alpha=0.8-i*0.2,
                                      edgecolor='black', linewidth=0.5)
                ax.add_patch(triangle)

    ax.grid(True, alpha=0.2)
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_title('Satellite-Style Ground Truth Forest Map')

    # Save satellite-style map
    satellite_file = os.path.join(output_dir, 'satellite_style_forest_map.png')
    plt.savefig(satellite_file, dpi=300, bbox_inches='tight')
    print(f"Satellite-style map saved to: {satellite_file}")

    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Generate ground truth 2D map from SDF world file')
    parser.add_argument('sdf_file', help='Path to SDF world file')
    parser.add_argument('--output-dir', default='.', help='Output directory for generated files')
    parser.add_argument('--map-size', type=float, default=100, help='Map size in meters')
    parser.add_argument('--satellite-style', action='store_true', help='Generate satellite-style map')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Parse SDF file
    print(f"Parsing SDF file: {args.sdf_file}")
    trees = parse_sdf_world(args.sdf_file)
    print(f"Found {len(trees)} trees")

    # Generate ground truth map
    trees = generate_ground_truth_map(trees, args.output_dir, args.map_size)

    # Generate satellite-style map if requested
    if args.satellite_style:
        create_satellite_style_map(trees, args.output_dir, args.map_size)

    # Print summary
    oak_count = sum(1 for tree in trees if tree['type'] == 'oak')
    pine_count = sum(1 for tree in trees if tree['type'] == 'pine')
    print(f"\nSummary:")
    print(f"Total trees: {len(trees)}")
    print(f"Oak trees: {oak_count}")
    print(f"Pine trees: {pine_count}")

    # Calculate tree density
    area = args.map_size * args.map_size
    density = len(trees) / area
    print(f"Tree density: {density:.3f} trees/m²")

if __name__ == "__main__":
    main()
