
# Place the package under

~/ros2_ws/src/sift

# The complete structure should look like:
ros2_ws
 └── src
      └── sift
          ├── setup.py
          ├── package.xml
          ├── launch/
          ├── sift/
          ├── resource/
          └── dataset/


# Build and Run Instructions
# Follow the steps below to build and run the SIFT ROS2 package on any machine.

# Move to your workspace
cd ~/ros2_ws

# Build the package
colcon build --packages-select sift

# Source your workspace
source install/setup.bash

# Source the ROS2 environment
source /opt/ros/jazzy/setup.bash

# Launch the system
ros2 launch sift sift.launch.py
