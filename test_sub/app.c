#include <stdio.h>
#include <unistd.h>

#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <std_msgs/msg/int32.h>
#include <std_msgs/msg/string.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

#include <driver/gpio.h>

#ifdef ESP_PLATFORM
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#endif

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Aborting.\n",__LINE__,(int)temp_rc);vTaskDelete(NULL);}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Continuing.\n",__LINE__,(int)temp_rc);}}

#define ARRAY_LEN 500

bool condition = false;

rcl_publisher_t publisher;
rcl_subscription_t subscriber;
std_msgs__msg__String send_msg;
std_msgs__msg__String recv_msg;

// void timer_callback(rcl_timer_t * timer, int64_t last_call_time)
// {
// 	RCLC_UNUSED(last_call_time);
// 	if (timer != NULL) {
// 		if (condition == true){
// 			sprintf(send_msg.data.data, "Hello Cuong!!!");
// 			send_msg.data.size = strlen(send_msg.data.data);
// 			RCSOFTCHECK(rcl_publish(&publisher, &send_msg, NULL));
// 			printf("Sent: %s\n", send_msg.data.data);
// 		}
// 	}
// }

void subscription_callback(const void * msgin)
{
	const std_msgs__msg__Int32 * msg = (const std_msgs__msg__Int32 *)msgin;
	// printf("Received: %d\n", msg->data);
	// // condition = true;
	// sprintf(recv_msg.data.data, "Hello Cuong Dep Trai Nhat The Gioi!!!");
	// recv_msg.data.size = strlen(recv_msg.data.data);
	// if (strcmp(recv_msg.data.data, msg->data) != 0){
	RCSOFTCHECK(rcl_publish(&publisher, (const void*)msg, NULL));
	// }
	// printf("Sent: %s\n", send_msg.data.data);
}

void appMain(void * arg)
{
	rcl_allocator_t allocator = rcl_get_default_allocator();
	rclc_support_t support;

	// create init_options
	RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

	// create node
	rcl_node_t node;
	RCCHECK(rclc_node_init_default(&node, "M5STACK", "", &support));

	// create publisher
	RCCHECK(rclc_publisher_init_default(
		&publisher,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String),
		"pong_msg"));

	// create subscriber
	RCCHECK(rclc_subscription_init_default(
		&subscriber,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String),
		"ping_msg"));

	// create executor
	rclc_executor_t executor;
	RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
	// RCCHECK(rclc_executor_add_timer(&executor, &timer));
	RCCHECK(rclc_executor_add_subscription(&executor, &subscriber, &recv_msg, &subscription_callback, ON_NEW_DATA));

	recv_msg.data.data = (char * ) malloc(ARRAY_LEN * sizeof(char));
	recv_msg.data.size =0;
	recv_msg.data.capacity = ARRAY_LEN;
	
	while(1){
		rclc_executor_spin(&executor);
		// usleep(100000);
	}

	// free resources
	RCCHECK(rcl_publisher_fini(&publisher, &node));
	RCCHECK(rcl_subscription_fini(&subscriber, &node));
	RCCHECK(rcl_node_fini(&node));

  	vTaskDelete(NULL);
}
