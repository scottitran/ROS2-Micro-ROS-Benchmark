# from distutils.command.config import config
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    config = os.path.join(
        get_package_share_directory('sender_ros2'),
        'config',
        'params.yaml'
        )
    
    node_1 = Node(
            package='sender_ros2',
            # namespace='sub1',
            executable='talker',
            name='publisher',
            parameters=[config]    
        )
 
    ld.add_action(node_1)
    return ld
