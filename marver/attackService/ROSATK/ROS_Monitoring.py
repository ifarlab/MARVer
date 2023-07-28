#!/usr/bin/env python
import getpass
import pyshark
import time
import multiprocessing as mp


fileCount = 1

def listen():
    global fileCount
    tmp = "/home/" + getpass.getuser() + "/Desktop/pcaptest/test"
    capture = pyshark.LiveCapture(interface='wlo1',output_file= tmp + str(fileCount) + '.pcap',)
    capture.sniff()

#capture = pyshark.LiveCapture(interface='wlo1',output_file='/home/**username**/Desktop/test.pcap',) #display_filter='xml'


pslist = []
pslist.append(mp.Process(target=listen))
pslist[0].start()

while(True):

    time.sleep(5)
    fileCount += 1
    pslist.append(mp.Process(target=listen))
    pslist[1].start()
    pslist[0].terminate()
    pslist.pop(0)

    
    
 


"""
tmp = "/home/" + getpass.getuser() + /Desktop/pcaptest/test"
for i in range(10):
    capture = pyshark.LiveCapture(interface='wlo1',output_file= tmp + str(i) + '.pcap',)
    capture.sniff(timeout=1)
"""


"""
for i in capture:
    print(i)
"""
""" 
   subs = str(i).split(' ')
    
    for j in subs:
        print(j)"""

### NASIL BİR MONİTORİNG VE LOGLAMA OLMASI BEKLENİYOR ? HAGNGİ ORTAMDA TUTULACAK (MONGO vb.) ?