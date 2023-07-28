#!/usr/bin/env python
from time import time_ns
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('ATK', String, queue_size=1)
    rospy.init_node('AttackPub', anonymous=False)
    print("Enter attack params(s): Type Countdown Duration Volume")
    while not rospy.is_shutdown():
        atkStr = input("=>")
        pub.publish(atkStr)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass