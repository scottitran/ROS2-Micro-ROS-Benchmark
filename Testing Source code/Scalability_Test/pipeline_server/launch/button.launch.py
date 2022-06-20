import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    config = os.path.join(
        get_package_share_directory('pipeline'),
        'config',
        'params.yaml'
        )
    
    node_1 = Node(
            package='pipeline_server',
            # namespace='sub1',
            executable='talker',
            name='start_pipeline',
            parameters=[config]    
        )

    node_2 = Node(
            package='pipeline_server',
            # namespace='sub1',
            executable='listener',
            name='end_pipeline'
        )

    ld.add_action(node_1)
    ld.add_action(node_2)

    return ld
