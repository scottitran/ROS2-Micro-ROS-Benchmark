# from distutils.command.config import config
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    config = os.path.join(
        get_package_share_directory('button'),
        'config',
        'params.yaml'
        )
    
    node_1 = Node(
            package='button',
            # namespace='sub1',
            executable='talker',
            name='publisher',
            parameters=[config]    
        )

    node_2 = Node(
            package='button',
            # namespace='sub1',
            executable='listener',
            name='subscriber',
            parameters=[config] 
        )

    node_3 = Node(
            package='button',
            # namespace='sub1',
            executable='listener',
            name='subscriber',
            parameters=[config] 
        )      

    ld.add_action(node_1)
    # ld.add_action(node_2)
    # ld.add_action(node_3)

    return ld