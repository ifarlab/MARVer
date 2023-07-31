#!/usr/bin/env python
import rospy
import numpy as np
import pandas as pd
import csv
import xml.etree.ElementTree as ET
from oma_msgs.msg import oma

POSITION_FILE = '/home/s216/catkin_ws/src/oma_msgs/scripts/position.csv'
VELOCITY_FILE = '/home/s216/catkin_ws/src/oma_msgs/scripts/position2.csv'
ACCELERATION_FILE = '/home/s216/catkin_ws/src/oma_msgs/scripts/position3.csv'
JERK_FILE = '/home/s216/catkin_ws/src/oma_msgs/scripts/position4.csv'

FIELDS = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
pflag, vflag, aflag, jflag  = 0, 0, 0, 0
positions, velocities, accelerations, jerks = [], [], [], []

def save_to_csv(file_path, data):
    if not data:
        return
    
    with open(file_path, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
        if not pflag:
            writer.writeheader()
            globals()[f'{file_path}_flag'] = 1
            
        writer.writerow({f'joint{i+1}': float(np.median(data[i])) for i in range(6)})
        
def omaGraphFunc(msg):
    global positions, velocities, accelerations, jerks
    
    positions = [msg.__getattribute__(f'posJ{i+1}') for i in range(6)]
    velocities = [msg.__getattribute__(f'velJ{i+1}') for i in range(6)]
    accelerations = [msg.__getattribute__(f'accJ{i+1}') for i in range(6)]
    jerks = [msg.__getattribute__(f'jrkJ{i+1}') for i in range(6)]
    
    save_to_csv(POSITION_FILE, positions)
    save_to_csv(VELOCITY_FILE, velocities)
    save_to_csv(ACCELERATION_FILE, accelerations)
    save_to_csv(JERK_FILE, jerks)   


def main():
    rospy.Subscriber('oma', oma, omaGraphFunc)
    rospy.init_node('omaGraph', anonymous=False)
    rospy.spin()
    
#It was originally used to run main.
if __name__ == '__main__':
    main()