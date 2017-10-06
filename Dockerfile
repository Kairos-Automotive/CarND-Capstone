# Udacity capstone project dockerfile
FROM ros:kinetic-robot
LABEL maintainer="olala7846@gmail.com"

# Install Dataspeed DBW https://goo.gl/KFSYi1 from binary
# adding Dataspeed server to apt
RUN sh -c 'echo "deb [ arch=amd64 ] http://packages.dataspeedinc.com/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-dataspeed-public.list'
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FF6D3CDA
RUN apt-get update

# setup rosdep
RUN sh -c 'echo "yaml http://packages.dataspeedinc.com/ros/ros-public-'$ROS_DISTRO'.yaml '$ROS_DISTRO'" > /etc/ros/rosdep/sources.list.d/30-dataspeed-public-'$ROS_DISTRO'.list'
RUN rosdep update
RUN apt-get install -y ros-$ROS_DISTRO-dbw-mkz
RUN apt-get upgrade -y
# end installing Dataspeed DBW

# install required ros dependencies
RUN apt-get install -y ros-$ROS_DISTRO-cv-bridge
RUN apt-get install -y ros-$ROS_DISTRO-pcl-ros
RUN apt-get install -y ros-$ROS_DISTRO-image-proc

# socket io
RUN apt-get install -y netbase

# install python packages
RUN apt-get install -y python-pip; pip install --upgrade "pip==0.9.1"
RUN pip install "Flask==0.12.2" "attrdict==2.0.0" "eventlet==0.21.0" "python-socketio==1.8.1" "numpy==1.13.3" "Pillow==4.3.0" "scipy==0.19.1" "keras==1.2.0" "tensorflow==1.0.0"

RUN mkdir /capstone
VOLUME ["/capstone"]
VOLUME ["/root/.ros/log/"]
WORKDIR /capstone/ros
