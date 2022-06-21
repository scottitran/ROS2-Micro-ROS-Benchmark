#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>


#include <std_msgs/msg/int32.h>
#include <tutorial_interfaces/msg/reliability_msg.h>

#include <stdio.h>
#include <unistd.h>

#ifdef ESP_PLATFORM
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#endif

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Aborting.\n",__LINE__,(int)temp_rc);vTaskDelete(NULL);}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Continuing.\n",__LINE__,(int)temp_rc);}}

rcl_subscription_t subscriber;
tutorial_interfaces__msg__Reliability_msg msg;

// create counter at subscriber = actually receive message
int count = 0;

void subscription_callback(const void * msgin)
{
	const tutorial_interfaces__msg__Reliability_msg * msg = (const tutorial_interfaces__msg__Reliability_msg *)msgin;
	printf("msg: %d, count: %d\n", msg->count, count);
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
	RCCHECK(rclc_node_init_with_options(&node, "int32_subscriber_rclc", "", &support, &node_ops));

	// create subscriber
	rmw_qos_profile_t sub_qos = rmw_qos_profile_default;
	sub_qos.reliability = RMW_QOS_POLICY_RELIABILITY_RELIABLE;
	sub_qos.history = RMW_QOS_POLICY_HISTORY_KEEP_ALL;
	sub_qos.durability = RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL;
	sub_qos.depth = 1000;

	RCCHECK(rclc_subscription_init(
		&subscriber,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(tutorial_interfaces, msg, Reliability_msg),
		"freertos_int32_publisher",
		&sub_qos));

	// create executor
	rclc_executor_t executor;
	RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
	RCCHECK(rclc_executor_add_subscription(&executor, &subscriber, &msg, &subscription_callback, ON_NEW_DATA));

	// Create and allocate the messages
	static int32_t memory[30];
	msg.data.capacity = 30;
	msg.data.data = memory;
	msg.data.size = 0;

	// rclc_executor_spin(&executor);
	while(1){
		rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
		usleep(100000);
	}

	// free resources
	RCCHECK(rcl_subscription_fini(&subscriber, &node));
	RCCHECK(rcl_node_fini(&node));
	free(msg.data.data);
	
	vTaskDelete(NULL);
}
