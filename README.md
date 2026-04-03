# my_xtdrone_demo

A simple ROS1 demo package for XTDrone + PX4 + MAVROS.

## Environment

- Ubuntu 24.04 host
- Docker container with ROS1 Noetic
- PX4 SITL
- Gazebo
- MAVROS
- XTDrone

## Current Features

- `auto_mission.py`
  - arm
  - takeoff
  - hover
  - land

## Build

```bash
cd /root/ws/catkin_ws
catkin build
source /root/ws/catkin_ws/devel/setup.bash
