# Homography Tutorial

**7CCEMSAP - Sensing and Perception Module**

This tutorial provides a hands-on introduction to Homography in ROS2, focusing on planar transformations between different viewpoints. Homography is essential for robotics applications including object recognition, visual servoing, and 3D scene understanding.

> **📋 Complete Solutions Provided**: This repository contains the complete working solutions for the Homography activity. Use these as reference implementations while learning computer vision concepts.

> **📄 PDF Version Available**: A formatted PDF version of this tutorial is available in the `resources/` directory for offline reading and printing.

## Learning Objectives

This tutorial introduces **Homography** - a fundamental concept in computer vision and robotics for understanding planar transformations between different viewpoints. Homography is essential for applications such as robot navigation, object recognition, and 3D scene understanding.

**Prerequisites**: 
- Working ROS2 environment
- Basic familiarity with computer vision concepts
- Understanding of geometric transformations

**Learning Goals:**
- **Homography matrix** computation and properties
- **Planar transformation** between different viewpoints
- **Feature matching** for homography estimation
- **Image warping** and perspective correction
- **ROS2 integration** for real-time homography processing

## What is Homography?

Homography is a transformation that maps points from one plane to another plane. It is particularly useful for:

- **Planar object recognition** from different viewpoints
- **Perspective correction** and image rectification
- **Camera pose estimation** from planar scenes
- **Image stitching** and panorama creation
- **Visual servoing** in robotics

Homography is widely used in robotics applications including:
- Autonomous navigation and mapping
- Object recognition and tracking
- Augmented reality and visual servoing
- Image registration and alignment

## Step-by-Step Tutorial

### Step 1: Setup

**Add the Homography package to your existing ROS2 workspace:**

```bash
# Navigate to your existing ROS2 workspace
cd ~/ros2_ws/src

# Clone the Homography repository
git clone https://github.kcl.ac.uk/7CCEMSAP/homography.git homography

# Build the new package
cd ~/ros2_ws
colcon build --packages-select homography
source install/setup.bash
```

**Verify your workspace structure:**
After setup, your workspace should look like this:
```
~/ros2_ws/
├── build/          # Build artifacts (generated)
├── install/        # Installed packages (generated)
├── log/           # Build logs (generated)
└── src/           # Source packages
    └── homography/ # This tutorial package
        ├── package.xml
        ├── setup.py
        ├── setup.cfg
        ├── homography/ # Python package directory
        │   ├── __init__.py
        │   └── homography_node.py
        ├── dataset/ # Sample images
        └── resources/
            └── homography.pdf # PDF version of tutorial
```

### Step 2: Check Your Dataset

**Dataset Location:**
Ensure that your dataset is placed in:
```bash
~/ros2_ws/src/homography/dataset/
```

**Check your dataset:**
```bash
ls ~/ros2_ws/src/homography/dataset/
```

You should see sample images in the dataset folder.

**Supported Formats:**
Each image should be in `.jpg`, `.png`, or `.jpeg` format.

### Step 3: Understanding the Code

> **📁 Code Location**: The complete working code has been provided for you! You can find the main Homography implementation in:
> ```bash
> ~/ros2_ws/src/homography/homography/homography_node.py
> ```
> This file contains the complete solution that you can examine, run, and modify.

**The Homography node does the following:**

1. **Loads image pairs** from datasets
2. **Detects and matches features** between images
3. **Computes homography matrix** using RANSAC
4. **Warps images** using the homography transformation
5. **Visualizes results** and publishes to ROS2

**Key parameters you can modify:**
- `max_features`: Maximum number of features to detect
- `match_ratio`: Lowe's ratio test threshold
- `ransac_threshold`: RANSAC threshold for homography estimation
- `warp_mode`: Type of image warping to perform

### Step 4: Code Breakdown

> **💡 Tip**: Open the code file in your editor to follow along:
> ```bash
> nano ~/ros2_ws/src/homography/homography/homography_node.py
> # or
> vim ~/ros2_ws/src/homography/homography/homography_node.py
> ```

Let's examine the Python code in detail:

#### **Homography Pipeline Overview**
The Homography node implements a complete planar transformation pipeline:

1. **Feature Detection** - Extract keypoints using SIFT detector
2. **Feature Matching** - Match features between image pairs
3. **Homography Estimation** - Compute transformation matrix using RANSAC
4. **Image Warping** - Apply homography to warp images
5. **Visualization** - Display results and transformations

#### **Homography Computation (Lines 45-65)**
```python
def compute_homography(self, kp1, kp2, matches):
    # Extract matched points
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    
    # Compute homography using RANSAC
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    
    return H, mask
```
- **Point Extraction**: Converts matched keypoints to coordinate arrays
- **RANSAC**: Robust estimation to handle outliers in feature matches
- **Homography Matrix**: 3x3 transformation matrix for planar mapping
- **Inlier Mask**: Identifies which matches are geometrically consistent

#### **Image Warping (Lines 67-85)**
```python
def warp_image(self, img, H, mode='perspective'):
    h, w = img.shape[:2]
    
    if mode == 'perspective':
        # Apply homography transformation
        warped = cv2.warpPerspective(img, H, (w, h))
    elif mode == 'affine':
        # Convert to affine transformation
        H_affine = H[:2, :]
        warped = cv2.warpAffine(img, H_affine, (w, h))
    
    return warped
```
- **Perspective Warping**: Full homography transformation
- **Affine Warping**: Simplified transformation for parallel planes
- **Image Dimensions**: Maintains original image size
- **Transformation Types**: Different warping modes for different applications

### Step 5: Run the Homography Pipeline

**Basic usage:**
```bash
cd ~/ros2_ws
source install/setup.bash

# Run the Homography node
ros2 run homography homography_node
```

**Advanced usage with custom parameters:**
```bash
# Run with custom parameters
ros2 run homography homography_node --ros-args \
  -p max_features:=500 \
  -p match_ratio:=0.75 \
  -p ransac_threshold:=5.0 \
  -p warp_mode:=perspective
```

The node will:
- Load image pairs from the dataset folder
- Compute homography between images
- Warp images using the transformation
- Display results and transformations (matches view and original vs warped)
- **Automatically save results** to the output directory
- **Gracefully terminate** after processing is complete

Saved outputs (per image pair, using filenames):
- `homography_vis_<img1>_to_<img2>.png` — side-by-side images with matched features drawn
- `warped_<img1>_to_<img2>.png` — the warped second image (into `<img2>`'s frame)
- `original_vs_warped_<img1>_to_<img2>.png` — original (left) next to warped (right)
- `H_<img1>_to_<img2>.json` — homography matrix for the pair
- `H_<img1>_to_<img2>.txt` — homography matrix (human-readable, aligned)
- `H_<img1>_to_<img2>.csv` — homography matrix (for spreadsheets)

Legacy-style warp filenames (for quick visual comparison):
- `<img1>-<img2>.png` — image 2 warped into image 1's frame (2→1)
- `<img2>-<img1>.png` — image 1 warped into image 2's frame (1→2)

Summary outputs:
- `homography_summary_<timestamp>.json` — list of all processed pairs, basic stats, parameters
  - Includes a brief human-readable summary string (pairs processed, total inliers, average inlier ratio, output folder)

### Step 6: Visualize the Results

The Homography node will automatically display:
- **Original images** side by side
- **Matched features** with correspondence lines
- **Warped images** showing perspective correction
- **Transformation visualization** with grid overlays

**Interactive visualization:**
- Windows: “Homography: original vs matches (left/right)” and “Original (left) vs Warped (right)”
- Press any key while a window is focused to advance/close (if configured)
- Check terminal output for transformation statistics

### Step 7: Advanced Exercises

#### **Multi-View Homography**
- **Goal**: Compute homography for multiple image pairs
- **Implementation**: Chain homography transformations across image sequences
- **Learning**: Understand how to build panoramic views from multiple images

#### **Homography Decomposition**
- **Goal**: Extract camera motion from homography matrix
- **Implementation**: Decompose homography into rotation and translation
- **Learning**: Understand the relationship between homography and camera pose

#### **Robust Homography Estimation**
- **Goal**: Improve homography estimation with better feature matching
- **Implementation**: Use advanced feature descriptors and matching strategies
- **Learning**: Understand how to handle challenging image pairs


## Summary

This tutorial has covered **Homography** implementation:

- **Homography Matrix**: Understanding planar transformations
- **Feature Matching**: Finding correspondences between images
- **RANSAC Estimation**: Robust homography computation
- **Image Warping**: Applying transformations for perspective correction
- **ROS2 Integration**: Real-time homography processing

Brief overview of what the node achieves:
- Loads a pair of images, detects and matches SIFT features, estimates a homography with RANSAC, and demonstrates the mapping by warping one image into the other's frame.
- Saves clear visual artifacts per pair: match visualization, original vs warped, 2→1 and 1→2 warped images, and the homography matrix in JSON, TXT, and CSV for easy inspection.

## Next Steps

**Continue Learning:**
- Implement multi-view homography and panorama stitching
- Explore homography decomposition for camera pose estimation
- Add robust feature matching and outlier rejection
- Experiment with different transformation types

**Advanced Projects:**
- Develop visual servoing systems using homography
- Implement augmented reality applications
- Create panoramic image stitching systems
- Build SLAM systems with planar scene understanding

## Troubleshooting

### Common Issues

**Poor homography estimation:**
- Check for sufficient planar content in images
- Verify good feature distribution across the image
- Adjust RANSAC threshold and match ratio
- Ensure sufficient overlap between image pairs

**Inaccurate image warping:**
- Verify homography matrix quality
- Check for degenerate cases (e.g., collinear points)
- Ensure proper image dimensions
- Validate transformation parameters

**Performance issues:**
- Reduce number of features detected
- Use smaller image resolution
- Optimize feature matching parameters
- Consider hardware acceleration

### ROS2 Commands Reference

```bash
# Build your package
colcon build --packages-select homography

# Source the workspace
source install/setup.bash

# Run a node
ros2 run homography homography_node

# List available nodes
ros2 pkg executables homography

# Check package dependencies
ros2 pkg xml homography
```

## Further Reading

- **OpenCV Documentation**: https://docs.opencv.org/
- **Homography Papers**: "Multiple View Geometry" by Hartley and Zisserman
- **Computer Vision Resources**: https://opencv.org/
- **ROS2 Computer Vision**: https://index.ros.org/p/cv_bridge/
- **Geometric Vision Tutorials**: https://docs.opencv.org/master/d9/dab/tutorial_homography.html
