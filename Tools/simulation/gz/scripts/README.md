# Ground Truth Map Generation and SLAM Evaluation Tools

This directory contains tools for generating ground truth 2D maps from SDF world files and evaluating ORB-SLAM3 results against these ground truth maps.

## Overview

These tools are designed to help you:
1. **Generate ground truth maps** from your SDF world files for benchmarking
2. **Evaluate ORB-SLAM3 performance** by comparing SLAM results with known ground truth
3. **Visualize comparisons** between ground truth and SLAM-generated maps

## Files

- `generate_ground_truth_map.py` - Main script to extract tree positions and generate ground truth maps
- `compare_slam_results.py` - Script to compare ORB-SLAM3 results with ground truth
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Generate Ground Truth Map

Generate a ground truth map from your SDF world file:

```bash
python generate_ground_truth_map.py path/to/your/world.sdf --output-dir ./output
```

**Options:**
- `--output-dir`: Directory to save generated files (default: current directory)
- `--map-size`: Size of the map in meters (default: 100)
- `--satellite-style`: Generate an additional satellite-style map

**Output files:**
- `ground_truth_forest_map.png` - Top-down view map
- `satellite_style_forest_map.png` - Satellite-style map (if requested)
- `tree_positions.csv` - Tree positions in CSV format
- `tree_positions.npy` - Tree positions in numpy format

### 2. Compare SLAM Results

Compare ORB-SLAM3 results with ground truth:

```bash
python compare_slam_results.py ground_truth.csv slam_results.csv --output-dir ./evaluation
```

**Options:**
- `--output-dir`: Directory to save evaluation results (default: current directory)
- `--max-distance`: Maximum distance for matching landmarks (default: 5.0 meters)
- `--no-plot`: Skip generating comparison plots

**Input formats:**
- Ground truth: CSV with columns `name,x,y,type` or numpy array
- SLAM results: CSV with columns `x,y,confidence` or numpy array

**Output files:**
- `evaluation_metrics.txt` - Detailed evaluation metrics
- `slam_comparison.png` - Visualization of comparison

## Example Workflow

1. **Generate ground truth from your world:**
```bash
python generate_ground_truth_map.py Tools/simulation/gz/worlds/z_my_forest.sdf --output-dir ./ground_truth
```

2. **Run ORB-SLAM3** on your simulation and save landmark positions

3. **Compare results:**
```bash
python compare_slam_results.py ./ground_truth/tree_positions.csv ./slam_landmarks.csv --output-dir ./evaluation
```

## Evaluation Metrics

The comparison script calculates several metrics:

- **Precision**: Percentage of SLAM landmarks that match ground truth
- **Recall**: Percentage of ground truth trees detected by SLAM
- **F1-Score**: Harmonic mean of precision and recall
- **Mean Distance**: Average distance between matched pairs
- **Matched Pairs**: Number of successfully matched landmarks
- **False Positives**: SLAM landmarks not matching ground truth
- **False Negatives**: Ground truth trees not detected by SLAM

## File Formats

### Ground Truth CSV Format
```csv
name,x,y,type
oak_tree_1,30,10,oak
pine_tree_1,8,8,pine
```

### SLAM Results CSV Format
```csv
x,y,confidence
29.5,10.2,0.95
8.1,7.9,0.87
```

### Numpy Array Format
2D array with shape (N, 2) where each row is [x, y] coordinates.

## Tips for ORB-SLAM3 Integration

1. **Extract landmarks**: Save ORB-SLAM3 landmark positions in the same coordinate system as your ground truth
2. **Coordinate alignment**: Ensure both ground truth and SLAM results use the same coordinate frame
3. **Confidence scores**: Include confidence scores for SLAM landmarks if available
4. **Filtering**: Consider filtering low-confidence landmarks before comparison

## Visualization

The tools generate several types of visualizations:

1. **Ground Truth Map**: Clean top-down view showing tree positions and types
2. **Satellite-Style Map**: More realistic appearance with shadows and texture
3. **Comparison Plot**: Side-by-side comparison with matching lines and metrics

## Troubleshooting

- **No trees found**: Check that your SDF file contains tree models with "Tree" in the URI
- **Coordinate mismatch**: Ensure both files use the same coordinate system
- **Poor matching**: Adjust the `--max-distance` parameter based on your SLAM accuracy
- **Missing dependencies**: Install required packages with `pip install -r requirements.txt`

## Example Output

The ground truth map will show:
- Oak trees as dark green circles
- Pine trees as forest green triangles
- Grid lines and scale indicators
- Legend with tree counts

The comparison visualization will show:
- Ground truth trees (grayed out)
- SLAM landmarks (colored by confidence)
- Matching lines between corresponding points
- Evaluation metrics overlay
