# Quick Test Guide for Custom PX4 Setup

## Your Custom Files

✅ **Custom World**: `z_my_forest.sdf` - Oil palm plantation simulation
✅ **Custom Model**: `x500_custom` - Custom drone with specific sensors  
✅ **Custom Airframe**: `4030_gz_x500_custom` - Airframe configuration
✅ **Custom Launch**: `single_vehicle_spawn_plantation.launch` - Launch file

## Quick Test Commands

### 1. Build Your Custom Setup
```bash
# Clean build
make clean

# Build with your custom airframe
make px4_sitl gz_x500_custom
```

### 2. Run with Custom World
```bash
# Run with your custom world
PX4_GZ_WORLD=z_my_forest make px4_sitl gz_x500_custom
```

### 3. Alternative Launch Method
```bash
# Use your custom launch file
ros2 launch px4_ros_compositor single_vehicle_spawn_plantation.launch
```

## Expected Behavior

- **World**: Should show 16 trees arranged in a 4x4 grid (excluding origin)
- **Drone**: Should spawn at (0,0,0) with your custom sensor configuration
- **Simulation**: Should run without errors

## Troubleshooting

### If build fails:
```bash
make clean
make px4_sitl gz_x500_custom
```

### If world doesn't load:
```bash
# Check if world file exists
ls Tools/simulation/gz/worlds/z_my_forest.sdf
```

### If model doesn't appear:
```bash
# Check if model files exist
ls Tools/simulation/gz/models/x500_custom/
```

## Version Control Status

✅ **Main Repository**: Pushed to https://github.com/kteo0018/PX4-Autopilot
✅ **Custom Branch**: `custom-x500-forest`
⚠️ **Submodule**: Changes are local (see CUSTOM_SETUP_GUIDE.md for details)

## Next Steps

1. Test the simulation thoroughly
2. Adjust sensor parameters as needed
3. Add more custom features
4. Consider contributing to upstream if useful

---

For detailed version control management, see `CUSTOM_SETUP_GUIDE.md`
