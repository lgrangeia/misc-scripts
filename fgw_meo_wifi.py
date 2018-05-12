#!/usr/bin/python
# 
# Script to enable / disable a Meo FiberGateway (GR241AG) router's wifi channel
# for use only over wired networks (duh!) on a cron job to disable wifi at night.
# by @lgrangeia (12/05/2018)
# 

import sys
import telnetlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("control", choices=['enable', 'disable'], help="enable/disable wifi")
args = parser.parse_args()

tn = telnetlib.Telnet("192.168.1.254")

print tn.read_until("Login: ")
tn.write("meo\r\n")
print tn.read_until("Password: ")
tn.write("meo\r\n")
print tn.read_until("/cli> ")

# disables both interfaces (2.4 and 5Ghz):
tn.write("wireless/basic/config --wifi-index=0 --wifi-enable=" + args.control + "\r\n")
print tn.read_until("/cli> ")
tn.write("wireless/basic/config --wifi-index=1 --wifi-enable=" + args.control + "\r\n")
print tn.read_until("/cli> ")
tn.write("quit\r\n")

print tn.read_all()
