#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Float32
from nav_msgs.msg import Odometry


lst_ros = []


def callback(data):
    global lst_ros, lst_csv
    lst_ros.append(data)

def avgPublisher():
    global lst_ros, lst_csv, normal
    rate = rospy.Rate(1)
    pub = rospy.Publisher('traffic', Float32, queue_size=10)
    while True:
        msg = float(2*len(lst_ros))
        lst_ros.clear()
        pub.publish(msg)
        rate.sleep()


def listener():
    rospy.init_node('ROSQoSSub', anonymous=False)

    rospy.Subscriber("odom", Odometry, callback)

    avgPublisher()
    
    

if __name__ == '__main__':
    listener()
