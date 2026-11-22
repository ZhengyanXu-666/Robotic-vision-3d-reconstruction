# Requirements

# This package requires:

ROS2 Jazzy

Ubuntu / WSL2 (recommended)

Python3 + OpenCV + cv_bridge

# Installed ROS packages:

sudo apt install ros-jazzy-vision-opencv ros-jazzy-cv-bridge

# Workspace Setup

~/ros2_ws/src/homography/
    ├── package.xml
    ├── setup.py
    ├── homography/
    │   └── homography_node.py
    ├── dataset/
    │   ├── im0.jpg
    │   └── im1.jpg
    └── ...

# Build the Package
cd ~/ros2_ws
colcon build --packages-select homography

# After build completes, source the workspace:
source /opt/ros/jazzy/setup.bash
source install/setup.bash

# Run

ros2 run homography homography_node

# Default dataset directory:

~/ros2_ws/src/homography/dataset/
