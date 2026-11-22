#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import glob
import os
import time
import random
import numpy as np

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')
        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)
        self.bridge = CvBridge()


        self.declare_parameter('dataset_dir', 'calibration_dataset')
        self.declare_parameter('pattern', '*.jpg')
        self.declare_parameter('publish_rate_hz', 2) 
        self.declare_parameter('loop_count', 2) 

        dataset_dir = self.get_parameter('dataset_dir').value
        pattern = self.get_parameter('pattern').value
        self.publish_rate = self.get_parameter('publish_rate_hz').value
        self.loop_count = self.get_parameter('loop_count').value

        dataset_dir = os.path.abspath(dataset_dir)
        
        self.image_files = sorted(glob.glob(os.path.join(dataset_dir, pattern)))
        print(f"read {len(self.image_files)} photos.repeat {self.loop_count} times")

    def publish_images(self):
        for loop in range(self.loop_count):
            print(f"Starting {loop + 1} term ")
            random.shuffle(self.image_files)
            for img_path in self.image_files:
                img = cv2.imread(img_path)
                if img is None:
                    self.get_logger().warn(f"Can't_read_image: {img_path}")
                    continue

                
                angle = random.uniform(-5, 5)
                M = cv2.getRotationMatrix2D((img.shape[1]/2, img.shape[0]/2), angle, 1)
                img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
                tx = random.randint(-10, 10)
                ty = random.randint(-10, 10)
                M_t = np.float32([[1, 0, tx], [0, 1, ty]])
                img = cv2.warpAffine(img, M_t, (img.shape[1], img.shape[0]))

                
                msg = self.bridge.cv2_to_imgmsg(img, encoding='bgr8')
                msg.header.frame_id = 'camera'
                msg.header.stamp.sec = int(time.time())
                msg.header.stamp.nanosec = int((time.time() % 1) * 1e9)

                self.publisher_.publish(msg)
                self.get_logger().info(f"pulish: {img_path}")
                time.sleep(1.0 / self.publish_rate)

        print(" Publish_finished.")

def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisher()
    try:
        node.publish_images()
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

