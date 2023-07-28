#!/usr/bin/env python
from time import time_ns
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('QoS', String, queue_size=1)
    rospy.init_node('ROSQoSPub', anonymous=False)
    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        timeStr = "%s" % time_ns()
        pub.publish(timeStr)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass