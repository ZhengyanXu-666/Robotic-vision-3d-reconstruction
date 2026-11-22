from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess


def generate_launch_description():
    # SIFT feature matcher node
    sift_node = Node(
        package='sift',
        executable='sift_dataset',
        name='sift_dataset_matcher',
        output='screen',
        parameters=[{
            'max_matches': 30,
            'match_ratio': 0.7,
            'enable_ransac': True,
            'contrast_threshold': 0.04,
            'edge_threshold': 10.0
        }]
    )

    # Image viewer (rqt_image_view)
    image_view = ExecuteProcess(
        cmd=['ros2', 'run', 'rqt_image_view', 'rqt_image_view'],
        output='screen'
    )

    return LaunchDescription([sift_node, image_view])

