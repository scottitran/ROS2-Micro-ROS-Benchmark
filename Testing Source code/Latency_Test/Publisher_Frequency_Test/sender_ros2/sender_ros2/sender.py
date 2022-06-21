import sys
import rclpy
#from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
#from rclpy.executors import MultiThreadedExecutor
#from rclpy.executors import ExternalShutdownException
import random
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

import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GREEN_LED = 7

from std_msgs.msg import Int32MultiArray

DEFAULT_PUBLISH_FREQUENCY = 1
DEFAULT_PUBLISH_TOPIC = "ping_msg"
DEFAULT_SUBSCRIBE_TOPIC = "pong_msg"

DEFAULT_MSG_SIZE = Int32MultiArray

DEFAULT_QOS_DEPTH = 10
DEFAULT_QOS_RELIABILITY = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE
DEFAULT_QOS_DURABILITY = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL

DEFAULT_QOS_BEST_EFFORT = False
DEFAULT_QOS_HISTORY_KEEP_LAST = True
DEFAULT_QOS_HISTORY_KEEP_ALL = False
DEFAULT_QOS_DURABILITY_TRANSIENT_LOCAL = False

DEFAULT_NUM = 30
start_time = datetime.now()

class BTN_PUB(Node):
    Timer = None

    def __init__(self):
        super().__init__('btn_pub')
        #self.group = MutuallyExclusiveCallbackGroup()
        #self.group1 = MutuallyExclusiveCallbackGroup()
        #self.group2 = ReentrantCallbackGroup()
        #self.group3 = ReentrantCallbackGroup()

        self.msg_size = DEFAULT_MSG_SIZE
        self.num = DEFAULT_NUM

        self.publish_frequency = DEFAULT_PUBLISH_FREQUENCY
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
                ('pub_frequency',   self.publish_frequency),
                ('ping_pub_topic',  self.publish_topic),
                ('ping_sub_topic',  self.subscribe_topic),
                ('qos_depth',       self.qos_depth),
                ('qos_best_effort', self.qos_best_effort),
                ('qos_durability_transient_local', self.qos_durability_transient_local),
                ('msg_num', self.num)
            ]
        )

        # get value from parameter file
        self.publish_frequency  =   self.get_parameter('pub_frequency').value
        self.publish_topic      =   self.get_parameter('ping_pub_topic').value
        self.subscribe_topic    =   self.get_parameter('ping_sub_topic').value
        self.qos_depth          =   self.get_parameter('qos_depth').value
        self.qos_best_effort    =   self.get_parameter('qos_best_effort').value
        self.qos_durability_transient_local =   self.get_parameter('qos_durability_transient_local').value
        self.num    =   self.get_parameter('msg_num').value

        self.add_on_set_parameters_callback(self.param_callback)
        self.setQOS_POLICY()      
        
        self.makePublisher()
        self.makeSubscriber()

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

    def stopTimer(self):
        if(self.Timer != None):
            self.Timer.cancel()

    def startTimer(self):
        self.stopTimer()
        #start_time = datetime.now()
        self.Timer = self.create_timer(self.publish_frequency, self.timer_callback)

    def timer_callback(self):
        msg = self.msg_size()
        for i in range(0, self.num):
            n = random.randint(0, 1000)
            msg.data.append(n)
        self.publisher_.publish(msg)
        GPIO.output(GREEN_LED, GPIO.HIGH)

    def makePublisher(self):
        self.stopTimer()
        self.publisher_ = self.create_publisher(self.msg_size, self.publish_topic, self.qos)#, callback_group=self.group1)
        self.startTimer()

    def makeSubscriber(self):
        self.subcriber_ = self.create_subscription(self.msg_size, self.subscribe_topic, self.sub_callback, self.qos)
        self.subcriber_

    def sub_callback(self,msg):
        GPIO.output(GREEN_LED,GPIO.LOW)


    def setBesteffort(self, value):
        self.qos_best_effort = value

    def setTransientLocal(self, value):
        self.qos_durability_transient_local = value

    def setDepth(self, value):
        self.qos_depth = value

    def setMsgNum(self, value):
        self.num = value

    def setPubFrequency(self, value):
        self.publish_frequency = value

    def param_callback(self, params):
        for param in params:

            if param.name == 'msg_num' and param.type_ == Parameter.Type.INTEGER:
                self.setMsgNum(param.value)

            elif param.name == 'qos_depth' and param.type_ == Parameter.Type.INTEGER:
                self.setDepth(param.value)

            elif param.name == 'qos_best_effort' and param.type_ == Parameter.Type.BOOL:
                self.setBesteffort(param.value)
                
            elif param.name == 'qos_durability_transient_local' and param.type_ == Parameter.Type.BOOL:
                self.setTransientLocal(param.value)

            elif param.name == 'pub_frequency' and param.type_ == Parameter.Type.DOUBLE:
                self.setPubFrequency(param.value)
                self.startTimer()

            elif param.name == 'ping_pub_topic' and param.type_ == Parameter.Type.STRING:
                setPubTopicName(param.value)
                makePublisher()

            elif param.name == 'ping_sub_topic' and param.type_ == Parameter.Type.STRING:
                setSubTopicName(param.value)
                makeSubscriber()
            
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    GPIO.setup(GREEN_LED,GPIO.OUT, initial=GPIO.HIGH)

    btn_pub = BTN_PUB()

    rclpy.spin(btn_pub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    btn_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
