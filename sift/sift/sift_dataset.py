#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy, HistoryPolicy
import cv2
import os
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class SIFTFeatureMatcher(Node):
    def __init__(self):
        super().__init__('sift_dataset_matcher')

        sensor_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            durability=QoSDurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        
        self.image_pub = self.create_publisher(Image, '/sift_features/matched_image', sensor_qos)
        
        self.dataset_path = os.path.expanduser("~/ros2_ws/src/sift/dataset/")
        self.bridge = CvBridge()
        self.sift = cv2.SIFT_create()
        self.load_images()

    def load_images(self):
        self.image_list = []
        for file in sorted(os.listdir(self.dataset_path)):
            if file.endswith((".jpg", ".png", ".jpeg")):
                image_path = os.path.join(self.dataset_path, file)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                if image is not None:
                    self.image_list.append((file, image))
        
        self.get_logger().info(f"Loaded {len(self.image_list)} images from dataset.")

    def process_images(self):
        if len(self.image_list) < 2:
            self.get_logger().error("Not enough images for feature matching.")
            return

        # Create a timer to continuously publish matched images
        self.current_pair = 0
        self.timer = self.create_timer(3.0, self.publish_next_match)

    def publish_next_match(self):
        if len(self.image_list) < 2:
            return
            
        i = self.current_pair % (len(self.image_list) - 1)
        img1_name, img1 = self.image_list[i]
        img2_name, img2 = self.image_list[i+1]

        self.get_logger().info(f"Processing {img1_name} and {img2_name}")

        keypoints1, descriptors1 = self.sift.detectAndCompute(img1, None)
        keypoints2, descriptors2 = self.sift.detectAndCompute(img2, None)

        if descriptors1 is not None and descriptors2 is not None:
            index_params = dict(algorithm=1, trees=5)
            search_params = dict(checks=50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(descriptors1, descriptors2, k=2)

            good_matches = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)

            matched_image = cv2.drawMatches(img1, keypoints1, img2, keypoints2, good_matches, None)

            try:
                ros_image = self.bridge.cv2_to_imgmsg(matched_image, "bgr8")
                self.image_pub.publish(ros_image)
                self.get_logger().info(f"Published match with {len(good_matches)} features")
            except Exception as e:
                self.get_logger().error(f"Failed to publish image: {str(e)}")
        else:
            self.get_logger().warn(f"No descriptors found for {img1_name} or {img2_name}")

        self.current_pair += 1

def main(args=None):
    rclpy.init(args=args)
    node = SIFTFeatureMatcher()
    
    try:
        node.process_images()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()