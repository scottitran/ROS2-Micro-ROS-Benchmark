# from distutils.command.config import config
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # Read config file from YAML file
    config = os.path.join(
        get_package_share_directory('demo'),
        'config',
        'params.yaml'
        )
        
    node_1 = Node(
            package='demo',
            # namespace='sub1',
            executable='talker',
            name='sender',
            parameters=[config]    
        )

    node_2 = Node(
            package='demo',
            # namespace='sub1',
            executable='listener',
            name='receiver',
            parameters=[config] 
        )
    

    ld.add_action(node_1)
    ld.add_action(node_2)

    return ld