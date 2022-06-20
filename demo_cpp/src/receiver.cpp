#include <chrono>
#include <memory>
#include <functional>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

#include "tutorial_interfaces/msg/num.hpp"

using namespace std::chrono_literals;
using std::placeholders::_1;

/* This example creates a subclass of Node and uses std::bind() to register a
 * member function as a callback from the timer. */

class MinimalPublisher : public rclcpp::Node
{
public:
  MinimalPublisher()
  : Node("receiver_cpp")
  {
    publisher_ = this->create_publisher<tutorial_interfaces::msg::Num>("pong_msg", rclcpp::QoS(1000).best_effort());
    subscription_ = this->create_subscription<tutorial_interfaces::msg::Num>("ping_msg", rclcpp::QoS(1000).best_effort(), std::bind(&MinimalPublisher::topic_callback, this, _1));
  }

private: 
  void topic_callback(const tutorial_interfaces::msg::Num::SharedPtr msg) const
  {
    auto message = tutorial_interfaces::msg::Num();
    // RCLCPP_INFO(this->get_logger(), "I heard: '%s'", message.data.c_str());
    message.signal = "ROS2 using C++";
    publisher_->publish(message);
  }
  rclcpp::Publisher<tutorial_interfaces::msg::Num>::SharedPtr publisher_;
  rclcpp::Subscription<tutorial_interfaces::msg::Num>::SharedPtr subscription_;
  // size_t count_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalPublisher>());
  rclcpp::shutdown();
  return 0;
}


