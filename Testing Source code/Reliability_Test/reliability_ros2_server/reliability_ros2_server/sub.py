import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSReliabilityPolicy
from rclpy.qos import QoSHistoryPolicy

import csv
from datetime import datetime

from tutorial_interfaces.msg import Reliability_msg

open('my_data.csv', mode='w')
start_time_stamp = datetime.now()

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.qos = QoSProfile(
            depth = 1000,
            reliability = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE,
            durability = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_VOLATILE,
            history = QoSHistoryPolicy.KEEP_LAST
        )

        self.subscription = self.create_subscription(
            Reliability_msg,
            'topic',
            self.listener_callback,
            self.qos)
        
        self.i = 0
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        with open('my_data.csv', 'a') as f:
              writer = csv.writer(f)
              end_time_stamp = datetime.now()
              time_stamp = end_time_stamp - start_time_stamp
              writer.writerow([time_stamp, msg.count, self.i])
        f.close()
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
