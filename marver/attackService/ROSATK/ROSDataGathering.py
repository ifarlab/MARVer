#!/usr/bin/env python
from time import time_ns
import rospy
from std_msgs.msg import String
from rostopic import ROSTopicHz
import rostopic
import multiprocessing as mp

def talker():
    pub = rospy.Publisher('QoS', String, queue_size=10)
    
    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        timeStr = "%s" % time_ns()
        pub.publish(timeStr)
        rate.sleep()

def listener():
    rt = ROSTopicHz(window_size=-1, filter_expr=None)
    sub = rospy.Subscriber('QoS', String, rt.callback_hz)        
    while not rospy.is_shutdown():
        rospy.loginfo(rt.times)

        


if __name__ == '__main__':
    try:
        rospy.init_node('ROSQoSPub', anonymous=False)

        listenermp = mp.Process(target=listener)
        listenermp.start()
        talkermp = mp.Process(target=talker)
        talkermp.start()
        


        talker()
        listener()
    except rospy.ROSInterruptException:
        pass