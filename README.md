# Each subfolder represents one independent module implemented for different stages of the 3D reconstruction and robotic manipulation pipeline. Every subfolder contains its own detailed README explaining how to build and run that specific module. This top-level README provides an overview of the purpose of each module and how they fit together.

# Repository Structure

Code/
│
├── camera_calibration/       →  Camera calibration publisher & YAML processing
│
├── homography/               →  Homography estimation & image warping
│
├── Robotic_arm_grasp_item/   →  MuJoCo robotic arm grasping demo (UR5e + gripper)
│
├── sfm/                      →  Structure-from-Motion 3D reconstruction pipeline
│
├── sift/                     →  SIFT keypoint detection & feature matching
│
└── README.md                 →  This file



# Important ! ! !:
Every module contains its own detailed README file, which explains the required dependencies, build steps, dataset location, and how to run that specific module.

This top-level README provides only a structural overview and the purpose of each folder.



# Module Overview

1. # camera_calibration

This folder contains the ROS2-based image publisher used to perform camera calibration. It publishes checkerboard images to the camera_calibration ROS2 tool and generates camera intrinsic parameters in YAML format. The output calibration data can be used in other modules such as SfM or rectification.
# Run instructions are provided inside this folder’s README.


2. # sift

This folder implements SIFT feature detection and matching in ROS2. It loads images from the dataset folder, extracts SIFT keypoints, matches them using FLANN or brute-force matching, filters matches using Lowe's ratio test, and publishes visualization results. It is used as a foundation for subsequent modules such as homography estimation and SfM.
# Run instructions are provided inside this folder’s README.


3. # homography

This module computes homography matrices between planar image pairs. It performs feature extraction, matching, RANSAC-based homography estimation, and image warping. The output includes visualizations and homography matrices saved in multiple formats. It demonstrates planar geometric transformation and image registration.
# Run instructions are provided inside this folder’s README.


4. # sfm

This folder contains the Structure-from-Motion (SfM) implementation. It loads a sequence of images, extracts features, performs feature matching, estimates camera motion using the essential matrix, triangulates 3D points, and generates a sparse 3D reconstruction. The module outputs a visualization of the reconstructed point cloud and camera trajectory.
# Run instructions are provided inside this folder’s README.


5. # Robotic_arm_grasp_item

This folder includes the MuJoCo simulation environment for robotic grasping. It contains the UR5e robot model, the gripper, and associated assets. The control script demonstrates a grasping task, where the robot approaches, grasps, lifts, and places an object. This module represents the robotic manipulation stage of the coursework.
# Run instructions are provided inside this folder’s README.


# How the Modules Connect

SIFT provides feature detection and matching.

Homography uses SIFT matches to compute planar transformations.

SfM uses SIFT matches and camera intrinsics (optional) to reconstruct a 3D point cloud.

The reconstructed model can be used as an object inside the MuJoCo simulation.

The robotic manipulation module demonstrates grasping based on the 3D model.

# Additional Notes

Each folder contains its own standalone ROS2 or MuJoCo executable.

The modules can be run independently.

The datasets used by each module should be placed in each module’s dataset folder.

The detailed instructions for building and running each module are provided inside the respective folder’s README.