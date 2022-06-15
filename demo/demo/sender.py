from gc import callbacks
import sys
from typing import final
import rclpy
import random

from rclpy.executors import MultiThreadedExecutor
from rclpy.executors import ExternalShutdownException
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.node import Node

# import QoS Profiiles Library
from rclpy.qos import QoSProfile
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSReliabilityPolicy
from rclpy.qos import QoSHistoryPolicy


from rclpy.exceptions import ParameterAlreadyDeclaredException

from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
from datetime import date, datetime

# import custome message
from tutorial_interfaces.msg import Num

DEFAULT_PUBLISH_FREQUENCY   = 1.0               # publisher frequency default at 1 second
DEFAULT_PUBLISH_TOPIC       = "ping_msg"        # topic name of publisher of sender
DEFAULT_SUBSCRIBE_TOPIC     = "pong_msg"        # topic name of subscriber of sender

DEFAULT_MSG_SIZE            = Num               

DEFAULT_QOS_DEPTH           = 10
DEFAULT_QOS_RELIABILITY     = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE
DEFAULT_QOS_DURABILITY      = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_VOLATILE
DEFAULT_QOS_HISTORY         = QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST


DEFAULT_QOS_BEST_EFFORT = False
DEFAULT_QOS_HISTORY_KEEP_ALL = False
DEFAULT_QOS_DURABILITY_TRANSIENT_LOCAL = False


DEFAULT_NUM = 30       # default message size is (30*4)+8 = 128 Bytes

class SENDER(Node):
    Timer = None

    def __init__(self):
        super().__init__('sender')

        # define configurable topic name through parameter
        self.MsgSize                        = DEFAULT_MSG_SIZE
        self.Num                            = DEFAULT_NUM

        self.PublishFrequency               = DEFAULT_PUBLISH_FREQUENCY
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
                ('pub_frequency',                   self.PublishFrequency),
                ('ping_pub_topic',                  self.PublishTopic),
                ('ping_sub_topic',                  self.SubscribeTopic),
                ('qos_depth',                       self.QosDepth),
                ('qos_best_effort',                 self.QosBestEffort),
                ('qos_durability_transient_local',  self.QosDurabilityTransientLocal),
                ('qos_history_keep_all',            self.QosHistoryKeepAll), 
                ('msg_num',                         self.Num)
            ]
        )

        # get value from parameter file
        self.PublishFrequency               =   self.get_parameter('pub_frequency').value
        self.PublishTopic                   =   self.get_parameter('ping_pub_topic').value
        self.SubscribeTopic                 =   self.get_parameter('ping_sub_topic').value
        self.QosDepth                       =   self.get_parameter('qos_depth').value
        self.QosBestEffort                  =   self.get_parameter('qos_best_effort').value
        self.QosDurabilityTransientLocal    =   self.get_parameter('qos_durability_transient_local').value
        self.QosHistoryKeepAll              =   self.get_parameter('qos_history_keep_all').value
        self.Num                            =   self.get_parameter('msg_num').value

        self.add_on_set_parameters_callback(self.paramCallback)
        self.setQosPolicy()

        self.makePublisher()
        self.makeSubscriber()

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

    def stopTimer(self):
        # Stops the timer when it was running
        if(self.Timer != None):
            self.Timer.cancel()

    def startTimer(self):
        # Starts the timer with new setup from parameter
        self.stopTimer()
        self.Timer = self.create_timer(self.PublishFrequency, self.TimerCallback)

    def TimerCallback(self):
        try:
            msg = self.MsgSize()    # define message type
            # fill random value into message
            for i in range(0,self.Num):
                n = random.randint(0,1000)
                msg.data.append(n) 

            dt = datetime.now()
            start_time = datetime.timestamp(dt) * 1000
            # msg.signal = "Start send msg ...: {}".format(start_time)
            self.get_logger().info('Start send msg ...: {}'.format(dt))
            self.publisher_.publish(msg)    # start publish message
        except IOError:
            self.get_logger().info('Not Publishing ...')
        except:
            e = sys.exc_info()[0]
            self.get_logger().error('Unexpected exception {}'.format(str(e)))

    # Create Publisher
    def makePublisher(self):
        self.stopTimer()
        self.publisher_ = self.create_publisher(self.MsgSize, self.PublishTopic, self.qos)
        self.startTimer()

    # Create Subscriber
    def makeSubscriber(self):
        self.subcriber_ = self.create_subscription(self.MsgSize, self.SubscribeTopic, self.SubCallback, self.qos)
        self.subcriber_

    # Subscription callback
    def SubCallback(self,msg):
        dt1 = datetime.now()
        end_time = datetime.timestamp(dt1)
        self.get_logger().info('Receive response from ROS2 using python {}'.format(dt1))

    def setBesteffort(self, value):
        self.QosBestEffort = value

    def setTransientLocal(self, value):
        self.QosDurabilityTransientLocal = value

    def setKeepAll(self, value):
        self.QosHistoryKeepAll = value

    def setDepth(self, value):
        self.QosDepth = value

    def setMsgNum(self, value):
        self.Num = value

    def setPubFrequency(self, value):
        self.PublishFrequency = value

    # Handle parameter updates
    def paramCallback(self, params):
        for param in params:

            if param.name == 'msg_num' and param.type_ == Parameter.Type.INTEGER:
                self.setMsgNum(param.value)

            elif param.name == 'qos_depth' and param.type_ == Parameter.Type.INTEGER:
                self.setDepth(param.value)

            elif param.name == 'qos_best_effort' and param.type_ == Parameter.Type.BOOL:
                self.setBesteffort(param.value)

            elif param.name == 'qos_durability_transient_local' and param.type_ == Parameter.Type.BOOL:
                self.setTransientLocal(param.value)

            elif param.name == 'qos_history_keep_all' and param.type_ == Parameter.Type.BOOL:
                self.setKeepAll(param.value)

            elif param.name == 'pub_frequency' and param.type_ == Parameter.Type.DOUBLE:
                self.setPubFrequency(param.value)
                self.startTimer()

            elif param.name == 'ping_pub_topic' and param.type_ == Parameter.Type.STRING:
                setPubTopicName(param.value)
                # makePublisher()

            elif param.name == 'ping_sub_topic' and param.type_ == Parameter.Type.STRING:
                setSubTopicName(param.value)
                # makeSubscriber()
            
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    Sender = SENDER()
    rclpy.spin(Sender)
    Sender.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()