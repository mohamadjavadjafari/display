cmake_minimum_required(VERSION 3.0.2)
project(display)

find_package(catkin REQUIRED COMPONENTS
  OpenCV
  rospy
  sensor_msgs
  std_msgs
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)
