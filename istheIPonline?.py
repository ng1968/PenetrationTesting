"""
Script that will parse IPs from a csv file and try to ping them.

Sheets link of file:
https://docs.google.com/spreadsheets/d/1RN39RxCHKoTVI7mttbQ9_6oS-zhqxg36_PmG4iwtsqY/

"""
from kamene.all import *
from socket import inet_aton
import csv

# Check if a string is a valid ip address
# Reference: https://stackoverflow.com/questions/10086572/ip-address-validation-in-python-using-regex
def is_ip(ip_address):
  try:
    socket.inet_aton(ip_address)
    return True
  except Exception as e:
    return False

def main():
  file_name = 'Indeed.com Host Records (A).csv'

  with open(file_name, 'r') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for col1, col2, _ in reader:
      # Extracts the IP from the second column
      ip_address = col2.split('\n')[0]
      subdomain = col1.split('\n')[0]
      # If HTTP is in the subdomain column we will use port 80
      # to check if its alive.
      if is_ip(ip_address) and 'HTTP' in col1:
        # TCP Ping: https://scapy.readthedocs.io/en/latest/usage.html#tcp-ping
        ans= sr1(IP(dst=ip_address)/TCP(dport=80,flags='S'), verbose=False)
        if ans['TCP'].flags == 18:
          print(f'IP address: {ip_address} is online for subdomain: {subdomain}')



if __name__ == '__main__':
    main()