"""
Script that will find the IP addresses of a list of urls.
"""
from kamene.all import *


def main():
  file_name = 'sublist3r.txt'
  is_online = {}

  with open(file_name, 'r') as indeed_file:
    for row in indeed_file:
      subdomain = row.rstrip()
        # TCP Ping: https://scapy.readthedocs.io/en/latest/usage.html#tcp-ping
      ans = sr1(IP(dst=subdomain.rstrip())/TCP(dport=80,flags='S'), verbose=False)
      if ans['TCP'].flags == 18:
          ip_address = ans['IP'].src
          is_online.setdefault(ip_address, [])
          if ip_address in is_online:
            is_online[ip_address].append(subdomain)

  for key, values in is_online.items():
    print('IP Address: {0:s} is online and has the following subdomains: {1:s}'.format(key,', '.join(values)))


if __name__ == '__main__':
    main()
