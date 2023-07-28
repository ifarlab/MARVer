#!/usr/bin/env python
from logging import StringTemplateStyle
from pickle import FALSE
import time
import rospy
from rospy.impl.rosout import RosOutHandler
from std_msgs.msg import String, Float32
from rv_sec.msg import rvsec
import os
import csv
import threading as th
import numpy as np
import matplotlib.pyplot as plt 
import math
import datetime

count = 0
curTime = time.time()
attackState = 'False'

lst_ros = []
lst_csv = []

logfile = open('ros.csv', mode='w')
logwriter = csv.writer(logfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

def bw():
     os.system("rostopic bw /QoS")

def hz():
     os.system("rostopic hz /QoS")

def callback(data):
    global lst_ros, lst_csv
    lst_ros.append(data)
   
def csv_packager(sample_time = 1):
    global lst_ros, lst_csv, normal
    data = []
    while True:
        packTime = time.time() + sample_time
        
        while time.time() <= packTime:
            if len(lst_ros) > 0:
                lst_csv.append(lst_ros.pop(0))
                
        frequency =   len(lst_csv) / sample_time 
        pub = rospy.Publisher('QoSFreq', rvsec, queue_size=10)
        print("Frequency: ",frequency)
           
        data.append(frequency)
        if (len(data) >= 5):
            msg = rvsec()
            AnomalyDetection(data)
            print("Ort: ",ortalama(data))
            if normal:
                msg.ad = 'True'
                msg.data = ortalama(data)
                pub.publish(msg)
            else:
                msg.ad = 'False'
                msg.data = ortalama(data)
                pub.publish(msg)
            data.clear()
        
        lst_csv.clear()



##############################AD#####################################

upper_limit = 103
lower_limit = 98
normal = True


def ortalama(vektor):
    veriAdedi = len(vektor)
    if veriAdedi <= 1:
        return vektor
    else:
        #print (sum(vektor) / veriAdedi)
        return sum(vektor) / veriAdedi

def standartSapma(vektor):
    sd = 0.0 # standart sapma
    veriAdedi = len(vektor)
    if veriAdedi <= 1:
        return 0.0
    else:
        for _ in vektor:
            sd += (float(_) - ortalama(vektor)) ** 2
        sd = (sd / float(veriAdedi)) ** 0.5
        return sd

def varyans(vektor):
    return standartSapma(vektor) ** 2

def AnomalyDetection(data):

    #identify len of data
    window_size=len(data)
    
    #identify limits as global
    global upper_limit
    global lower_limit
    global normal
    
    #calculate new window of data's SS and mean
    data_std = standartSapma(data)
    data_ort = ortalama(data)
    cut_off = data_std * 3    
    
    if cut_off > 2:
    	for j,outlier in enumerate(data):
    		if outlier > math.ceil(upper_limit) or outlier < math.floor(lower_limit):
                    normal=False
                    print("anomaly detected", data[j], upper_limit, lower_limit) 

    else:
        normal = True
        print("normal")
    
    if normal==True and cut_off > 2:
        lower_limit  = data_ort - cut_off 
        upper_limit = data_ort + cut_off
        print("bounds updated: ", upper_limit, lower_limit)
###################################################################

def listener():
    rospy.init_node('ROSQoSSub', anonymous=True)

    rospy.Subscriber("QoS", String, callback)

    try:
        customFrequency = th.Thread(target=csv_packager)
        customFrequency.start()
    except:
        print("Multi threading error!")


    rospy.spin()
    

if __name__ == '__main__':
    listener()