#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
import random

def talker():
    rospy.init_node('adMaster', anonymous=False)
    pub = rospy.Publisher('ad1', Float32, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():

        pub.publish(90 + random.randint(0, 100)/10)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        print('fail')
        pass