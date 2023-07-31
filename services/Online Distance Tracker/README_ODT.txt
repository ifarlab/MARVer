Dependencies:
============

 - Eigen version 3.4.0 (available at http://eigen.tuxfamily.org/)
 - libccd (available at https://github.com/danfis/libccd)
 - octomap (optional dependency, available at http://octomap.github.com)
 - FCL version 0.7.0 (available at https://github.com/flexible-collision-library/fcl)
 - rapidxml (https://github.com/Fe-Bell/RapidXML)


	- Note: The odt folder must be added to the catkin_ws/src folder for the ODT service to work. After that, the catkin_make action should be applied.

ROS Noetic:
==========

wget -c https://raw.githubusercontent.com/qboticslabs/ros_install_noetic/master/ros_install_noetic.sh && chmod +x ./ros_install_noetic.sh && ./ros_install_noetic.sh

RVIZ:
====

sudo apt-get install ros-noetic-rviz

ROS OCTOMAP MSG:
===============

sudo apt install ros-noetic-octomap-msgs

RVIZ OCTOMAP VISUALIZATION:
==========================

sudo apt-get install ros-noetic-octomap-rviz-plugins