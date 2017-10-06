# Self Driving Car Engineer Nanodegree -- Capstone project

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/79ddbbe506054e43859247d9fd0b11b5)](https://www.codacy.com/app/Kairos-Automotive/carla-brain?utm_source=github.com&utm_medium=referral&utm_content=Kairos-Automotive/carla-brain&utm_campaign=badger) 
[![Build Status](https://travis-ci.org/Kairos-AutomotAive/carla-braAin.svg?branch=master)](https://travis-ci.org/Kairos-Automotive/carla-brain) 
[![Docker Status](https://dockerbuildbadges.quelltext.eu/status.svg?organization=kairosautomotive&repository=carla-brain)](https://hub.docker.com/r/kairosautomotive/carla-brain/) 

This is the project repo for the final project of the Udacity
Self-Driving Car Nanodegree: Programming a Real Self-Driving Car.

## Team Members

This repository is maintained by the following:
- [Alexey Simonov](https://github.com/asimonov)
- [Victor Guerra](https://github.com/vguerra)
- [Ralf Beier](https://github.com/avrabe)
-
-


## Workflow

Please see [wiki](wiki) for complete description.


## Installation

We use ROS Kinetic on Ubuntu 16.04

### Native Install

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus.
 [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).

The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow [these instructions](http://wiki.ros.org/kinetic/Installation/Ubuntu) to install ROS
* Install [Dataspeed DBW SDK](https://bitbucket.org/DataspeedInc/dbw_mkz_ros).
  On a workstation that already has ROS installed use this option:
  [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)

### Docker Install
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t kairosautomotive/carla-brain:latest
```

or pull the latest docker container from dockerhub
```bash
docker pull kairosautomotive/carla-brain:latest
```

Run the docker file
```bash
docker run -p 127.0.0.1:4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it kairosautomotive/carla-brain
```

### Simulator

Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases/tag/v1.2)


## Build and Run in Simulator

1. Clone the project repository
```bash
git clone https://github.com/Kairos-Automotive/carla-brain.git
```

2. Install python dependencies
```bash
cd carla-brain
pip install -r requirements.txt
```

3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```

4. Run the simulator


## Test with ROS bags from real car

1. Download [training bag](https://drive.google.com/file/d/0B2_h37bMVw3iYkdJTlRSUlJIamM/view?usp=sharing)
that was recorded on the Udacity self-driving car (a bag demonstraing the correct
predictions in autonomous mode can be found
[here](https://drive.google.com/open?id=0B2_h37bMVw3iT0ZEdlF4N01QbHc))

2. Unzip the file
```bash
unzip traffic_light_bag_files.zip
```

3. Play the bag file
```bash
rosbag play -l traffic_light_bag_files/loop_with_traffic_light.bag
```

4. Launch your project in site mode
```bash
cd carla-brain/ros
roslaunch launch/site.launch
```

5. Confirm that traffic light detection works on real life images

