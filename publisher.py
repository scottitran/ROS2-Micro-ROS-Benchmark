import rclpy
from rclpy.node import Node

# from std_msgs.msg import Int32
from tutorial_interfaces.msg import Num


class BTN_PUB(Node):

    def __init__(self):
        super().__init__('btn_pub')
        self.publisher_ = self.create_publisher(Num, 'ping_msg', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.subcriber_ = self.create_subscription(Num, 'pong_msg', self.callback, 10)
        self.subcriber_

    def timer_callback(self):
        msg = Num()
        # msg.data = 10
        self.publisher_.publish(msg)
        # self.get_logger().info('Publishing: {}'.format(msg.data))

    def callback(self,msg):
        self.get_logger().info('I heard from the pong')

def main(args=None):
    rclpy.init(args=args)

    btn_pub = BTN_PUB()

    rclpy.spin(btn_pub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    btn_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()