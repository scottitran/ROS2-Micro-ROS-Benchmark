#include <stdio.h>
#include <unistd.h>

#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <std_msgs/msg/int32.h>

#include <rclc/rclc.h>
#include <rclc/executor.h>

#ifdef ESP_PLATFORM
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#endif

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Aborting.\n",__LINE__,(int)temp_rc);vTaskDelete(NULL);}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Continuing.\n",__LINE__,(int)temp_rc);}}

rcl_publisher_t publisher;
rcl_publisher_t publisher1;
rcl_publisher_t publisher2;
rcl_publisher_t publisher3;
rcl_publisher_t publisher4;
rcl_subscription_t subscriber;
rcl_subscription_t subscriber1;
rcl_subscription_t subscriber2;
rcl_subscription_t subscriber3;
rcl_subscription_t subscriber4;

std_msgs__msg__Int32 msg;


void timer_callback(rcl_timer_t * timer, int64_t last_call_time)
{
	(void)	last_call_time;
	(void)	timer;

	if (timer != NULL) {
		RCSOFTCHECK(rcl_publish(&publisher, &msg, NULL));
		RCSOFTCHECK(rcl_publish(&publisher1, &msg, NULL));
		RCSOFTCHECK(rcl_publish(&publisher2, &msg, NULL));
		RCSOFTCHECK(rcl_publish(&publisher3, &msg, NULL));
		RCSOFTCHECK(rcl_publish(&publisher4, &msg, NULL));
	}
}

void subscription_callback(const void * msgin)
{
	const std_msgs__msg__Int32 * msg = (const std_msgs__msg__Int32 *)msgin;
}

void appMain(void * arg)
{
	rcl_allocator_t allocator = rcl_get_default_allocator();
	rclc_support_t support;

	// create init_options
	RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

	// create node
	rcl_node_t node;
	RCCHECK(rclc_node_init_default(&node, "freertos_int32_publisher", "", &support));

	RCCHECK(rclc_publisher_init_default(
		&publisher,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
		"freertos_int32_publisher"));

	RCCHECK(rclc_publisher_init_default(
		&publisher1,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
		"freertos_int32_publisher1"));
	RCCHECK(rclc_publisher_init_default(
		&publisher2,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
		"freertos_int32_publisher2"));

	RCCHECK(rclc_publisher_init_default(
		&publisher3,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
		"freertos_int32_publisher3"));

	RCCHECK(rclc_publisher_init_default(
		&publisher4,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
		"freertos_int32_publisher4"));

	RCCHECK(rclc_subscription_init_default(
		&subscriber,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
		"freertos_int32_publisher"));

	RCCHECK(rclc_subscription_init_default(
		&subscriber1,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
		"freertos_int32_publisher1"));

	RCCHECK(rclc_subscription_init_default(
		&subscriber2,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
		"freertos_int32_publisher2"));

	RCCHECK(rclc_subscription_init_default(
		&subscriber3,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
		"freertos_int32_publisher3"));

	RCCHECK(rclc_subscription_init_default(
		&subscriber4,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
		"freertos_int32_publisher4"));


	// create timer,
	rcl_timer_t timer;
	RCCHECK(rclc_timer_init_default(
		&timer,
		&support,
		RCL_MS_TO_NS(1000),
		timer_callback));

	// create executor
	rclc_executor_t executor;
	RCCHECK(rclc_executor_init(&executor, &support.context, 6, &allocator));
	RCCHECK(rclc_executor_add_timer(&executor, &timer));
	RCCHECK(rclc_executor_add_subscription(&executor, &subscriber, &msg, &subscription_callback, ON_NEW_DATA));
	RCCHECK(rclc_executor_add_subscription(&executor, &subscriber1, &msg, &subscription_callback, ON_NEW_DATA));
	RCCHECK(rclc_executor_add_subscription(&executor, &subscriber2, &msg, &subscription_callback, ON_NEW_DATA));
	RCCHECK(rclc_executor_add_subscription(&executor, &subscriber3, &msg, &subscription_callback, ON_NEW_DATA));
	RCCHECK(rclc_executor_add_subscription(&executor, &subscriber4, &msg, &subscription_callback, ON_NEW_DATA));

	rclc_executor_spin(&executor);

	// free resources
	RCCHECK(rcl_publisher_fini(&publisher, &node));
	RCCHECK(rcl_publisher_fini(&publisher1, &node));
	RCCHECK(rcl_publisher_fini(&publisher2, &node));
	RCCHECK(rcl_publisher_fini(&publisher3, &node));
	RCCHECK(rcl_publisher_fini(&publisher4, &node));
	RCCHECK(rcl_subscription_fini(&subscriber, &node));
	RCCHECK(rcl_subscription_fini(&subscriber1, &node));
	RCCHECK(rcl_subscription_fini(&subscriber2, &node));
	RCCHECK(rcl_subscription_fini(&subscriber3, &node));
	RCCHECK(rcl_subscription_fini(&subscriber4, &node));
	RCCHECK(rcl_node_fini(&node));
  	vTaskDelete(NULL);
}
