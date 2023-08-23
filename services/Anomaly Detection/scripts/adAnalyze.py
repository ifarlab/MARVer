#!/usr/bin/env python
import rospy
from adservice.msg import adrv


msgCount = 0
attackMsgCount = 0
faultDedectedMsgCount = 0

def callback(msg):
    global msgCount, attackMsgCount, faultDedectedMsgCount

    msgCount += 1
    if msg.attackState:
        attackMsgCount += 1
        if msg.adResult:
            faultDedectedMsgCount += 1

    print('Messages:', msgCount)
    print('Messages While Attacking:', attackMsgCount)
    print('Anomaly Dedected Messages:', faultDedectedMsgCount)
    if attackMsgCount != 0:
        print('Detection Ratio:', faultDedectedMsgCount/attackMsgCount)

def listener():
 
    rospy.init_node('anomalyAnalyzer', anonymous=False)

    rospy.Subscriber('adRVComparision', adrv, callback)

    rospy.spin()


        

if __name__ == '__main__':
    listener()
