from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    ld = LaunchDescription()

    config = os.path.join(
        get_package_share_directory('receiver_ros2'),
        'config',
        'params.yaml'
        )

    node_1 = Node(
            package='receiver_ros2',
            # namespace='sub1',
            executable='listener',
            name='receiver',
            parameters=[config] 
        )

    ld.add_action(node_1)

    return ld
