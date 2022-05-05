import rclpy
from rclpy.node import Node

# from std_msgs.msg import Int32
from tutorial_interfaces.msg import Num128b
from tutorial_interfaces.msg import Num1kb
from tutorial_interfaces.msg import Num10kb
from tutorial_interfaces.msg import Num100kb
from tutorial_interfaces.msg import Num500kb

class BTN_SUB(Node):
    def __init__(self):
        super().__init__('btn_sub')
        self.publisher_ = self.create_publisher(Num128b, 'pong_msg', 10)
        self.subscription=self.create_subscription(Num128b, 'ping_msg', self.callback, 10)
        self.subscription
    def callback(self,msg):
        self.get_logger().info('I heard {} and start to send pong message'.format(msg.data))
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    btn_sub = BTN_SUB()
    rclpy.spin(btn_sub)

    btn_sub.destroy_node()
    rclpy.shutdown()

main()
