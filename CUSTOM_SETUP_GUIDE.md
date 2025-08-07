# PX4 Custom Setup Guide

This guide explains how to manage your custom modifications to PX4-Autopilot with proper version control.

## Your Custom Modifications

### 1. Custom Drone Model: `x500_custom`
- **Location**: `Tools/simulation/gz/models/x500_custom/`
- **Files**: 
  - `model.sdf` - 3D model definition
  - `model.config` - Model metadata

### 2. Custom World: `z_my_forest.sdf`
- **Location**: `Tools/simulation/gz/worlds/z_my_forest.sdf`
- **Description**: Oil palm plantation simulation with 16 trees arranged in a grid

### 3. Custom Airframe: `4030_gz_x500_custom`
- **Location**: `ROMFS/px4fmu_common/init.d-posix/airframes/4030_gz_x500_custom`
- **Description**: Airframe configuration for your custom x500_custom model

### 4. Custom Launch File: `single_vehicle_spawn_plantation.launch`
- **Location**: `launch/single_vehicle_spawn_plantation.launch`
- **Description**: Launch file for spawning your custom drone in the plantation world

## Version Control Setup

### Repository Structure
```
PX4-Autopilot (your fork)
├── origin: https://github.com/kteo0018/PX4-Autopilot.git (your fork)
├── upstream: https://github.com/PX4/PX4-Autopilot.git (original)
└── branch: custom-x500-forest (your custom work)
```

### Current Status
✅ **Main Repository**: Your custom changes are committed and pushed to your fork
⚠️ **Submodule Issue**: The `Tools/simulation/gz` submodule points to the original PX4 repository where you don't have write access

## Recommended Solutions

### Option 1: Keep Submodule Changes Local (Recommended)
Since you can't push to the original submodule repository, keep your submodule changes local:

```bash
# Your submodule changes are already committed locally
# They will be included when you clone your repository
cd Tools/simulation/gz
git log --oneline -5  # Check your commits
```

### Option 2: Fork the Submodule Repository
If you want to push submodule changes:

1. Fork https://github.com/PX4/PX4-gazebo-models
2. Update the submodule remote:
   ```bash
   cd Tools/simulation/gz
   git remote set-url origin https://github.com/YOUR_USERNAME/PX4-gazebo-models.git
   git push -u origin custom-x500-forest
   ```

### Option 3: Copy Files to Main Repository
Move your custom files to the main repository:

```bash
# Create directories in main repo
mkdir -p Tools/simulation/gz/worlds
mkdir -p Tools/simulation/gz/models/x500_custom

# Copy files (if needed)
cp Tools/simulation/gz/worlds/z_my_forest.sdf Tools/simulation/gz/worlds/
cp Tools/simulation/gz/models/x500_custom/* Tools/simulation/gz/models/x500_custom/
```

## Working with Your Custom Setup

### Building and Running
```bash
# Build your custom setup
make px4_sitl gz_x500_custom

# Run with your custom world
make px4_sitl gz_x500_custom gazebo-worlds/z_my_forest
```

### Updating from Upstream
```bash
# Get latest changes from original PX4
git fetch upstream
git checkout main
git merge upstream/main

# Rebase your custom branch
git checkout custom-x500-forest
git rebase main
```

### Making New Changes
```bash
# Create a new branch for changes
git checkout -b feature/new-sensor

# Make your changes
# ...

# Commit and push
git add .
git commit -m "Add new sensor configuration"
git push origin feature/new-sensor
```

## File Locations Summary

| File | Purpose | Location |
|------|---------|----------|
| `z_my_forest.sdf` | Custom plantation world | `Tools/simulation/gz/worlds/` |
| `x500_custom/` | Custom drone model | `Tools/simulation/gz/models/` |
| `4030_gz_x500_custom` | Airframe config | `ROMFS/px4fmu_common/init.d-posix/airframes/` |
| `single_vehicle_spawn_plantation.launch` | Launch file | `launch/` |

## Best Practices

1. **Always work on feature branches** before merging to main
2. **Keep submodule changes local** unless you have write access
3. **Document your changes** in commit messages
4. **Test thoroughly** before pushing changes
5. **Regularly sync with upstream** to get security updates

## Troubleshooting

### If submodule changes are lost:
```bash
cd Tools/simulation/gz
git checkout custom-x500-forest
```

### If you need to reset to a clean state:
```bash
git checkout main
git branch -D custom-x500-forest
git checkout -b custom-x500-forest
# Re-add your custom files
```

### If build fails:
```bash
make clean
make px4_sitl gz_x500_custom
```

## Next Steps

1. Test your custom setup thoroughly
2. Consider creating a pull request to upstream if your changes are useful to the community
3. Set up CI/CD for automated testing
4. Document your custom sensor configurations and parameters

---

**Note**: This setup allows you to maintain your custom work while staying in sync with the upstream PX4 development. Your custom files are safely version controlled in your fork.
