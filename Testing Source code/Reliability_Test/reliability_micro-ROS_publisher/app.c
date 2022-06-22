#include <stdio.h>
#include <unistd.h>

#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <tutorial_interfaces/msg/reliability_msg.h>

#include <rclc/rclc.h>
#include <rclc/executor.h>

#ifdef ESP_PLATFORM
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#endif

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Aborting.\n",__LINE__,(int)temp_rc);vTaskDelete(NULL);}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Continuing.\n",__LINE__,(int)temp_rc);}}

rcl_publisher_t publisher;
tutorial_interfaces__msg__Reliability_msg msg;
int count = 0;

void timer_callback(rcl_timer_t * timer, int64_t last_call_time)
{
	RCLC_UNUSED(last_call_time);

	msg.count = count;
	if (timer != NULL) {
		RCSOFTCHECK(rcl_publish(&publisher, &msg, NULL));
		// send publisher counter which is equal with expected received message
		printf("pub send seq %d\n", msg.count);
		count++;
	}
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
	RCCHECK(rclc_node_init_with_options(&node, "freertos_int32_publisher", "", &support, &node_ops));

	// create publisher
	rmw_qos_profile_t pub_qos = rmw_qos_profile_default;
	pub_qos.reliability = RMW_QOS_POLICY_RELIABILITY_RELIABLE;
	pub_qos.history = RMW_QOS_POLICY_HISTORY_KEEP_ALL;
	pub_qos.depth = 1000;
	pub_qos.durability = RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL;

	RCCHECK(rclc_publisher_init(
		&publisher,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(tutorial_interfaces, msg, Reliability_msg),
		"freertos_int32_publisher",
		&pub_qos));

	// create timer,
	rcl_timer_t timer;
	const unsigned int timer_timeout = 100.0;		// publisher frequency 1000.0 = 1s
	RCCHECK(rclc_timer_init_default(
		&timer,
		&support,
		RCL_MS_TO_NS(timer_timeout),
		timer_callback));

	// create executor
	rclc_executor_t executor;
	RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
	RCCHECK(rclc_executor_add_timer(&executor, &timer));

	// Create and allocate the messages
	static int32_t memory[30];
	msg.data.capacity = 30;
	msg.data.data = memory;
	msg.data.size = 0;

	for (int32_t i =0; i < 30; i++){	
		msg.data.data[i] = 1;//rand();
		msg.data.size++;
	}

	while(1){
		rclc_executor_spin(&executor);
		usleep(100000);
	}

	// free resources
	RCCHECK(rcl_publisher_fini(&publisher, &node));
	RCCHECK(rcl_node_fini(&node));
	free(msg.data.data);

  	vTaskDelete(NULL);
}
