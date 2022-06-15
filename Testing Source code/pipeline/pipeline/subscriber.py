import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy
from rclpy.qos import QoSDurabilityPolicy
import Jetson.GPIO as GPIO

from std_msgs.msg import Int32MultiArray

GPIO.setmode(GPIO.BOARD)

# RED_LED = 23
GREEN_LED = 7

class BTN_SUB(Node):
    def __init__(self):
        super().__init__('btn_sub')
        qos = QoSProfile(
            depth = 10,
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            durability = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_VOLATILE
        )

        self.subscription=self.create_subscription(Int32MultiArray, 'pong_msg', self.callback, qos)
        self.subscription

    def callback(self,msg):
        #self.get_logger().info('I heard message from pong')
        GPIO.output(GREEN_LED, GPIO.LOW)
        

def main(args=None):
    rclpy.init(args=args)
    GPIO.setup(GREEN_LED,GPIO.OUT, initial=GPIO.HIGH)
    btn_sub = BTN_SUB()
    rclpy.spin(btn_sub)

    btn_sub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
