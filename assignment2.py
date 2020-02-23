"""
Write a Scapy script in a language of your choice (python recommended) or
command(s) to send network traffic similar to the following nmap command. 
Scapy must receive the correct answers from the targets, 
same as if nmap was used.
# nmap -sS 45.33.32.156 -n -p 22,23,31337 -Pn --traceroute

-sS = TCP SYN/Connect
-n = no DNS resolution
-p = port or port ranges
-Pn = No ping, ignore Nmap discovery stage.
--tracerout = traceroutes are performed post-scan using information from the 
              scan results to determine the port and protocol most likely to 
              reach the target.

Reference: 
How to Build a TCP Connection in Scapy: https://www.fir3net.com/Programming/Python/how-to-build-a-tcp-connection-in-scapy.html
Traceroute: https://scapy.readthedocs.io/en/latest/usage.html#tcp-traceroute

Example output: sudo nmap -sS 45.33.32.156 -n -p 22,23,31337 -Pn --traceroute
Starting Nmap 7.80 ( https://nmap.org ) at 2020-02-20 09:14 EST
Nmap scan report for 45.33.32.156
Host is up (0.17s latency).

PORT      STATE  SERVICE
22/tcp    open   ssh
23/tcp    closed telnet
31337/tcp open   Elite

TRACEROUTE (using port 23/tcp)
HOP RTT       ADDRESS
1   8.33 ms   192.168.43.83
2   66.62 ms  10.198.38.97
3   66.71 ms  10.0.115.1
4   66.92 ms  10.198.38.65
5   73.43 ms  10.164.59.213
6   73.49 ms  10.164.176.185
7   75.52 ms  4.15.212.21
8   89.52 ms  4.15.212.21
9   43.97 ms  4.68.62.186
10  98.07 ms  63.243.128.121
11  118.54 ms 63.243.128.29
12  120.47 ms 216.6.33.114
13  117.26 ms 173.230.159.71
14  123.53 ms 45.33.32.156

Nmap done: 1 IP address (1 host up) scanned in 1.46 seconds
"""

# Python3 version of Scapy.
from kamene.all import *
import random
import time


DST_IP_ADDRESS = '45.33.32.156'
DST_PORTS = {22: 'SSH',
             23: 'telnet',
             31337: 'Elite'}
SRC_HIGH_PORT = random.randint(1024,65535)


def main():
  current_time = time.localtime()
  time_start = time.process_time()
  its_online = False
  print(f'Starting scan at {time.asctime(current_time)}')

  # Checks if the ports are open.
  # How to Build a TCP Connection in Scapy: https://www.fir3net.com/Programming/Python/how-to-build-a-tcp-connection-in-scapy.html
  print('PORT\t\tSTATE\tSERVICE')
  for port, service in DST_PORTS.items():
    # SYN packet
    ip=IP(dst=DST_IP_ADDRESS)
    SYN=TCP(sport=SRC_HIGH_PORT,dport=port)
    # Sends packet and awaits response.
    SYNACK=sr1(ip/SYN, verbose=False)

    # Since we want to make a TCP connection, we look for the SYN/ACK flag response with code 18
    if SYNACK['TCP'].flags == 18:
      # Port is open.
      print(f'{port}/tcp\t\topen\t{service}')
      # ACK packet send.
      ACK=TCP(sport=SRC_HIGH_PORT, dport=port, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
      send(ip/ACK, verbose=False)
      its_online = True
    else:
      # Port is closed.
      print(f'{port}/tcp\t\tclosed\t{service}')

  # https://scapy.readthedocs.io/en/latest/usage.html#tcp-traceroute
  traceroute(DST_IP_ADDRESS, dport=22, verbose=None)
  time_end = time.process_time()

  if its_online:
      print(f'Scan done: 1 IP address (1 host up) scanned in {time_end - time_start} seconds')

if __name__ == '__main__':
  main()
