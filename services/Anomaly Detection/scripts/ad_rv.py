#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from adservice.msg import adrv

adRes = 'False'
aState = 'False'

def anomalyState(data):
    global adRes
    adRes = data.data
    
def attackStateCB(data):
    global aState
    aState = data.data

def listener():
    global adRes, aState
 
    rospy.init_node('anomalyDetectionRV', anonymous=False)

    rospy.Subscriber('adResult', String, anomalyState)
    rospy.Subscriber('attackState', String, attackStateCB)

    rate = rospy.Rate(1)
    pub=rospy.Publisher('adRVComparision', adrv, queue_size=10)
    while rospy.is_shutdown:
        msg = adrv()
        if adRes == 'True': msg.adResult = 1
        elif adRes == 'False': msg.adResult = 0
        if aState == 'True': msg.attackState = 1
        elif aState == 'False': msg.attackState = 0
        pub.publish(msg)
        rate.sleep()
        
    


    

if __name__ == '__main__':
    listener()
