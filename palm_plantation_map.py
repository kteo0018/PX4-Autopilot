#!/usr/bin/env python3
"""
2D Map Generator for Palm Plantation World
Creates a visual representation of the SDF world file with grid, coordinates, and annotations.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

def create_palm_plantation_map():
    # Set up the figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))

    # Define the coordinate ranges based on the SDF file
    x_min, x_max = 0, 40
    y_min, y_max = -40, 0

    # Set axis limits and labels
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('X Coordinate (meters)', fontsize=12)
    ax.set_ylabel('Y Coordinate (meters)', fontsize=12)
    ax.set_title('Palm Plantation World Map', fontsize=16, fontweight='bold')

    # Create grid
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_xticks(range(x_min, x_max + 1, 2))
    ax.set_yticks(range(y_min, y_max + 1, 2))

    # Invert Y axis to match the coordinate system (negative Y values)
    ax.invert_yaxis()

    # Define grass patch data (from SDF file)
    grass_patches = [
        {'name': 'grasspatch_center', 'pos': (20, -20)},
        {'name': 'grasspatch_top_middle', 'pos': (35, -20)},
        {'name': 'grasspatch_middle_right', 'pos': (20, -35)},
        {'name': 'grasspatch_top_right', 'pos': (35, -35)},
        {'name': 'grasspatch_bottom_middle', 'pos': (5, -20)},
        {'name': 'grasspatch_middle_left', 'pos': (20, -5)},
        {'name': 'grasspatch_bottom_left', 'pos': (5, -5)},
        {'name': 'grasspatch_bottom_right', 'pos': (5, -35)},
        {'name': 'grasspatch_top_left', 'pos': (35, -5)}
    ]

    # Draw grass patches as green rectangles
    for grass in grass_patches:
        x, y = grass['pos']
        # Create a rectangle for each grass patch (approximate size)
        rect = Rectangle((x-7.5, y-7.5), 15, 15,
                        facecolor='lightgreen',
                        edgecolor='darkgreen',
                        alpha=0.6,
                        linewidth=1)
        ax.add_patch(rect)

        # Add grass patch name as semi-transparent text
        ax.text(x, y, grass['name'],
                ha='center', va='center',
                fontsize=8, alpha=0.7,
                color='darkgreen', fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

    # Define palm tree data (from SDF file)
    palm_trees = []

    # Row 1: Bottom row (Y = -8)
    for i in range(1, 8):
        x = 4 + i * 4  # 8, 12, 16, 20, 24, 28, 32
        y = -8
        palm_trees.append({'name': f'palm_tree_1_{i}', 'pos': (x, y), 'row': 1, 'col': i})

    # Row 2: Second row (Y = -12)
    for i in range(1, 8):
        x = 4 + i * 4
        y = -12
        palm_trees.append({'name': f'palm_tree_2_{i}', 'pos': (x, y), 'row': 2, 'col': i})

    # Row 3: Third row (Y = -16)
    for i in range(1, 8):
        x = 4 + i * 4
        y = -16
        palm_trees.append({'name': f'palm_tree_3_{i}', 'pos': (x, y), 'row': 3, 'col': i})

    # Row 4: Fourth row (Y = -20)
    for i in range(1, 8):
        x = 4 + i * 4
        y = -20
        palm_trees.append({'name': f'palm_tree_4_{i}', 'pos': (x, y), 'row': 4, 'col': i})

    # Row 5: Fifth row (Y = -24)
    for i in range(1, 8):
        x = 4 + i * 4
        y = -24
        palm_trees.append({'name': f'palm_tree_5_{i}', 'pos': (x, y), 'row': 5, 'col': i})

    # Row 6: Sixth row (Y = -28)
    for i in range(1, 8):
        x = 4 + i * 4
        y = -28
        palm_trees.append({'name': f'palm_tree_6_{i}', 'pos': (x, y), 'row': 6, 'col': i})

    # Row 7: Seventh row (Y = -32)
    for i in range(1, 8):
        x = 4 + i * 4
        y = -32
        palm_trees.append({'name': f'palm_tree_7_{i}', 'pos': (x, y), 'row': 7, 'col': i})

    # Draw palm trees
    for palm in palm_trees:
        x, y = palm['pos']

        # Draw palm tree as a circle
        circle = plt.Circle((x, y), 1.5,
                           facecolor='brown',
                           edgecolor='darkgreen',
                           linewidth=2,
                           alpha=0.8)
        ax.add_patch(circle)

        # Add palm tree number annotation
        ax.text(x, y, f"{palm['row']}.{palm['col']}",
                ha='center', va='center',
                fontsize=7, fontweight='bold',
                color='white')

        # Add palm tree name as small text below
        ax.text(x, y+1.5, palm['name'],
                ha='center', va='top',
                fontsize=6, alpha=0.8,
                color='darkblue')

    # Add coordinate annotations at corners
    ax.text(x_min + 1, y_min + 1, f'({x_min}, {y_min})',
            fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))
    ax.text(x_max - 3, y_min + 1, f'({x_max}, {y_min})',
            fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))
    ax.text(x_min + 1, y_max - 1, f'({x_min}, {y_max})',
            fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))
    ax.text(x_max - 3, y_max - 1, f'({x_max}, {y_max})',
            fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))

    # Add legend
    grass_patch = mpatches.Patch(color='lightgreen', alpha=0.6, label='Grass Patches')
    palm_tree = mpatches.Patch(color='brown', alpha=0.8, label='Palm Trees')
    ax.legend(handles=[grass_patch, palm_tree], loc='upper center')

    # Add scale indicator
    ax.text(x_max - 5, y_min + 2, 'Scale: 1 unit = 1 meter',
            fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.8))

    # Set equal aspect ratio
    ax.set_aspect('equal')

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('/home/ken/PX4-Autopilot/palm_plantation_map.png',
                dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')

    print("Map saved as 'palm_plantation_map.png'")
    print(f"Total palm trees: {len(palm_trees)}")
    print(f"Total grass patches: {len(grass_patches)}")

    # Show the plot
    plt.show()

if __name__ == "__main__":
    create_palm_plantation_map()
