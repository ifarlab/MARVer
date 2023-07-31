#!/usr/bin/env python
import rospy
from sensor_msgs.msg import JointState
import threading
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET 
from oma_msgs.msg import oma
from std_msgs.msg import Float64MultiArray
import getpass

#reads the xml file as specified from MARVer-s Module.
with open('/home/'+getpass.getuser()+'/catkin_ws/src/oma_msgs/output.xml', 'r') as file:
    xml_string = file.read()    

#defining the parameters used in Oma service dynamically. 
root = ET.fromstring(xml_string)
value_element = root.find('.//value') 
des_pac_div_element=root.find('.//des_pac_div')
hz_element=root.find('.//hz')
topic_name= root.find('.//topic')

value = int(value_element.text)  # extract the text content of the <value> element
des_pac_div=int(des_pac_div_element.text) #extract the text content of the <des_pack divider> element
hz=int(hz_element.text) #extract the text content of the <hz> element
topic=str(topic_name.text) #extract the text content of the <topic> element


# rightJointState function values
joint1, joint2, joint3, joint4, joint5, joint6 = (0.0 for i in range(6))
joint1_list, joint2_list, joint3_list, joint4_list, joint5_list, joint6_list = ([] for i in range(6))
# while loop values
firstValueOma, changeValueOma = (0 for i in range(2))
# run_oma_in_thread function values
max_difference, differences = (0.0 for i in range(2))
position_joint1, position_joint2, position_joint3, position_joint4, position_joint5, position_joint6 = (0.0 for i in range(6))
velocity_joint1, velocity_joint2, velocity_joint3, velocity_joint4, velocity_joint5, velocity_joint6 = ([] for i in range(6))
acceleration_joint1, acceleration_joint2, acceleration_joint3, acceleration_joint4, acceleration_joint5, acceleration_joint6 = ([] for i in range(6))
jerk_joint1, jerk_joint2, jerk_joint3, jerk_joint4, jerk_joint5, jerk_joint6 = ([] for i in range(6))

#First number of data received from the OMA when we run the application.
# value = 30
# des_pac_div= 30
# hz = 30

#We publish the results of the calculations made in the run_oma_in_thread function in the talker function.
def talker():
    global topic
    pub = rospy.Publisher(topic, oma, queue_size=10)
    message = oma()

    message.posJ1 = position_joint1
    message.posJ2 = position_joint2
    message.posJ3 = position_joint3
    message.posJ4 = position_joint4
    message.posJ5 = position_joint5
    message.posJ6 = position_joint6
    
    vel1 = sum(velocity_joint1) / des_pac_div
    vel2 = sum(velocity_joint2) / des_pac_div
    vel3 = sum(velocity_joint3) / des_pac_div
    vel4 = sum(velocity_joint4) / des_pac_div
    vel5 = sum(velocity_joint5) / des_pac_div
    vel6 = sum(velocity_joint6) / des_pac_div
    
    acc1 = sum(acceleration_joint1) / des_pac_div
    acc2 = sum(acceleration_joint2) / des_pac_div
    acc3 = sum(acceleration_joint3) / des_pac_div
    acc4 = sum(acceleration_joint4) / des_pac_div
    acc5 = sum(acceleration_joint5) / des_pac_div
    acc6 = sum(acceleration_joint6) / des_pac_div
    
    jrk1 = sum(jerk_joint1) / des_pac_div
    jrk2 = sum(jerk_joint2) / des_pac_div
    jrk3 = sum(jerk_joint3) / des_pac_div
    jrk4 = sum(jerk_joint4) / des_pac_div
    jrk5 = sum(jerk_joint5) / des_pac_div
    jrk6 = sum(jerk_joint6) / des_pac_div

    message.velJ1 = vel1
    message.velJ2 = vel2
    message.velJ3 = vel3
    message.velJ4 = vel4
    message.velJ5 = vel5
    message.velJ6 = vel6

    message.accJ1 = acc1
    message.accJ2 = acc2
    message.accJ3 = acc3
    message.accJ4 = acc4
    message.accJ5 = acc5
    message.accJ6 = acc6

    message.jrkJ1 = jrk1
    message.jrkJ2 = jrk2
    message.jrkJ3 = jrk3
    message.jrkJ4 = jrk4
    message.jrkJ5 = jrk5
    message.jrkJ6 = jrk6

    pub.publish(message)
    
    pub2 = rospy.Publisher('mam_oma', Float64MultiArray, queue_size=10)
    msg = Float64MultiArray()
    msg.data = [position_joint1, position_joint2, position_joint3, position_joint4, position_joint5, position_joint6, 
                vel1, vel2, vel3, vel4, vel5, vel6, acc1, acc2, acc3, acc4, acc5, acc6, jrk1, jrk2, jrk3, jrk4, jrk5, jrk6]
    pub2.publish(msg)

#The data from the rightJointState function is calculated here.
def run_oma_in_thread(qjoint1_list, qjoint2_list, qjoint3_list, qjoint4_list, qjoint5_list, qjoint6_list):
    df = pd.DataFrame({'joint1_list': pd.Series(qjoint1_list),
                       'joint2_list': pd.Series(qjoint2_list),
                       'joint3_list': pd.Series(qjoint3_list),
                       'joint4_list': pd.Series(qjoint4_list),
                       'joint5_list': pd.Series(qjoint5_list),
                       'joint6_list': pd.Series(qjoint6_list)
                      })
    df = df.astype('float64')
 
    global position_joint1, position_joint2, position_joint3, position_joint4, position_joint5, position_joint6
    global velocity_joint1, velocity_joint2, velocity_joint3, velocity_joint4, velocity_joint5, velocity_joint6
    global acceleration_joint1, acceleration_joint2, acceleration_joint3, acceleration_joint4, acceleration_joint5, acceleration_joint6
    global differences, max_difference
    
    position_joint1 = np.median(qjoint1_list)
    position_joint2 = np.median(qjoint2_list)
    position_joint3 = np.median(qjoint3_list)
    position_joint4 = np.median(qjoint4_list)
    position_joint5 = np.median(qjoint5_list)
    position_joint6 = np.median(qjoint6_list)

    for i in range(len(qjoint1_list) - 1):
        differences = (qjoint1_list[i] - qjoint1_list[i+1])
        max_difference = np.max(differences)
        if qjoint1_list[i] > max_difference:
            break
    
    for i in range(1, len(df)):
        velocity_joint1.append((df.joint1_list[i] - df.joint1_list[i-1]) * hz)
        velocity_joint2.append((df.joint2_list[i] - df.joint2_list[i-1]) * hz)
        velocity_joint3.append((df.joint3_list[i] - df.joint3_list[i-1]) * hz)
        velocity_joint4.append((df.joint4_list[i] - df.joint4_list[i-1]) * hz)
        velocity_joint5.append((df.joint5_list[i] - df.joint5_list[i-1]) * hz)
        velocity_joint6.append((df.joint6_list[i] - df.joint6_list[i-1]) * hz)
        
        if i == len(df) - 1:
            velocity_joint1.insert(0, sum(df.joint1_list) / i)
            velocity_joint2.insert(0, sum(df.joint2_list) / i)
            velocity_joint3.insert(0, sum(df.joint3_list) / i)
            velocity_joint4.insert(0, sum(df.joint4_list) / i)
            velocity_joint5.insert(0, sum(df.joint5_list) / i)
            velocity_joint6.insert(0, sum(df.joint6_list) / i)

        if len(velocity_joint1) > des_pac_div:
            velocity_joint1.pop(0)
            velocity_joint2.pop(0)
            velocity_joint3.pop(0)
            velocity_joint4.pop(0)
            velocity_joint5.pop(0)
            velocity_joint6.pop(0)
            if i == len(df) - 1:
                velocity_joint1.pop(0)
                velocity_joint2.pop(0)
                velocity_joint3.pop(0)
                velocity_joint4.pop(0)
                velocity_joint5.pop(0)
                velocity_joint6.pop(0)

    for i in range(1, len(df)):
        acceleration_joint1.append(velocity_joint1[i] - velocity_joint1[i-1])
        acceleration_joint2.append(velocity_joint2[i] - velocity_joint2[i-1])
        acceleration_joint3.append(velocity_joint3[i] - velocity_joint3[i-1])
        acceleration_joint4.append(velocity_joint4[i] - velocity_joint4[i-1])
        acceleration_joint5.append(velocity_joint5[i] - velocity_joint5[i-1])
        acceleration_joint6.append(velocity_joint6[i] - velocity_joint6[i-1])
        
        if(i == len(df)-1):
            acceleration_joint1.insert(0, sum(velocity_joint1) / i)
            acceleration_joint2.insert(0, sum(velocity_joint2) / i)
            acceleration_joint3.insert(0, sum(velocity_joint3) / i)
            acceleration_joint4.insert(0, sum(velocity_joint4) / i)
            acceleration_joint5.insert(0, sum(velocity_joint5) / i)
            acceleration_joint6.insert(0, sum(velocity_joint6) / i)

        if len(acceleration_joint1) > des_pac_div:
            acceleration_joint1.pop(0)
            acceleration_joint2.pop(0)
            acceleration_joint3.pop(0)
            acceleration_joint4.pop(0)
            acceleration_joint5.pop(0)
            acceleration_joint6.pop(0)
            if(i == len(df)-1):
                acceleration_joint1.pop(0)
                acceleration_joint2.pop(0)
                acceleration_joint3.pop(0)
                acceleration_joint4.pop(0)
                acceleration_joint5.pop(0)
                acceleration_joint6.pop(0)

    for i in range(1, len(df)):
        jerk_joint1.append(acceleration_joint1[i] - acceleration_joint1[i-1])
        jerk_joint2.append(acceleration_joint2[i] - acceleration_joint2[i-1])
        jerk_joint3.append(acceleration_joint3[i] - acceleration_joint3[i-1])
        jerk_joint4.append(acceleration_joint4[i] - acceleration_joint4[i-1])
        jerk_joint5.append(acceleration_joint5[i] - acceleration_joint5[i-1])
        jerk_joint6.append(acceleration_joint6[i] - acceleration_joint6[i-1])
        
        if i == len(df) - 1:
            jerk_joint1.insert(0, sum(acceleration_joint1) / i)
            jerk_joint2.insert(0, sum(acceleration_joint2) / i)
            jerk_joint3.insert(0, sum(acceleration_joint3) / i)
            jerk_joint4.insert(0, sum(acceleration_joint4) / i)
            jerk_joint5.insert(0, sum(acceleration_joint5) / i)
            jerk_joint6.insert(0, sum(acceleration_joint6) / i)

        if len(jerk_joint1) > des_pac_div:
            jerk_joint1.pop(0)
            jerk_joint2.pop(0)
            jerk_joint3.pop(0)
            jerk_joint4.pop(0)
            jerk_joint5.pop(0)
            jerk_joint6.pop(0)
            if i == len(df) - 1:
                jerk_joint1.pop(0)
                jerk_joint2.pop(0)
                jerk_joint3.pop(0)
                jerk_joint4.pop(0)
                jerk_joint5.pop(0)
                jerk_joint6.pop(0)
            
    talker()

#Data from oma is processed here.
def rightJointState(msg):
    global firstValueOma,changeValueOma
    global joint1,joint2,joint3,joint4,joint5,joint6
    global joint1_list, joint2_list, joint3_list, joint4_list, joint5_list, joint6_list
    
    # Assign msg.position to individual joint variables
    joint1, joint2, joint3, joint4, joint5, joint6 = msg.position

    if firstValueOma == value:
        #Initially our changeValueOma is zero.
        if changeValueOma == 0:
            #Until firstValueOma is equal to value, appended data is sent to run_oma_in_thread function with thread.
            #In addition, after each append and pop operation, when the condition is met, new data is sent to run_oma_in_thread with the thread.
            worker = threading.Thread(target=run_oma_in_thread, args=(joint1_list,joint2_list,joint3_list,joint4_list,joint5_list,joint6_list,), daemon=True)
            worker.start()
            worker.join()
            changeValueOma += 1
        #When it is equal to half, the value is reset.
        elif changeValueOma == int(des_pac_div):
            changeValueOma = 0 
        #The else operation is performed until the ChangeValueOma equals half of the value.     
        else:
            #to add new incoming data sequentially.
            joint1_list.append(joint1)
            joint2_list.append(joint2)
            joint3_list.append(joint3)
            joint4_list.append(joint4)
            joint5_list.append(joint5)
            joint6_list.append(joint6)
            #to delete old data sequentially.
            joint1_list.pop(0)
            joint2_list.pop(0)
            joint3_list.pop(0)
            joint4_list.pop(0)
            joint5_list.pop(0)
            joint6_list.pop(0)
            changeValueOma += 1
    #The else operation is performed until firstValueOma is equal to the specified value.
    else:
        joint1_list.append(joint1)
        joint2_list.append(joint2)
        joint3_list.append(joint3)
        joint4_list.append(joint4)
        joint5_list.append(joint5)
        joint6_list.append(joint6)
        firstValueOma += 1

#We listen to the shared data about Oma in the main function.
def main():
    rospy.Subscriber('right_rokos/joint_states', JointState, rightJointState)
    rospy.init_node('oma', anonymous=True)
    rospy.spin()
    
#It was originally used to run main.
if __name__ == '__main__':
    main()
