# from distutils.command.config import config
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    config = os.path.join(
        get_package_share_directory('parallel_client'),
        'config',
        'params.yaml'
        )
    
    node_1 = Node(
            package='parallel_client',
            # namespace='sub1',
            executable='talker',
            name='publisher',
            parameters=[config]    
        )

    node_2 = Node(
            package='parallel_client',
            # namespace='sub1',
            executable='talker1',
            name='publisher1',
            parameters=[config] 
        )

    node_3 = Node(
            package='parallel_client',
            # namespace='sub1',
            executable='talker1',
            name='publisher2',
            parameters=[config] 
        )      

    node_4 = Node(
            package='parallel_client',
            # namespace='sub1',
            executable='talker1',
            name='publisher3',
            parameters=[config] 
        )  

    node_5 = Node(
            package='parallel_client',
            # namespace='sub1',
            executable='talker1',
            name='publisher4',
            parameters=[config] 
        )  

    node_6 = Node(
            package='parallel_client',
            # namespace='sub1',
            executable='talker1',
            name='publisher5',
            parameters=[config] 
        )
    node_7 = Node(
            package='parallel_client',
            # namespace='sub1',
            executable='talker1',
            name='publisher6',
            parameters=[config] 
        )  

    node_8 = Node(
            package='parallel_client',
            # namespace='sub1',
            executable='talker1',
            name='publisher7',
            parameters=[config] 
        )  

    node_9 = Node(
            package='parallel_client',
            # namespace='sub1',
            executable='talker1',
            name='publisher8',
            parameters=[config] 
        )
    node_10 = Node(
            package='parallel_client',
            # namespace='sub1',
            executable='talker1',
            name='publisher9',
            parameters=[config] 
        )  

    node_11 = Node(
            package='parallel_client',
            # namespace='sub1',
            executable='talker2',
            name='publisher10',
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

    return ld
