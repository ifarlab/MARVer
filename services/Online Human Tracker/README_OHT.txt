Dependencies:
============

 - Eigen version 3.4.0 (available at http://eigen.tuxfamily.org/)
 - libccd (available at https://github.com/danfis/libccd)
 - FCL version 0.7.0 (available at https://github.com/flexible-collision-library/fcl)
 - Nuitrack (https://github.com/3DiVi/nuitrack-sdk/blob/master/doc/Install.md)
 - rapidxml (https://github.com/Fe-Bell/RapidXML)


	- Note: The oht folder must be added to the catkin_ws/src folder for the OHT service to work. After that, the catkin_make action should be applied.

ROS Noetic:
==========

wget -c https://raw.githubusercontent.com/qboticslabs/ros_install_noetic/master/ros_install_noetic.sh && chmod +x ./ros_install_noetic.sh && ./ros_install_noetic.sh

RVIZ:
====

sudo apt-get install ros-noetic-rviz

Nuitrack Ubuntu Install:
=======================

sudo dpkg -i nuitrack-ubuntu-amd64.deb

confirm environment variables set correctly:
-------------------------------------------

echo $NUITRACK_HOME (should be /usr/etc/nuitrack)
echo $LD_LIBRARY_PATH (should include /usr/local/lib/nuitrack)

If environment variables are not set, to set:
--------------------------------------------

export NUITRACK_HOME=/usr/etc/nuitrack
export LD_LIBRARY_PATH=/usr/local/lib/nuitrack

Lastly, run Nuitrack and activate Nuitrack with activation key.
--------------------------------------------------------------
(For activation, the camera must be connected to the computer.)


Nuitrack SDK Install:
====================

In home directory:
-----------------

mkdir sdk
cd sdk
git clone https://github.com/3DiVi/nuitrack-sdk.git
mv nuitrack-sdk NuitrackSDK 

