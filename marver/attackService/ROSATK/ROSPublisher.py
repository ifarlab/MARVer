#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist 


def callback(data):

    global msg
    if data.data=="Unknown":

        pub_ = rospy.Publisher('cmd_vel', Twist)
        rospy.loginfo("Classifiers output: %s in unknown" % data.data)
        msg.linear.x = 2
        msg.linear.y = 0
        msg.linear.x = 0
        msg.angular.z = 0
        speed = 0.4 
        rospy.loginfo("checking for cmd" + str(msg.linear))
        pub_.publish(msg)

    elif data.data=="Check":
        rospy.loginfo("Classifiers output: %s in check" % data.data)
    else:      
        rospy.loginfo("Classifiers output: %s and not unknown or check" % data.data)


def listener():

     global msg
     rospy.init_node('listener', anonymous=True)
     msg = Twist()
     rospy.Subscriber("chatter", String, callback)
     rospy.spin()


if __name__ == '__main__':


     listener()