# Testing Usability of ROS2 and Micro-ROS Demo

## About : 
This respository contains source code for ROS2 and Micro-ROS applications that were used during the testing for Graduation Assignment at Benchmark. The source code contains three different program languages including Python, C and C++. However, the focus only in Python for ROS2 and C for Micro-ROS. 
Besides, this also include the guidline how to install and setup hardware and sofware requirements which were used in the project. 

## Hardware Components needed
- Jetson Nano
- ESP32 

## Features
List the parameters are used to evaluate:
- Latency
- Memory Consumption
- Scalability
- Reliability


## Getting Started 
Jetson Nano is the hardware used in this project to run ROS2. However, basic OS that Jetson Nano use is Ubuntu 18.04 and it not up to date to run ROS2 foxy. There are three ways to run Ubuntu 20.04 on Jetson Nano. 
- Install [Xubuntu 20.04](https://forums.developer.nvidia.com/t/xubuntu-20-04-focal-fossa-l4t-r32-3-1-custom-image-for-the-jetson-nano/121768) Focal Fossa L4T - a custom image for Jetson Nano running Ubuntu 20.04 
- Upgrade Ubuntu 18.04 to Ubuntu 20.04 by follow [this tutorial](https://qengineering.eu/install-ubuntu-20.04-on-jetson-nano.html)
- Running Ubuntu 20.04 on Docker

After successful install ubuntu, you need to install ROS2 environment by follow [this link](https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html)

## Clone this resposity 
Always source ROS2 environment `source /opt/ros/foxy/setup.bash`.

You need to created a ROS2 workspace to run ROS2 and Micro-ROS application:
```
mkdir -p ~/dev_ws/src
cd ~/dev_ws/src
 ```
Then clone ROS2 and Micro-ROS code from this repository:

> `git clone https://github.com/scottitran/ROS2-Micro-ROS-Benchmark.git`

## Running 
## Build Demo
To run project demo, you need to build demo package using the command:

> `colcon build --packages-select demo`

- then source ROS2 environment and source workplace: 
> `source /opt/ros/foxy/setup.bash`

> `. install/setup.bash`

- Now the program can be run by using launch file:

> `ros2 launch demo demo.launch.py`


## Install and running demo by using Docker
First, you have to install docker in your machine by follow [docker tutorial](https://docs.docker.com/engine/install/)

After finishing clone this repository, you will have Dockerfiles folder. You need to open the terminal in this folder then build docker using this command:

> `docker build -t <name_of_image>:<version>`

Running Docker image in the network host:
`docker run --rm -it --net_host --pid=host <Image_id>` which is check by using this command `docker images`

when you come inside the docker image, you are already inside dev_ws folder. You only need to source workplace: 
> `. install/setup.bash`

Then run the demo program: 

> `ros2 launch demo demo.launch.py`


## Overview and use parameters:
MSG_SIZE: Message sizes of the topic:
- 128 Bytes 
- 1 Kilobyte
- 10 Kilobytes
- 100 Kilobytes

PUB_FREQUENCY (Hz)

QoS profiles:
- Reliability
- Durability
- History 
- Depth

To change parameters value inside ROS2 code when they are running. 

1. Check the param available by: `ros2 param list`
2. Set new param value: `ros2 param set /<publisher_or_subscriber_name> <param_name> <new_values>`
For example in this demo, set new message size = 128B: `ros2 param set /publisher sub_num 30`

## Debug ROS2 Topic in terminal
Below only include topic commands because this project only use _topic_ communication mechanism
- `ros2 topic list`: to see all of topics which are running in the network.
- `ros2 topic echo /<topic_name>`: all of data in message will be shown in terminal 
- `ros2 topic info /<topic_name> -v`: this command will check all the information of topic such as _msg_type_, _QoS_Profile_. Morverover, it also check how many publisher and subscriber are using this topic to communicate
- `ros2 topic hz /<topic_name>`: to check the _min_, _max_ and _average_ value of publisher frequency of this topic
- `ros2 topic bw /<topic_name>`: to check the _min_, _max_ and _average_ value of how much message size used in this topic

---
## Author 
  - **Tran Tien Cuong** (tran.tien.cuong@bench.com or cuongtdtqb@gmail.com)
