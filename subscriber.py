import rclpy
from rclpy.node import Node

# from std_msgs.msg import Int32
from tutorial_interfaces.msg import Num

class BTN_SUB(Node):
    def __init__(self):
        super().__init__('btn_sub')
        self.publisher_ = self.create_publisher(Num, 'pong_msg', 10)
        self.subscription=self.create_subscription(Num, 'ping_msg', self.callback, 10)
        self.subscription
    def callback(self,msg):
        # self.get_logger().info('I heard {} and start to send pong message'.format(msg.data))
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    btn_sub = BTN_SUB()
    rclpy.spin(btn_sub)

    btn_sub.destroy_node()
    rclpy.shutdown()

main()
