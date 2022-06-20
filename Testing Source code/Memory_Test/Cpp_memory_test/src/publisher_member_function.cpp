////////***************************** Print Hello world string program *****************************//////////////////////////////////////
/////////////**************** Uncommand to use ****************////////////////////////////

// Your First C++ Program

#include <iostream>
using namespace std;
 
int main() {
   while (true) {
      cout << "hello" << endl;
   }
}

/////////////////////////////////////////////////////////////////////////////////

/////////////**************** Only Create Node ****************////////////////////////////
/////////////**************** Uncommand to use ****************////////////////////////////

// #include "rclcpp/rclcpp.hpp"

// int main(int argc, char **argv)
// {
//   rclcpp::init(argc, argv);
//   auto node = std::make_shared<rclcpp::Node>("my_node_name");
//   rclcpp::spin(node);
//   rclcpp::shutdown();
//   return 0;
// }


///////////////////////////////////////////////////////////////////////////////
/////////////**************** Create different Publishers and Subscribers with different Topics ****************////////////////////////////
/////////////**************** Uncommand to use ****************////////////////////////////

// #include <chrono>
// #include <functional>
// #include <memory>
// #include <string>

// #include "rclcpp/rclcpp.hpp"
// #include "std_msgs/msg/string.hpp"

// using namespace std::chrono_literals;
// using std::placeholders::_1;
// /* This example creates a subclass of Node and uses std::bind() to register a
// * member function as a callback from the timer. */

// class MinimalPublisher : public rclcpp::Node
// {
//   public:
//     MinimalPublisher()
//     : Node("minimal_publisher")
//     {
//       publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
//       // publisher1 = this->create_publisher<std_msgs::msg::String>("topic1", 10);
//       // publisher2 = this->create_publisher<std_msgs::msg::String>("topic2", 10);
//       // publisher3 = this->create_publisher<std_msgs::msg::String>("topic3", 10);
//       // publisher4 = this->create_publisher<std_msgs::msg::String>("topic4", 10);
//       // publisher5 = this->create_publisher<std_msgs::msg::String>("topic5", 10);
//       // publisher6 = this->create_publisher<std_msgs::msg::String>("topic6", 10);
//       // publisher7 = this->create_publisher<std_msgs::msg::String>("topic7", 10);
//       // publisher8 = this->create_publisher<std_msgs::msg::String>("topic8", 10);
//       // publisher9 = this->create_publisher<std_msgs::msg::String>("topic9", 10);
      
//       subscription_ = this->create_subscription<std_msgs::msg::String>("topic", 10, std::bind(&MinimalPublisher::topic_callback, this, _1));
//       // subscription1 = this->create_subscription<std_msgs::msg::String>("topic1", 10, std::bind(&MinimalPublisher::topic_callback, this, _1));
//       // subscription2 = this->create_subscription<std_msgs::msg::String>("topic2", 10, std::bind(&MinimalPublisher::topic_callback, this, _1));
//       // subscription3 = this->create_subscription<std_msgs::msg::String>("topic3", 10, std::bind(&MinimalPublisher::topic_callback, this, _1));
//       // subscription4 = this->create_subscription<std_msgs::msg::String>("topic4", 10, std::bind(&MinimalPublisher::topic_callback, this, _1));
//       // subscription5 = this->create_subscription<std_msgs::msg::String>("topic5", 10, std::bind(&MinimalPublisher::topic_callback, this, _1));
//       // subscription6 = this->create_subscription<std_msgs::msg::String>("topic6", 10, std::bind(&MinimalPublisher::topic_callback, this, _1));
//       // subscription7 = this->create_subscription<std_msgs::msg::String>("topic7", 10, std::bind(&MinimalPublisher::topic_callback, this, _1));
//       // subscription8 = this->create_subscription<std_msgs::msg::String>("topic8", 10, std::bind(&MinimalPublisher::topic_callback, this, _1));
//       // subscription9 = this->create_subscription<std_msgs::msg::String>("topic9", 10, std::bind(&MinimalPublisher::topic_callback, this, _1));

//       timer_ = this->create_wall_timer(
//       10ms, std::bind(&MinimalPublisher::timer_callback, this));
//     }

//   private:
//     void timer_callback()
//     {
//       auto message = std_msgs::msg::String();
//       message.data = "Hello, world! ";
//       RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
//       publisher_->publish(message);
//       // publisher1->publish(message);
//       // publisher2->publish(message);
//       // publisher3->publish(message);
//       // publisher4->publish(message);
//       // publisher5->publish(message);
//       // publisher6->publish(message);
//       // publisher7->publish(message);
//       // publisher8->publish(message);
//       // publisher9->publish(message);

//     }

//     void topic_callback(const std_msgs::msg::String::SharedPtr msg) const
//     {
//       RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());
//     }

//     rclcpp::TimerBase::SharedPtr timer_;
//     rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
//     // rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher1;
//     // rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher2;
//     // rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher3;
//     // rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher4;
//     // rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher5;
//     // rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher6;
//     // rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher7;
//     // rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher8;
//     // rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher9;

//    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
//   //  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription1;
//   //  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription2;
//   //  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription3;
//   //  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription4;
//   //  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription5;
//   //  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription6;
//   //  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription7;
//   //  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription8;
//   //  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription9;

// };

// int main(int argc, char * argv[])
// {
//   rclcpp::init(argc, argv);
//   rclcpp::spin(std::make_shared<MinimalPublisher>());
//   rclcpp::shutdown();
//   return 0;
}

