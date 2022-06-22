from time import time
import rclpy

from rclpy.node import Node

# import QoS Profiiles Library
from rclpy.qos import QoSProfile
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSReliabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSLivelinessPolicy

from datetime import datetime
from rclpy.exceptions import ParameterAlreadyDeclaredException

from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult

# import custome message
from tutorial_interfaces.msg import Num

DEFAULT_PUBLISH_TOPIC = "pong_msg"      # topic name of publisher of receiver
DEFAULT_SUBSCRIBE_TOPIC = "ping_msg"    # topic name of subscriber of receiver

DEFAULT_MSG_SIZE = Num

DEFAULT_QOS_DEPTH = 10
DEFAULT_QOS_RELIABILITY = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE
DEFAULT_QOS_DURABILITY  = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_VOLATILE
DEFAULT_QOS_HISTORY     = QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST

DEFAULT_QOS_BEST_EFFORT = False
DEFAULT_QOS_HISTORY_KEEP_ALL = False
DEFAULT_QOS_DURABILITY_TRANSIENT_LOCAL = False

class RECEIVER(Node):
    def __init__(self):
        super().__init__('receiver')

        # define configurable topic name through parameter
        self.MsgSize                        = DEFAULT_MSG_SIZE

        self.PublishTopic                   = DEFAULT_PUBLISH_TOPIC
        self.SubscribeTopic                 = DEFAULT_SUBSCRIBE_TOPIC

        self.QosDepth                       = DEFAULT_QOS_DEPTH
        self.QosReliability                 = DEFAULT_QOS_RELIABILITY
        self.QosDurability                  = DEFAULT_QOS_DURABILITY
        self.QosHistory                     = DEFAULT_QOS_HISTORY
        self.QosBestEffort                  = DEFAULT_QOS_BEST_EFFORT
        self.QosDurabilityTransientLocal    = DEFAULT_QOS_DURABILITY_TRANSIENT_LOCAL
        self.QosHistoryKeepAll              = DEFAULT_QOS_HISTORY_KEEP_ALL

        # declare parameters
        self.declare_parameters(
            namespace='',
            parameters=[
                ('pong_pub_topic',                  self.PublishTopic),
                ('pong_sub_topic',                  self.SubscribeTopic),
                ('qos_depth',                       self.QosDepth),
                ('qos_best_effort',                 self.QosBestEffort),
                ('qos_durability_transient_local',  self.QosDurabilityTransientLocal),
                ('qos_history_keep_all',            self.QosHistoryKeepAll)
            ]
        )

        # get value from parameter file
        self.PublishTopic                   =   self.get_parameter('pong_pub_topic').value
        self.SubscribeTopic                 =   self.get_parameter('pong_sub_topic').value
        self.QosDepth                       =   self.get_parameter('qos_depth').value
        self.QosBestEffort                  =   self.get_parameter('qos_best_effort').value
        self.QosDurabilityTransientLocal    =   self.get_parameter('qos_durability_transient_local').value
        self.QosHistoryKeepAll              =   self.get_parameter('qos_history_keep_all').value

        self.add_on_set_parameters_callback(self.ParamCallback)
        self.setQosPolicy()

        self.makeSubscriber()
        self.makePublisher()
        
    # Set QoS Profiles
    def setQosPolicy(self):
        self.setReliablityPolicy()
        self.setDurability()
        self.setHistory()

        self.qos = QoSProfile(
            depth = self.QosDepth,
            reliability = self.QosReliability,
            durability = self.QosDurability,
            history = self.QosHistory
        )

    # Set Reliability QoS Policies from parameter
    def setReliablityPolicy(self):
        if (self.QosBestEffort == True):
            self.QosReliability = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT
        else:
            self.QosReliability = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE

    # Set Durability QoS Policies from parameter    
    def setDurability(self):
        if(self.QosDurabilityTransientLocal == True):
            self.QosDurability = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL
        else:
            self.QosDurability = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_VOLATILE

    # Set History QoS Policies from parameter
    def setHistory(self):
        if(self.QosHistoryKeepAll == True):
            self.QosHistory = QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_ALL
        else:
            self.QosHistory = QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST

    # Set Topic name of publisher from parameter
    def setPubTopicName(self, pubtopicName):
        self.PublishTopic = pubtopicName

    # Set Topic name of subscriber from parameter
    def setSubTopicName(self, subtopicName):
        self.SubscribeTopic = subtopicName

    # Create Publisher
    def makePublisher(self):
        self.publisher_ = self.create_publisher(
            self.MsgSize, 
            self.PublishTopic, 
            self.qos)

    # Create Subscriber
    def makeSubscriber(self):
        self.subcriber_ = self.create_subscription(self.MsgSize, self.SubscribeTopic, self.SubCallback, self.qos)
        self.subcriber_

    # Subscription callback
    def SubCallback(self,msg):
        dt = datetime.now()
        time_stamp = datetime.timestamp(dt) * 1000
        self.get_logger().info('Hear from sender, response back from ROS2 {}'.format(dt))
        self.publisher_.publish(msg)
        

    def setBesteffort(self, value):
        self.QosBestEffort = value

    def setTransientLocal(self, value):
        self.QosDurabilityTransientLocal = value

    def setKeepAll(self, value):
        self.QosHistoryKeepAll = value

    def setDepth(self, value):
        self.QosDepth = value

    # Handle parameter updates
    def ParamCallback(self, params):
        for param in params:

            if param.name == 'qos_depth' and param.type_ == Parameter.Type.INTEGER:
                self.setDepth(param.value)

            elif param.name == 'qos_best_effort' and param.type_ == Parameter.Type.BOOL:
                self.setBesteffort(param.value)

            elif param.name == 'qos_durability_transient_local' and param.type_ == Parameter.Type.BOOL:
                self.setTransientLocal(param.value)
            
            elif param.name == 'qos_history_keep_all' and param.type_ == Parameter.Type.BOOL:
                self.setKeepAll(param.value)

            elif param.name == 'pong_pub_topic' and param.type_ == Parameter.Type.STRING:
                setPubTopicName(param.value)
                # makePublisher()

            elif param.name == 'pong_sub_topic' and param.type_ == Parameter.Type.STRING:
                setSubTopicName(param.value)
                # makeSubscriber()
            
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    Receviver = RECEIVER()
    rclpy.spin(Receviver)
    Receviver.destroy_node()
    rclpy.shutdown()

main()
