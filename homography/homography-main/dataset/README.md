# Homography Dataset

This directory contains sample images for testing homography algorithms.

## Sample Images

The dataset includes sample images that demonstrate different types of planar transformations:
- Perspective changes
- Rotation and translation
- Scale variations
- Planar object views

## Usage

Place your own image pairs in this directory. The homography node will automatically process all supported image formats (.jpg, .png, .jpeg) in alphabetical order.

## Image Requirements

- **Format**: JPG, PNG, or JPEG
- **Naming**: Sequential naming (e.g., 001.jpg, 002.jpg, 003.jpg)
- **Content**: Planar objects or scenes for best results
- **Overlap**: Sufficient overlap between consecutive frames for feature matching

## Alternative Datasets

For testing with different types of planar scenes, you can use datasets from:
- **COCO Dataset**: Common Objects in Context
- **TUM RGB-D Dataset**: RGB-D sequences with planar scenes
- **Custom datasets**: Capture your own planar object sequences
