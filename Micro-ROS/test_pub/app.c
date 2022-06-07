#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <std_msgs/msg/int32.h>
#include <std_msgs/msg/string.h>
#include <std_msgs/msg/int32_multi_array.h>
#include <std_msgs/msg/float32_multi_array.h>
#include <tutorial_interfaces/msg/num.h>

#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <rclc_parameter/rclc_parameter.h>

#include <driver/gpio.h>

#ifdef ESP_PLATFORM
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#endif

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Aborting.\n",__LINE__,(int)temp_rc);vTaskDelete(NULL);}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Continuing.\n",__LINE__,(int)temp_rc);}}

#define RED_LED 25

rclc_parameter_server_t param_server;
rcl_timer_t timer;
rcl_publisher_t publisher;
rcl_subscription_t subscriber;

tutorial_interfaces__msg__Num msg_sent;
tutorial_interfaces__msg__Num msg_receive;

const char * publish_rate = "publish_rate";
double publish_rate_value = 100.0;

const char * msg_size = "msg_size";
int MSG = 30;

int count = 0;

void timer_callback(rcl_timer_t * timer, int64_t last_call_time)
{
	(void)	last_call_time;
	(void)	timer;

	msg_sent.count = count;
	if (timer != NULL) {

		RCSOFTCHECK(rcl_publish(&publisher, &msg_sent, NULL));
		gpio_set_level(RED_LED,1);
		
		printf("pub send seq %d\n", msg_sent.count);
		count++;
	}
}

void parameter_callback(Parameter * param)
{
	if (param == NULL){
		return;
	}

	if (strcmp(param->name.data, "publish_rate") == 0){
		switch (param ->value.type)
		{
			case RCLC_PARAMETER_DOUBLE:
				RCSOFTCHECK(rcl_timer_exchange_period(&timer, RCL_MS_TO_NS(param->value.double_value), &publish_rate_value));
				break;
			
			default:
				break;
		}
	}

	if (strcmp(param->name.data, "msg_size") == 0){
		switch (param ->value.type)
		{
			case RCLC_PARAMETER_INT:
				MSG = param->value.integer_value;
				break;
			
			default:
				break;
		}
	}
}

void subscription_callback(const void * msgin)
{
	const tutorial_interfaces__msg__Num * msg = (const tutorial_interfaces__msg__Num *)msgin;
	gpio_set_level(RED_LED,0);
}

void appMain(void * arg)
{
	gpio_pad_select_gpio(RED_LED);
	gpio_set_direction(RED_LED, GPIO_MODE_OUTPUT);

	gpio_set_level(RED_LED,0);

	rcl_allocator_t allocator = rcl_get_default_allocator();
	rclc_support_t support;

	// create init_options
	RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

	// create node
	rcl_node_t node;
	rcl_node_options_t node_ops = rcl_node_get_default_options();
	node_ops.domain_id = 4;
	RCCHECK(rclc_node_init_with_options(&node, "ESP32", "", &support, &node_ops));

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
		"ping_msg",
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
		"pong_msg",
		&sub_qos));

	// create parameter service
	rclc_parameter_server_init_default(&param_server, &node);

	// create timer,
	RCCHECK(rclc_timer_init_default(
		&timer,
		&support,
		RCL_MS_TO_NS(publish_rate_value),
		timer_callback));

	// create executor
	rclc_executor_t executor;
	RCCHECK(rclc_executor_init(&executor, &support.context, RCLC_PARAMETER_EXECUTOR_HANDLES_NUMBER + 2, &allocator));
	RCCHECK(rclc_executor_add_parameter_server(&executor, &param_server, parameter_callback));
	RCCHECK(rclc_executor_add_timer(&executor, &timer));
	RCCHECK(rclc_executor_add_subscription(&executor, &subscriber, &msg_receive, &subscription_callback, ON_NEW_DATA));

	// add parameters
	rcl_ret_t rc = rclc_add_parameter(&param_server, publish_rate, RCLC_PARAMETER_DOUBLE);
	rcl_ret_t rc1 = rclc_add_parameter(&param_server, msg_size, RCLC_PARAMETER_INT);

	rc = rclc_parameter_set_double(&param_server, publish_rate, publish_rate_value);
	rc1 = rclc_parameter_set_int(&param_server, msg_size, MSG);

	rc = rclc_parameter_get_double(&param_server, publish_rate, &publish_rate_value);
	rc1 = rclc_parameter_get_int(&param_server, msg_size, &MSG);

////////////////////////////////////////////////////
	msg_sent.data.capacity = MSG;
	msg_sent.data.data = (int32_t*) malloc(msg_sent.data.capacity * sizeof(int32_t));
	msg_sent.data.size = 0;

	for (int32_t i =0; i < MSG; i++){	
		msg_sent.data.data[i] = 1;//rand();
		msg_sent.data.size++;
	}

	msg_receive.data.capacity = MSG;
	msg_receive.data.data = (int32_t*) malloc(msg_receive.data.capacity * sizeof(int32_t));
	msg_receive.data.size = 0;

	rclc_executor_prepare(&executor);

	rclc_executor_spin(&executor);

	// free resources
	free(msg_sent.data.data);
	free(msg_receive.data.data);
	RCCHECK(rcl_publisher_fini(&publisher, &node));
	RCCHECK(rcl_subscription_fini(&subscriber, &node));
	RCCHECK(rclc_parameter_server_fini(&param_server, &node));
	RCCHECK(rcl_node_fini(&node));

  	vTaskDelete(NULL);
}