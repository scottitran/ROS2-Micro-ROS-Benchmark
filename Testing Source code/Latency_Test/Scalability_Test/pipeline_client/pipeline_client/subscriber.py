import sys
import rclpy
#from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
#from rclpy.executors import MultiThreadedExecutor
import csv
from rclpy.executors import ExternalShutdownException

from datetime import datetime
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSReliabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSLivelinessPolicy

from rclpy.exceptions import ParameterAlreadyDeclaredException

from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult

from std_msgs.msg import Int32MultiArray
#from tutorial_interfaces.msg import Num
DEFAULT_PUBLISH_TOPIC = "pong_msg"

open('my_data.csv', mode='w')

DEFAULT_SUBSCRIBE_TOPIC = "ping_msg"

DEFAULT_MSG_SIZE = Int32MultiArray

DEFAULT_QOS_DEPTH = 10
DEFAULT_QOS_RELIABILITY = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE
DEFAULT_QOS_DURABILITY = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL

DEFAULT_QOS_BEST_EFFORT = False

DEFAULT_QOS_HISTORY_KEEP_LAST = True
DEFAULT_QOS_HISTORY_KEEP_ALL = False

DEFAULT_QOS_DURABILITY_TRANSIENT_LOCAL = True


class BTN_SUB(Node):
    def __init__(self):
        super().__init__('btn_sub')

        self.msg_size = DEFAULT_MSG_SIZE

        self.publish_topic = DEFAULT_PUBLISH_TOPIC
        self.subscribe_topic = DEFAULT_SUBSCRIBE_TOPIC

        self.qos_depth = DEFAULT_QOS_DEPTH
        self.qos_reliability = DEFAULT_QOS_RELIABILITY
        self.qos_durability = DEFAULT_QOS_DURABILITY
        self.qos_best_effort = DEFAULT_QOS_BEST_EFFORT
        self.qos_durability_transient_local = DEFAULT_QOS_DURABILITY_TRANSIENT_LOCAL

        # declare parameters
        self.declare_parameters(
            namespace='',
            parameters=[
                ('pong_pub_topic',  self.publish_topic),
                ('pong_sub_topic',  self.subscribe_topic),
                ('qos_depth',       self.qos_depth),
                ('qos_best_effort', self.qos_best_effort),
                ('qos_durability_transient_local', self.qos_durability_transient_local)
            ]
        )

        # get value from parameter file
        self.publish_topic      =   self.get_parameter('pong_pub_topic').value
        self.subscribe_topic    =   self.get_parameter('pong_sub_topic').value
        self.qos_depth          =   self.get_parameter('qos_depth').value
        self.qos_best_effort    =   self.get_parameter('qos_best_effort').value
        self.qos_durability_transient_local =   self.get_parameter('qos_durability_transient_local').value

        self.add_on_set_parameters_callback(self.param_callback)
        self.setQOS_POLICY()

        self.makeSubscriber()
        self.makePublisher()
        

    def setReliablityPolicy(self):
        if (self.qos_best_effort == True):
            self.qos_reliability = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT
        else:
            self.qos_reliability = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE

    def setDurability(self):
        if(self.qos_durability_transient_local == True):
            self.qos_durability = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL
        else:
            self.qos_durability = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_VOLATILE

    def setQOS_POLICY(self):
        self.setReliablityPolicy()
        self.setDurability()

        self.qos = QoSProfile(
            depth = self.qos_depth,
            reliability = self.qos_reliability,
            durability = self.qos_durability,
            history = QoSHistoryPolicy.KEEP_LAST
        )

    def setPubTopicName(self, pubtopicName):
        self.publish_topic = pubtopicName

    def setSubTopicName(self, subtopicName):
        self.subscribe_topic = subtopicName

    def makePublisher(self):
        self.publisher_ = self.create_publisher(
            self.msg_size, 
            self.publish_topic, 
            self.qos)

    def makeSubscriber(self):
        self.subcriber_ = self.create_subscription(self.msg_size, self.subscribe_topic, self.sub_callback, self.qos)
        self.subcriber_

    def sub_callback(self,msg):
        #dt = datetime.now().strftime('%S.%f')[:-1]
        #time_stamp = dt.timestamp() * 1000
        #time_stamp = dt.strftime('%S.%3f')[:-3]
        #self.get_logger().info('{}, {}'.format(msg.signal, dt))
        #with open('my_data.csv', 'a') as f: 
        #      writer = csv.writer(f)
        #      writer.writerow([msg.signal, dt])
        #f.close()

        self.publisher_.publish(msg)
        #self.get_logger().info('after receive sending new msg')

    def setBesteffort(self, value):
        self.qos_best_effort = value

    def setTransientLocal(self, value):
        self.qos_durability_transient_local = value

    def setDepth(self, value):
        self.qos_depth = value

    def param_callback(self, params):
        for param in params:

            if param.name == 'qos_depth' and param.type_ == Parameter.Type.INTEGER:
                self.setDepth(param.value)

            elif param.name == 'qos_best_effort' and param.type_ == Parameter.Type.BOOL:
                self.setBesteffort(param.value)
                
            elif param.name == 'qos_best_effort' and param.type_ == Parameter.Type.BOOL:
                self.setTransientLocal(param.value)

            elif param.name == 'pong_pub_topic' and param.type_ == Parameter.Type.STRING:
                setPubTopicName(param.value)
                # makePublisher()

            elif param.name == 'pong_sub_topic' and param.type_ == Parameter.Type.STRING:
                setSubTopicName(param.value)
                # makeSubscriber()
            
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    try:
       btn_sub = BTN_SUB()
       rclpy.spin(btn_sub)
    #except KeyboardInterrupt:
    #   pass
    except ExternalShutdownException:
       sys.exit(1)
    finally:
       btn_sub.destroy_node()
       rclpy.try_shutdown()

main()
