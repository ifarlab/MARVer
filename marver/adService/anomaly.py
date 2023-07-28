# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 15:20:57 2021

@author: elifd
"""

import numpy as np
import math

class cls_AnomalyDetection():
    upper_limit1 = 120
    lower_limit1 = 90
    normal = False
    counter = 0
    def __init__(self,time_interval, upper_limit, lower_limit, sensitivity):
        self.time_interval = time_interval
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.sensitivity = sensitivity
        

    def ortalama(self, vektor):
        self.veriAdedi = len(vektor)
        if self.veriAdedi <= 1:
            return vektor
        else:
            #print (sum(vektor) / veriAdedi)
            return sum(vektor) / self.veriAdedi

    def standartSapma(self, vektor):
        sd = 0.0 # standart sapma
        self.vector = vektor
        veriAdedi = len(self.vector)
        if veriAdedi <= 1:
            return 0.0
        else:
            for _ in vektor:
                sd += (float(_) - self.ortalama(vektor)) ** 2
            sd = (sd / float(veriAdedi)) ** 0.5
            #print("adada",sd)
            return sd

    def varyans(self, vektor):
        return self.standartSapma(self, vektor) ** 2

    def AnomalyDetection(self, data):
        #identify data   
        #self.time_interval = 50  # for obtaining sound
        #self.lowerbound = 98  # for obtaining sound
        #self.upperbound = 100
        #self.senscutoff = 3  # update plot every 30/1000 second
        if self.counter>=1:
            window_size=int(self.time_interval)
            tmp_data = data[-window_size:]
            print(tmp_data)
            #calculate new window of data's SS and mean
            data_std = self.standartSapma(tmp_data)
            data_ort = self.ortalama(tmp_data)
            cut_off = data_std * self.sensitivity    
            
            tmp_max = max(tmp_data)
            tmp_min = min(tmp_data)
            
            #print(data_std,data_ort,cut_off)
            if tmp_max>self.upper_limit or tmp_min<self.lower_limit:
                for j,outlier in enumerate(tmp_data):
                    if outlier > math.ceil(self.upper_limit) or outlier < math.floor(self.lower_limit):
                            self.normal=True
                            print("anomaly detected", tmp_data[j], self.upper_limit, self.lower_limit) 

            else:
                self.normal = False
                print("normal")
            
            if self.normal==False :
                self.lower_limit  = data_ort - cut_off 
                self.upper_limit = data_ort + cut_off
                print("bounds updated: ", self.upper_limit, self.lower_limit)
                return self.normal
            else:
                #print("false :: bounds updated: ", self.upper_limit, self.lower_limit)
                #print(data_std,data_ort,cut_off)
                #print("somethings wrong")
                return self.normal
        else:
            self.counter += 1
            print("not ready", self.counter)                
            
