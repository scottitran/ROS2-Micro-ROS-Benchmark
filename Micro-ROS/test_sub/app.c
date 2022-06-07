#include <stdio.h>
#include <unistd.h>
#include <time.h>

#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <std_msgs/msg/int32.h>
#include <std_msgs/msg/string.h>

#include <std_msgs/msg/int32_multi_array.h>
#include <std_msgs/msg/float32_multi_array.h>
#include <tutorial_interfaces/msg/num.h>

#include <rclc/rclc.h>
#include <rclc/executor.h>

#ifdef ESP_PLATFORM
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#endif

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Aborting.\n",__LINE__,(int)temp_rc);vTaskDelete(NULL);}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Continuing.\n",__LINE__,(int)temp_rc);}}

// #define ARRAY_LEN 1000

// bool condition = false;

rcl_publisher_t publisher;
rcl_subscription_t subscriber;

// std_msgs__msg__Int32MultiArray msg_sent;
// std_msgs__msg__Int32MultiArray msg_receive;
tutorial_interfaces__msg__Num msg;
int count = 0;

void subscription_callback(const void * msgin)
{
	const tutorial_interfaces__msg__Num * msg = (const tutorial_interfaces__msg__Num *)msgin;
	RCSOFTCHECK(rcl_publish(&publisher, (const void*)msg, NULL));
	// struct timespec ts;
	// clock_gettime(CLOCK_REALTIME, &ts);
	printf("msg: %d, count: %d\n", msg->count, count);
	// printf("time: %ld, msg: %d, count: %d\n", ts.tv_nsec, msg->count, count);
	count++;
}

void appMain(void * arg)
{
	rcl_allocator_t allocator = rcl_get_default_allocator();
	rclc_support_t support;

	// create init_options
	RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

	// create node
	rcl_node_t node;
	rcl_node_options_t node_ops = rcl_node_get_default_options();
	node_ops.domain_id = 4;
	RCCHECK(rclc_node_init_with_options(&node, "M5STACK", "", &support, &node_ops));

	// create publisher
	rmw_qos_profile_t pub_qos = rmw_qos_profile_default;
	pub_qos.reliability = RMW_QOS_POLICY_RELIABILITY_RELIABLE;
	pub_qos.history = RMW_QOS_POLICY_HISTORY_KEEP_ALL;
	// pub_qos.depth = 1000;
	pub_qos.durability = RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL;

	RCCHECK(rclc_publisher_init(
		&publisher,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(tutorial_interfaces, msg, Num),
		"pong_msg",
		&pub_qos));

	// create subscriber
	rmw_qos_profile_t sub_qos = rmw_qos_profile_default;
	sub_qos.reliability = RMW_QOS_POLICY_RELIABILITY_RELIABLE;
	sub_qos.history = RMW_QOS_POLICY_HISTORY_KEEP_ALL;
	sub_qos.durability = RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL;
	// sub_qos.depth = 1000;

	RCCHECK(rclc_subscription_init(
		&subscriber,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(tutorial_interfaces, msg, Num),
		"ping_msg",
		&sub_qos));

	// create executor
	rclc_executor_t executor;
	RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
	RCCHECK(rclc_executor_add_subscription(&executor, &subscriber, &msg, &subscription_callback, ON_NEW_DATA));
	
	msg.data.capacity = 2498;
	msg.data.data = (int32_t*) malloc(msg.data.capacity * sizeof(int32_t));
	msg.data.size = 0;

	rclc_executor_spin(&executor);
	// while(1){
	// 	rclc_executor_spin(&executor);
	// 	// usleep(100000);
	// }

	free(msg.data.data);

	// free resources
	RCCHECK(rcl_publisher_fini(&publisher, &node));
	RCCHECK(rcl_subscription_fini(&subscriber, &node));
	RCCHECK(rcl_node_fini(&node));

  	vTaskDelete(NULL);
}
