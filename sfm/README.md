# 1. Requirements
Operating System

Ubuntu 24.04

# To install ROS 2 Jazzy
sudo apt update
sudo apt install ros-jazzy-desktop
sudo apt install python3-colcon-common-extensions

# 2. Workspace Setup

# Create workspace:

mkdir -p ~/ros2_ws/src
cd ~/ros2_ws


# copy the sfm package into:

~/ros2_ws/src/sfm


# Check the structure:

sfm/
 ├── package.xml
 ├── setup.py
 ├── setup.cfg
 ├── sfm/
 │    └── sfm_node.py
 ├── dataset/
 │    └── 000.jpg, 001.jpg, ...
 └── results/

# Then build:

colcon build --packages-select sfm

# Source the environment:

source /opt/ros/jazzy/setup.bash
source install/setup.bash

# 4. Run the SfM Node

ros2 run sfm sfm_node --ros-args \
  -p dataset_path:=~/ros2_ws/src/sfm/dataset \
  -p nfeatures:=1000 \
  -p ransac_threshold:=1.0 \
  -p show_visualization:=true

# Results are saved to:

~/ros2_ws/src/sfm/results/
