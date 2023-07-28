#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Int16
import time
import multiprocessing as mp
import os
import subprocess
import signal

curTime = time.time()

def subsBomb(vol):
    os.system('python SubscriberBomb.py ' + str(vol))

def tcpFlood(secs):
    atck = subprocess.Popen(['sudo', 'python', 'TCP_flood.py'])
    time.sleep(secs -1)
    atck.kill()
    


def callback(data):
    str = data.data
    command = str.split(" ")

    pub = rospy.Publisher('AttackState', Int16, queue_size=10)


    if len(command) == 4:
        for i in range(len(command)):
            command[i] = int(command[i])

        print(command)
        print("Attack Starts in", command[1], "seconds")
        time.sleep(command[1])

        if (command[0] == 1):
            try:
                attackProc = mp.Process(target=subsBomb, args=(command[3], ))
                attackProc.start()
                pub.publish(1)
                print("Attack started for", command[2], "seconds with", command[3], "volume")
                time.sleep(command[2])
                attackProc.kill()
                pub.publish(0)
                print("Attack Stopped")
                flag = True
            except:
                print("Multi threading error!")
        
        elif (command[0] == 2):
            try:
                global atck
                attackProc = mp.Process(target=tcpFlood, args=(command[2], ))
                attackProc.start()
                print("Attack started for", command[2], "seconds")
                time.sleep(command[2])
                attackProc.kill()
                print("Attack Stopped")
                flag = True
            except:
                print("Multi threading error!")

            
    else:
        print("Input error!")






def listener():
    rospy.init_node('AttackSub', anonymous=True)
    
    rospy.Subscriber("ATK", String, callback)


    rospy.spin()
    

if __name__ == '__main__':
    listener()