import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from datetime import datetime
# from std_msgs.msg import Int32
from std_msgs.msg import Int32MultiArray
# from tutorial_interfaces.msg import Num128b
# from tutorial_interfaces.msg import Num1kb
# from tutorial_interfaces.msg import Num10kb
# from tutorial_interfaces.msg import Num100kb
# from tutorial_interfaces.msg import Num500kb

import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

# RED_LED = 23
GREEN_LED = 7

class BTN_SUB(Node):
    def __init__(self):
        super().__init__('btn_sub')
        qos = QoSProfile(
            depth = 1000,
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE,
            durability = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_VOLATILE,
            history = QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST
        )
        self.subscription=self.create_subscription(Int32MultiArray, 'ping_msg13', self.callback, qos)
        self.subscription
    def callback(self,msg):
        # self.get_logger().info('I heard {} and start to send pong message'.format(msg.data))
        GPIO.output(GREEN_LED,GPIO.LOW)
        end_time = datetime.now()
        self.get_logger().info('Sub at {}'.format(end_time))


def main(args=None):
    GPIO.setup(GREEN_LED,GPIO.OUT)
    rclpy.init(args=args)
    btn_sub = BTN_SUB()
    rclpy.spin(btn_sub)

    btn_sub.destroy_node()
    rclpy.shutdown()

main()
