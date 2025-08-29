# ORB-SLAM3 Forest Mapping Evaluation Guide

This guide explains how to use the ground truth evaluation tools to assess ORB-SLAM3 performance in forest mapping scenarios.

## Overview

The tools provided here enable you to:
1. **Generate ground truth maps** from SDF world files
2. **Evaluate ORB-SLAM3 accuracy** by comparing SLAM results with known ground truth
3. **Visualize and quantify** mapping performance

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Ground Truth
```bash
python3 generate_ground_truth_map.py ../worlds/z_my_forest.sdf --output-dir ./ground_truth
```

### 3. Run ORB-SLAM3
Execute your ORB-SLAM3 system and save landmark positions in CSV format:
```csv
x,y,confidence
29.5,10.2,0.95
30.1,-9.8,0.92
...
```

### 4. Compare Results
```bash
python3 compare_slam_results.py ./ground_truth/tree_positions.csv ./slam_results.csv --output-dir ./evaluation
```

## Detailed Workflow

### Step 1: Ground Truth Generation

The `generate_ground_truth_map.py` script:
- Parses your SDF world file
- Extracts tree positions and types
- Generates visual maps (top-down and satellite-style)
- Saves data in multiple formats (CSV, numpy)

**Output files:**
- `ground_truth_forest_map.png` - Clean top-down view
- `satellite_style_forest_map.png` - Realistic satellite view
- `tree_positions.csv` - Tree coordinates and types
- `tree_positions.npy` - Numpy array for programmatic use

### Step 2: ORB-SLAM3 Integration

To integrate with ORB-SLAM3, you need to:

1. **Extract landmark positions** from ORB-SLAM3 output
2. **Save in the expected format** (CSV with x, y, confidence columns)
3. **Ensure coordinate alignment** with ground truth

**Example ORB-SLAM3 output format:**
```csv
x,y,confidence
29.5,10.2,0.95
30.1,-9.8,0.92
-29.8,10.1,0.88
```

### Step 3: Evaluation

The `compare_slam_results.py` script calculates:

- **Precision**: Percentage of SLAM landmarks matching ground truth
- **Recall**: Percentage of ground truth trees detected
- **F1-Score**: Harmonic mean of precision and recall
- **Mean Distance**: Average error in matched pairs
- **Matched Pairs**: Number of successful matches
- **False Positives/Negatives**: Detection errors

## Evaluation Metrics Explained

### Precision
```
Precision = True Positives / (True Positives + False Positives)
```
- Measures how many SLAM landmarks are correct
- High precision = few false detections

### Recall
```
Recall = True Positives / (True Positives + False Negatives)
```
- Measures how many ground truth trees were detected
- High recall = few missed trees

### F1-Score
```
F1-Score = 2 * (Precision * Recall) / (Precision + Recall)
```
- Balanced measure of overall performance
- Range: 0.0 (poor) to 1.0 (perfect)

### Mean Distance
- Average Euclidean distance between matched pairs
- Lower values indicate better accuracy
- Units: meters

## Best Practices

### 1. Coordinate System Alignment
- Ensure both ground truth and SLAM results use the same coordinate frame
- Common issues: different origins, axis orientations, or units

### 2. Distance Threshold
- Adjust `--max-distance` parameter based on your SLAM accuracy
- Typical values: 2-5 meters for forest environments
- Too small: misses valid matches
- Too large: includes false matches

### 3. Confidence Filtering
- Consider filtering low-confidence SLAM landmarks
- Use confidence scores to weight evaluation metrics
- Balance between completeness and accuracy

### 4. Tree Type Considerations
- Ground truth includes tree types (oak/pine)
- SLAM typically doesn't distinguish tree types
- Focus on positional accuracy for evaluation

## Example Results Interpretation

```
Precision: 0.950
Recall: 0.750
F1-Score: 0.840
Mean Distance: 1.2m
Matched Pairs: 36
False Positives: 2
False Negatives: 12
```

**Interpretation:**
- **Good precision**: Most detected landmarks are correct
- **Moderate recall**: Some trees were missed
- **Good F1-score**: Overall balanced performance
- **Reasonable accuracy**: 1.2m average error
- **36/48 trees detected**: 75% detection rate

## Troubleshooting

### Common Issues

1. **No trees found in SDF file**
   - Check that tree models have "Tree" in the URI
   - Verify XML structure and namespaces

2. **Poor matching results**
   - Check coordinate system alignment
   - Adjust max_distance parameter
   - Verify data formats

3. **Missing dependencies**
   - Install required packages: `pip install -r requirements.txt`
   - Check Python version compatibility

4. **Visualization issues**
   - Ensure matplotlib backend is properly configured
   - Check file permissions for output directories

### Performance Optimization

1. **Large datasets**: Use numpy arrays instead of CSV for better performance
2. **Batch processing**: Process multiple SLAM runs in sequence
3. **Memory usage**: Consider processing in chunks for very large maps

## Integration with ROS

If using ROS with ORB-SLAM3:

1. **Subscribe to landmark topics**:
```python
import rospy
from geometry_msgs.msg import PointStamped

def landmark_callback(msg):
    # Extract and save landmark data
    x, y = msg.point.x, msg.point.y
    # Save to CSV or process directly
```

2. **Use ROS bags** for offline processing:
```bash
rosbag record /orb_slam3/landmarks
```

3. **Convert to evaluation format**:
```python
# Extract landmarks from ROS bag
# Convert to CSV format
# Run evaluation
```

## Advanced Usage

### Custom Evaluation Metrics

You can extend the evaluation by:
- Adding custom distance metrics
- Implementing tree type classification evaluation
- Creating time-based analysis for SLAM convergence

### Batch Evaluation

For multiple experiments:
```bash
for slam_file in slam_results_*.csv; do
    python3 compare_slam_results.py ground_truth.csv "$slam_file" --output-dir "./eval_${slam_file%.*}"
done
```

### Statistical Analysis

Use the generated metrics for:
- Performance comparison across different SLAM parameters
- Statistical significance testing
- Trend analysis over multiple runs

## Conclusion

This evaluation framework provides a comprehensive way to assess ORB-SLAM3 performance in forest environments. The ground truth maps serve as reliable benchmarks, while the evaluation metrics give quantitative insights into SLAM accuracy and completeness.

For best results:
- Use consistent coordinate systems
- Adjust parameters based on your specific environment
- Consider multiple evaluation runs for statistical significance
- Combine quantitative metrics with qualitative visual analysis
