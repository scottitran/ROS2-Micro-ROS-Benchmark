# Testing Usability of ROS2 and Micro-ROS 

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


## Build
To run project demo, this respository need to be cloned.
- Then source code have to be build by using this command:

> `colcon build --packages-select demo`

- then source ROS2 environment and source workplace: 
> `source /opt/ros/foxy/setup.bash`

> `. install/setup.bash`

- Now the program can be run by using launch file:

`ros2 launch demo demo.launch.py`


## Use
Project is: _in progress_ / _complete_ / _no longer being worked on_. If you are no longer working on it, provide reasons why.


## Overview of parameters:
MSG_SIZE: Message sizes of the topic:
- 128 Bytes
- 1 Kilobyte
- 10 Kilobytes
- 100 Kilobytes

PUB_FREQUENCY (Hz):
- Feature to be added 1
- Feature to be added 2

QoS profiles:
- Reliability
- Durability
- History 
- Depth


## Start multi processes
Give credit here.
- This project was inspired by...
- This project was based on [this tutorial](https://www.example.com).
- Many thanks to...

---
## Author 
  - **Tran Tien Cuong** (tran.tien.cuong@bench.com or cuongtdtqb@gmail.com)
