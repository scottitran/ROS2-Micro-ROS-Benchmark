import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSReliabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSLivelinessPolicy

from rclpy.exceptions import ParameterAlreadyDeclaredException

from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult

# from std_msgs.msg import Int32
from tutorial_interfaces.msg import Num128b
from tutorial_interfaces.msg import Num1kb
from tutorial_interfaces.msg import Num10kb
from tutorial_interfaces.msg import Num100kb

DEFAULT_PUBLISH_TOPIC = "pong_msg"
DEFAULT_SUBSCRIBE_TOPIC = "ping_msg"

DEFAULT_MSG_128B = True
DEFAULT_MSG_1KB = False
DEFAULT_MSG_10KB = False
DEFAULT_MSG_100KB = False

DEFAULT_MSG_SIZE = Num128b

DEFAULT_QOS_DEPTH = 10
DEFAULT_QOS_RELIABILITY = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE
DEFAULT_QOS_DURABILITY = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL

DEFAULT_QOS_RELIABLE = True
DEFAULT_QOS_BEST_EFFORT = False

DEFAULT_QOS_HISTORY_KEEP_LAST = True
DEFAULT_QOS_HISTORY_KEEP_ALL = False

DEFAULT_QOS_DURABILITY_TRANSIENT_LOCAL = True
DEFAULT_QOS_DURABILITY_VOLATILE = False


class BTN_SUB(Node):
    def __init__(self):
        super().__init__('btn_sub')

        self.msg_size = DEFAULT_MSG_SIZE

        self.publish_topic = DEFAULT_PUBLISH_TOPIC
        self.subscribe_topic = DEFAULT_SUBSCRIBE_TOPIC

        self.msg_128B = DEFAULT_MSG_128B
        self.msg_1KB = DEFAULT_MSG_1KB
        self.msg_10KB = DEFAULT_MSG_10KB
        self.msg_100KB = DEFAULT_MSG_100KB

        self.qos_depth = DEFAULT_QOS_DEPTH
        self.qos_reliability = DEFAULT_QOS_RELIABILITY
        self.qos_durability = DEFAULT_QOS_DURABILITY
        self.qos_best_effort = DEFAULT_QOS_BEST_EFFORT
        self.qos_reliable = DEFAULT_QOS_RELIABLE
        self.qos_durability_transient_local = DEFAULT_QOS_DURABILITY_TRANSIENT_LOCAL
        self.qos_durability_volatile = DEFAULT_QOS_DURABILITY_VOLATILE

        # declare parameters
        self.declare_parameters(
            namespace='',
            parameters=[
                ('pong_pub_topic',  self.publish_topic),
                ('pong_sub_topic',  self.subscribe_topic),
                ('msg_128B',        self.msg_128B),
                ('msg_1KB',         self.msg_1KB),
                ('msg_10KB',        self.msg_10KB),
                ('msg_100KB',       self.msg_100KB),
                ('qos_depth',       self.qos_depth),
                ('qos_best_effort', self.qos_best_effort),
                ('qos_reliable', self.qos_reliable),
                ('qos_durability_transient_local', self.qos_durability_transient_local),
                ('qos_durability_volatile', self.qos_durability_volatile)
            ]
        )

        # get value from parameter file
        self.publish_topic      =   self.get_parameter('pong_pub_topic').value
        self.subscribe_topic    =   self.get_parameter('pong_sub_topic').value
        self.msg_128B           =   self.get_parameter('msg_128B').value
        self.msg_1KB            =   self.get_parameter('msg_1KB').value
        self.msg_10KB           =   self.get_parameter('msg_10KB').value
        self.msg_100KB          =   self.get_parameter('msg_100KB').value
        self.qos_depth          =   self.get_parameter('qos_depth').value
        self.qos_best_effort    =   self.get_parameter('qos_best_effort').value
        self.qos_reliable       =   self.get_parameter('qos_reliable').value
        self.qos_durability_transient_local =   self.get_parameter('qos_durability_transient_local').value
        self.qos_durability_volatile        =   self.get_parameter('qos_durability_volatile').value

        self.add_on_set_parameters_callback(self.param_callback)
        self.setQOS_POLICY()
        self.setMSG_Size()

        self.makeSubscriber()
        self.makePublisher()
        

    def setReliablityPolicy(self):
        if (self.qos_best_effort == True):
            self.qos_reliability = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT
        elif(self.qos_reliable == True):
            self.qos_reliability = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE

    def setDurability(self):
        if(self.qos_durability_transient_local == True):
            self.qos_durability = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL
        elif(self.qos_durability_volatile == True):
            self.qos_durability = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_VOLATILE

    def setQOS_POLICY(self):
        self.setReliablityPolicy()
        self.setDurability()

        self.qos = QoSProfile(
            depth = self.qos_depth,
            reliability = self.qos_reliability,
            durability = self.qos_durability
        )

    def setMSG_Size(self):
        if (self.msg_128B == True):
            self.msg_size = Num128b
        elif( self.msg_1KB == True):
            self.msg_size = Num1kb
        elif (self.msg_10KB == True):
            self.msg_size = Num10kb
        elif (self.msg_100KB == True):
            self.msg_size = Num100kb

    def setPubTopicName(self, pubtopicName):
        self.publish_topic = pubtopicName

    def setSubTopicName(self, subtopicName):
        self.subscribe_topic = subtopicName

    def set128B_MSG(self, value):
        self.msg_128B = value

    def set1KB_MSG(self, value):
        self.msg_1KB = value
    
    def set10KB_MSG(self, value):
        self.msg_10KB = value

    def set100KB_MSG(self, value):
        self.msg_100KB = value

    def makePublisher(self):
        self.publisher_ = self.create_publisher(
            self.msg_size, 
            self.publish_topic, 
            self.qos)
        # QoSProfile(depth = 10,
        #     reliability = QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
        #     durability = QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_VOLATILE))

    def makeSubscriber(self):
        self.subcriber_ = self.create_subscription(self.msg_size, self.subscribe_topic, self.sub_callback, self.qos)
        self.subcriber_

    def sub_callback(self,msg):
        self.publisher_.publish(msg)

    def setBesteffort(self, value):
        self.qos_best_effort = value

    def setReliable(self, value):
        self.qos_reliable = value

    def setTransientLocal(self, value):
        self.qos_durability_transient_local = value

    def setVolatile(self, value):
        self.qos_durability_volatile = value

    def param_callback(self, params):
        for param in params:

            if param.name == 'msg_128B' and param.type_ == Parameter.Type.BOOL:
                self.set128B_MSG(param.value)

            elif param.name == 'msg_1KB' and param.type_ == Parameter.Type.BOOL:
                self.set1KB_MSG(param.value)

            elif param.name == 'msg_10KB' and param.type_ == Parameter.Type.BOOL:
                self.set10KB_MSG(param.value)

            elif param.name == 'msg_100KB' and param.type_ == Parameter.Type.BOOL:
                self.set100KB_MSG(param.value)

            elif param.name == 'qos_best_effort' and param.type_ == Parameter.Type.BOOL:
                self.setBesteffort(param.value)
                
            elif param.name == 'qos_best_effort' and param.type_ == Parameter.Type.BOOL:
                self.setReliable(param.value)

            elif param.name == 'qos_best_effort' and param.type_ == Parameter.Type.BOOL:
                self.setTransientLocal(param.value)

            elif param.name == 'qos_best_effort' and param.type_ == Parameter.Type.BOOL:
                self.setVolatile(param.value)

            elif param.name == 'pong_pub_topic' and param.type_ == Parameter.Type.STRING:
                setPubTopicName(param.value)
                # makePublisher()

            elif param.name == 'pong_sub_topic' and param.type_ == Parameter.Type.STRING:
                setSubTopicName(param.value)
                # makeSubscriber()
            
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    btn_sub = BTN_SUB()
    rclpy.spin(btn_sub)

    btn_sub.destroy_node()
    rclpy.shutdown()

main()

