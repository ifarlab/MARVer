#!/usr/bin/env python
import rospy
from oma_msgs.msg import oma

import json
import pandas as pd
import numpy as np
import re

msgTrueCount = 0
msgErrorCount = 0
msgCount = 0
with open('/home/esogu-ifarlab/marver/3rdparty/rosmonitoring/oracle/TLOracle/properties/oma_demo.json') as f:
    data = json.load(f)

formula = data['properties'][0]['formula']
values = re.findall(r'\d+\.\d+', formula)
values = list(map(float, values))

# print(values)

def callback(msg):
    global msgCount, msgTrueCount, msgErrorCount
    msgCount += 1
    if msg.posJ1 < values[0] and msg.posJ2 < values[1] and msg.posJ3 < values[2] and msg.posJ4 < values[3] and msg.posJ5 < values[4] and msg.posJ6 < values[5]:
        msgTrueCount += 1
    else:
        msgErrorCount += 1

    print(f"True :  {msgTrueCount}")
    print(f"False :  {msgErrorCount}")
  
def main():
    rospy.init_node('omaTestCode', anonymous=True)
    rospy.Subscriber('oma_mon', oma, callback)
    rospy.spin()
    
if __name__ == '__main__':
    main()
