##########################################################################
# Minimal ROS2 python program, only create ROS2 node 
############################## Uncommand to use ###########################

import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node_name')
        self.create_timer(0.2, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info("Hello World")

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    
##--------------------------------------------------------------------------
## Minimal ROS2 python program with different publishers and subscribers
##--------------------------- Uncommand to use -----------------------------
##--------------------------------------------------------------------------

# import rclpy
# from rclpy.node import Node

# from std_msgs.msg import String
# from std_msgs.msg import Int32MultiArray
# import random

# class MinimalPublisher(Node):

#     def __init__(self):
#         super().__init__('minimal_publisher_memory_test')
#         self.publisher_ = self.create_publisher(Int32MultiArray, 'memory_test', 10)
#         # self.publisher1 = self.create_publisher(Int32MultiArray, 'topic1', 10)
#         # self.publisher2 = self.create_publisher(Int32MultiArray, 'topic2', 10)
#         # self.publisher3 = self.create_publisher(Int32MultiArray, 'topic3', 10)
#         # self.publisher4 = self.create_publisher(Int32MultiArray, 'topic4', 10)

#         self.subscription = self.create_subscription(
#             Int32MultiArray,
#             'memory_test',
#             self.listener_callback,
#             10)

#         # self.subscription1 = self.create_subscription(
#         #     Int32MultiArray,
#         #     'topic1',
#         #     self.listener_callback,
#         #     10)

#         # self.subscription2 = self.create_subscription(
#         #     Int32MultiArray,
#         #     'topic2',
#         #     self.listener_callback,
#         #     10)
        
#         # self.subscription3 = self.create_subscription(
#         #     Int32MultiArray,
#         #     'topic3',
#         #     self.listener_callback,
#         #     10)

#         # self.subscription4 = self.create_subscription(
#         #     Int32MultiArray,
#         #     'topic4',
#         #     self.listener_callback,
#         #     10)

#         self.subscription
#         # self.subscription1
#         # self.subscription2
#         # self.subscription3
#         # self.subscription4

#         timer_period = 0.5  # seconds
#         self.timer = self.create_timer(timer_period, self.timer_callback)

#     def listener_callback(self, msg):
#         self.get_logger().info('I heard: "%s"' % msg.data)

#     def timer_callback(self):
#         msg = Int32MultiArray()
#         for i in range(0, 246):
#             n = random.randint(0,1000)
#             msg.data.append(n)
#         self.publisher_.publish(msg)
#         # self.publisher1.publish(msg)
#         # self.publisher2.publish(msg)
#         # self.publisher3.publish(msg)
#         # self.publisher4.publish(msg)
#         # self.get_logger().info('Publishing: "%s"' % msg.data)



# def main(args=None):
#     rclpy.init(args=args)

#     minimal_publisher = MinimalPublisher()

#     rclpy.spin(minimal_publisher)

#     # Destroy the node explicitly
#     # (optional - otherwise it will be done automatically
#     # when the garbage collector destroys the node object)
#     minimal_publisher.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()