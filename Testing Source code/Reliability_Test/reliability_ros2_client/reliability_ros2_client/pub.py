import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSReliabilityPolicy
from rclpy.qos import QoSHistoryPolicy

import random
from std_msgs.msg import Int32
from std_msgs.msg import Int32MultiArray
from tutorial_interfaces.msg import Reliability_msg

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.qos = QoSProfile(
            depth = 1000,
            reliability = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE,
            durability = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_VOLATILE,
            history = QoSHistoryPolicy.KEEP_LAST
        )
        self.publisher_ = self.create_publisher(Reliability_msg, 'topic', self.qos)
        # self.count = self.create_publisher(Int32, 'count', 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        # self.count = 0

    def timer_callback(self):
        msg = Reliability_msg()
        # msg_count = Int32()
        for i in range(0, 30):
            n = random.randint(0,1000)
            msg.data.append(n) 
        msg.count = self.i
        # msg_count.data = self.i
        self.publisher_.publish(msg)
        # self.count.publish(msg_count)
        #self.get_logger().info('Publishing: "%s"' % self.i)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
