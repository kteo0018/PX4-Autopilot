# x500_custom Drone Sensor Parameters
## Complete Sensor Configuration for SLAM Systems

This document contains all sensor parameters for the x500_custom drone, extracted from the PX4-Autopilot configuration files. Use these parameters when configuring ORB-SLAM 3, OpenVINS, or other SLAM systems.

---

## 📷 Camera Parameters

### Single Camera Configuration (x500_custom)
**File**: `Tools/simulation/gz/models/x500_custom/model.sdf`

#### Physical Configuration
- **Position**: `(0.12, 0, 0.05)` meters from drone center
- **Orientation**: Forward-facing
- **Mass**: 0.008 kg
- **Size**: 0.04 × 0.04 × 0.04 meters

#### Camera Specifications
- **Field of View**: 80° horizontal (1.39626 radians)
- **Resolution**: 640 × 480 pixels
- **Format**: R8G8B8 (RGB)
- **Frame Rate**: 30 Hz
- **Clip Range**: 0.1m to 100m

#### Noise Parameters
- **Type**: Gaussian
- **Mean**: 0.0
- **Standard Deviation**: 0.005

#### ROS Topic
```
world/z_my_forest/model/x500_custom_0/link/camera_link/sensor/camera/image
```

---

### Stereo Camera Configuration (x500_custom_stereo)
**File**: `Tools/simulation/gz/models/x500_stereo/model.sdf`

#### Left Camera
- **Position**: `(0.12, 0, 0.05)` meters
- **Same specifications as single camera**

#### Right Camera
- **Position**: `(0.12, 0.08, 0.05)` meters
- **Baseline**: 0.08 meters (8cm separation)
- **Same specifications as left camera**

#### Camera Intrinsics (Both Cameras)
```
fx = 320.0  (focal length x)
fy = 240.0  (focal length y)
cx = 320.0  (principal point x)
cy = 240.0  (principal point y)
s = 0.0     (skew)
```

#### Distortion Parameters
```
k1 = 0.0  (radial distortion)
k2 = 0.0
k3 = 0.0
p1 = 0.0  (tangential distortion)
p2 = 0.0
```

#### Lens Configuration
- **Type**: Stereographic
- **Scale to HFOV**: true
- **Cutoff Angle**: 1.570796 radians (90°)
- **Environment Texture Size**: 256

#### ROS Topics
```
Left:  world/z_my_forest/model/x500_custom_stereo_0/link/camera_left_link/sensor/camera_left/image
Right: world/z_my_forest/model/x500_custom_stereo_0/link/camera_right_link/sensor/camera_right/image
```

---

## 🧭 IMU Sensor Parameters

**File**: `Tools/simulation/gz/models/x500_custom/model.sdf`

### Physical Configuration
- **Position**: `(0, 0, 0.08)` meters (center of drone body)
- **Mass**: 0.005 kg
- **Size**: 0.025 × 0.025 × 0.025 meters
- **Update Rate**: 200 Hz

### Gyroscope (Angular Velocity) Parameters
**Noise Type**: Gaussian

#### X-axis
- **Mean**: 0.0 rad/s
- **Standard Deviation**: 0.0002 rad/s
- **Bias Mean**: 0.0000075 rad/s
- **Bias Standard Deviation**: 0.0000008 rad/s

#### Y-axis
- **Mean**: 0.0 rad/s
- **Standard Deviation**: 0.0002 rad/s
- **Bias Mean**: 0.0000075 rad/s
- **Bias Standard Deviation**: 0.0000008 rad/s

#### Z-axis
- **Mean**: 0.0 rad/s
- **Standard Deviation**: 0.0002 rad/s
- **Bias Mean**: 0.0000075 rad/s
- **Bias Standard Deviation**: 0.0000008 rad/s

### Accelerometer (Linear Acceleration) Parameters
**Noise Type**: Gaussian

#### X-axis
- **Mean**: 0.0 m/s²
- **Standard Deviation**: 0.017 m/s²
- **Bias Mean**: 0.1 m/s²
- **Bias Standard Deviation**: 0.001 m/s²

#### Y-axis
- **Mean**: 0.0 m/s²
- **Standard Deviation**: 0.017 m/s²
- **Bias Mean**: 0.1 m/s²
- **Bias Standard Deviation**: 0.001 m/s²

#### Z-axis
- **Mean**: 0.0 m/s²
- **Standard Deviation**: 0.017 m/s²
- **Bias Mean**: 0.1 m/s²
- **Bias Standard Deviation**: 0.001 m/s²

#### ROS Topic
```
world/z_my_forest/model/x500_custom_0/link/imu_link/sensor/imu/imu
```

---

## 📍 GPS Sensor Parameters

**File**: `Tools/simulation/gz/models/x500_custom/model.sdf`

### Physical Configuration
- **Position**: `(0, 0, 0.15)` meters (top center of drone)
- **Mass**: 0.003 kg
- **Size**: Sphere with radius 0.015 meters
- **Update Rate**: 10 Hz

### GPS Noise Parameters
- **Horizontal Position Noise**: 0.05 meters
- **Vertical Position Noise**: 0.05 meters
- **Horizontal Velocity Noise**: 0.05 m/s
- **Vertical Velocity Noise**: 0.05 m/s

#### ROS Topic
```
world/z_my_forest/model/x500_custom_0/link/gps_link/sensor/gps/navsat
```

---

## 🚁 Drone Physical Parameters

**File**: `ROMFS/px4fmu_common/init.d-posix/airframes/4001_gz_x500`

### Rotor Configuration
- **Rotor 0**: Position `(0.13, 0.22, 0)` with KM=0.05
- **Rotor 1**: Position `(-0.13, -0.20, 0)` with KM=0.05
- **Rotor 2**: Position `(0.13, -0.22, 0)` with KM=-0.05
- **Rotor 3**: Position `(-0.13, 0.20, 0)` with KM=-0.05

### Flight Parameters
- **Hover Throttle**: 0.60
- **Navigation DLL Active**: 2
- **Airframe Type**: Quadrotor

---

## 🔧 Configuration for SLAM Systems

### ORB-SLAM 3 Configuration

#### Camera Intrinsics Matrix
```cpp
cv::Mat K = (cv::Mat_<float>(3,3) <<
    320.0, 0.0, 320.0,
    0.0, 240.0, 240.0,
    0.0, 0.0, 1.0);
```

#### Distortion Coefficients
```cpp
cv::Mat distCoeffs = (cv::Mat_<float>(5,1) << 0.0, 0.0, 0.0, 0.0, 0.0);
```

#### Stereo Configuration
```cpp
float baseline = 0.08;  // 8cm baseline
```

### OpenVINS Configuration

#### IMU Parameters
```yaml
# Gyroscope
gyroscope_noise_density: 0.0002      # rad/s/sqrt(Hz)
gyroscope_random_walk: 0.0000008     # rad/s^2/sqrt(Hz)
gyroscope_bias: 0.0000075            # rad/s

# Accelerometer
accelerometer_noise_density: 0.017   # m/s^2/sqrt(Hz)
accelerometer_random_walk: 0.001     # m/s^3/sqrt(Hz)
accelerometer_bias: 0.1              # m/s^2
```

#### Camera Parameters
```yaml
# Camera intrinsics
fx: 320.0
fy: 240.0
cx: 320.0
cy: 240.0

# Distortion
k1: 0.0
k2: 0.0
k3: 0.0
p1: 0.0
p2: 0.0

# Stereo baseline
baseline: 0.08
```

### ROS2 Configuration

#### Camera Info Message
```yaml
header:
  frame_id: "camera_link"
height: 480
width: 640
distortion_model: "plumb_bob"
D: [0.0, 0.0, 0.0, 0.0, 0.0]
K: [320.0, 0.0, 320.0, 0.0, 240.0, 240.0, 0.0, 0.0, 1.0]
P: [320.0, 0.0, 320.0, 0.0, 0.0, 240.0, 240.0, 0.0, 0.0, 0.0, 1.0, 0.0]
```

#### IMU Message
```yaml
header:
  frame_id: "imu_link"
angular_velocity_covariance: [0.0002, 0.0, 0.0, 0.0, 0.0002, 0.0, 0.0, 0.0, 0.0002]
linear_acceleration_covariance: [0.017, 0.0, 0.0, 0.0, 0.017, 0.0, 0.0, 0.0, 0.017]
```

---

## 📁 File Locations

- **Single Camera Model**: `Tools/simulation/gz/models/x500_custom/model.sdf`
- **Stereo Camera Model**: `Tools/simulation/gz/models/x500_stereo/model.sdf`
- **Airframe Config**: `ROMFS/px4fmu_common/init.d-posix/airframes/4030_gz_x500_custom`
- **Base Airframe**: `ROMFS/px4fmu_common/init.d-posix/airframes/4001_gz_x500`

---

## 🔄 Update Notes

- **Last Updated**: [Current Date]
- **PX4 Version**: Based on current PX4-Autopilot repository
- **Model**: x500_custom and x500_custom_stereo
- **Simulation**: Gazebo (Garden)

---

*This document serves as a reference for configuring SLAM systems with the x500_custom drone. All parameters are extracted from the actual PX4 configuration files and are ready for use in ORB-SLAM 3, OpenVINS, or other visual-inertial odometry systems.*
