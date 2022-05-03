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

#define RED_LED 25
#define GREEN_LED 26

#define ARRAY_LEN 500

rcl_publisher_t publisher;
rcl_subscription_t subscriber;
std_msgs__msg__String msg_req;
std_msgs__msg__String msg_res;
// char test_array[ARRAY_LEN];
int count =0;

void timer_callback(rcl_timer_t * timer, int64_t last_call_time)
{
	RCLC_UNUSED(last_call_time);
	if (timer != NULL) {
		sprintf(msg_req.data.data, "Hello Cuong, the most handsome guy in the world!!! #%d", count++);
		msg_req.data.size = strlen(msg_req.data.data);
		RCSOFTCHECK(rcl_publish(&publisher, &msg_req, NULL));
		gpio_set_level(RED_LED,1);
	}
}

void subscription_callback(const void * msgin)
{
	const std_msgs__msg__String * msg = (const std_msgs__msg__String *)msgin;
	gpio_set_level(RED_LED,0);
}

void appMain(void * arg)
{
	gpio_pad_select_gpio(RED_LED);
	gpio_set_direction(RED_LED, GPIO_MODE_OUTPUT);
	gpio_pad_select_gpio(GREEN_LED);
	gpio_set_direction(GREEN_LED, GPIO_MODE_OUTPUT);

	gpio_set_level(RED_LED,0);
	gpio_set_level(GREEN_LED,0);

	rcl_allocator_t allocator = rcl_get_default_allocator();
	rclc_support_t support;

	// create init_options
	RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

	// create node
	rcl_node_t node;
	RCCHECK(rclc_node_init_default(&node, "ESP32", "", &support));

	// create publisher
	RCCHECK(rclc_publisher_init_default(
		&publisher,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String),
		"ping_msg"));

	// create subscriber
	RCCHECK(rclc_subscription_init_default(
		&subscriber,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String),
		"pong_msg"));

	// create timer,
	rcl_timer_t timer;
	const unsigned int timer_timeout = 1000;
	RCCHECK(rclc_timer_init_default(
		&timer,
		&support,
		RCL_MS_TO_NS(timer_timeout),
		timer_callback));

	// create executor
	rclc_executor_t executor;
	RCCHECK(rclc_executor_init(&executor, &support.context, 2, &allocator));
	RCCHECK(rclc_executor_add_timer(&executor, &timer));
	RCCHECK(rclc_executor_add_subscription(&executor, &subscriber, &msg_res, &subscription_callback, ON_NEW_DATA));

	// msg_res.data = 0;
	msg_req.data.data = (char * ) malloc(ARRAY_LEN * sizeof(char));
	msg_req.data.size =0;
	msg_req.data.capacity = ARRAY_LEN;

	msg_res.data.data = (char * ) malloc(ARRAY_LEN * sizeof(char));
	msg_res.data.size =0;
	msg_res.data.capacity = ARRAY_LEN;

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
