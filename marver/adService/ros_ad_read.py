#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16

def callback(data):
    print("ros-ad-read.py:")
    rospy.loginfo(data.data)
    
def listener():
    rospy.init_node('ad_listen', anonymous=False)
    rospy.Subscriber("ad1", Int16, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()