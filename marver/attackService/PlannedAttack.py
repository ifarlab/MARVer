import os
import signal
import subprocess
import time
import rospy
from std_msgs.msg import String

def msgpublish(s):
    msg = String()
    msg.data = s
    for _ in range(3):
        pub.publish(msg)

rospy.init_node('attackStateNode', anonymous=False)
pub = rospy.Publisher("attackState", String, queue_size=10)

AttackStr = "python SubscriberBomb.py 10"
#AttackStr = "hping3 -S 192.168.1.10 -a 192.168.1.13 --flood"
#AttackStr = "hping3 --flood 192.168.1.13"

f = open('AttackPlan.txt', 'r')
cmds = f.readlines()
sudo_password = 'toor'

for cmd in cmds:
    cmd = cmd.replace('\n', '')
    subCmd = cmd.split(' ')

    if subCmd[0] == 'Normal':
        print('Idle Phase', int(subCmd[1]), 'min')
        for i in range(5): pub.publish('False')
        time.sleep(int(subCmd[1]) * 60)    
    elif subCmd[0] == 'Attack':
        for i in range(5): pub.publish('True')
        print('Attack Phase', int(subCmd[1]), 'min')
        pro = subprocess.Popen(AttackStr, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
        time.sleep(int(subCmd[1]) * 60)
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
    elif subCmd[0] == 'Start':
        print('Started')
        #os.system('echo '' > /home/**username**ROSMonitoring/oracle/online_log.txt')
    elif subCmd[0] == 'End':
        print('Test is over. Do NOT forget to save your file!')
        #os.system('cp /home/**username**ROSMonitoring/oracle/online_log.txt /home/**username**/ROSMonitoring/oracle/Data.txt ')
