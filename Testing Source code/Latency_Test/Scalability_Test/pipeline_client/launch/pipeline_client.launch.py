from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    ld = LaunchDescription()

    config = os.path.join(
        get_package_share_directory('pipeline_client'),
        'config',
        'params.yaml'
        )

    node_1 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber',
            parameters=[config] 
        )

    node_2 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber1',
            parameters=[config] 
        )
      
    node_3 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber2',
            parameters=[config] 
        )
    node_4 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber3',
            parameters=[config] 
        )

    node_5 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber4',
            parameters=[config] 
        )

    node_6 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber5',
            parameters=[config] 
        )

    node_7 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber6',
            parameters=[config] 
        )

    node_8 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber7',
            parameters=[config] 
        )

    node_9 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber8',
            parameters=[config] 
        )

    node_10 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber9',
            parameters=[config] 
        )

    node_11 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber10',
            parameters=[config] 
        )

    node_12 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber11',
            parameters=[config] 
        )

    node_13 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber12',
            parameters=[config] 
        )

    node_14 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber13',
            parameters=[config] 
        )

    node_15 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber14',
            parameters=[config] 
        )

    node_16 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber15',
            parameters=[config] 
        )

    node_17 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber16',
            parameters=[config] 
        )
    node_18 = Node(
            package='pipeline_client',
            # namespace='sub1',
            executable='listener',
            name='subscriber17',
            parameters=[config] 
        )

    ld.add_action(node_1)
    #ld.add_action(node_2)
    #ld.add_action(node_3)
    #ld.add_action(node_4)
    #ld.add_action(node_5)
    #ld.add_action(node_6)
    #ld.add_action(node_7)
    #ld.add_action(node_8)
    #ld.add_action(node_9)
    #ld.add_action(node_10)
    #ld.add_action(node_11)
    #ld.add_action(node_12)
    #ld.add_action(node_13)
    #ld.add_action(node_14)
    #ld.add_action(node_15)
    #ld.add_action(node_16)
    #ld.add_action(node_17)
    #ld.add_action(node_18)

    return ld
