FROM ubuntu:20.04

# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# install packages 
RUN apt update && apt install -y curl gnupg2 lsb-release
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg

# setup sources.list
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y ros-foxy-desktop
RUN DEBIAN_FRONTEND=noninteractive apt install -y cmake
RUN apt --fix-missing update
RUN apt install -y git-all

WORKDIR /root/dev_ws
RUN git clone https://github.com/scottitran/src.git
# WORKDIR /root/dev_ws

RUN apt-get install python3-rosdep -y
RUN rosdep init
RUN rosdep update
RUN apt-get install -y vim nano
RUN apt install python3-colcon-common-extensions -y

RUN echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc
RUN rosdep install -i --from-path src --rosdistro foxy -y

RUN colcon build
