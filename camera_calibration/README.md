# Camera Calibration Package (ROS 2 - Jazzy)

This project contains everything required to perform camera calibration using the 
ROS 2 `camera_calibration` tool and a custom image publisher node.

---

##  Included Files

### 1. `custom_image_publisher/`
ROS 2 package that publishes images from a local dataset for calibration.

Contains:
- `image_publisher.py`  main image publishing node
- `package.xml`
- `setup.py`
- `params.yaml`  parameter file loaded at runtime

---

### 2. `calibration_dataset/`
Set of chessboard images used as input to the calibration tool.

### 3. `calib_out/`
Output generated after running the calibration GUI.
Main file:
- `ost.yaml`   final intrinsic & distortion parameters

---



##  How to Build （Build Before Run）


cd ~/camera_calib_ws
colcon build --symlink-install
source /opt/ros/jazzy/setup.bash
source install/setup.bash

## How to Run

# Terminal A  Start calibration GUI
cd ~/camera_calib_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 run camera_calibration cameracalibrator \
  --size 9x6 --square 0.035 --no-service-check \
  --ros-args -r image:=/camera/image_raw -r camera:=/camera


# Terminal B  Start image publisher
cd ~/camera_calib_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 run custom_image_publisher image_publisher \
  --ros-args --params-file src/custom_image_publisher/params.yaml