#!/bin/python
# 
# Script to enable / disable a Meo (thomson TG784) router's wifi channel
# for use only over wired networks (duh!) on a cron job to disable wifi at night.
# by @lgrangeia (16/10/2017)
# 

import sys
import telnetlib

if len(sys.argv) != 2 and (sys.argv[1] != "disabled" or sys.argv[1] != "enabled"):
    print "usage: " + sys.argv[0] + " <enabled|disabled>"

tn = telnetlib.Telnet("192.168.1.254")

tn.read_until("Username :")
tn.write("meo\r\n")
tn.read_until("Password :")
tn.write("meo\r\n")
tn.read_until("{meo}=>")
tn.write("wireless radio state = " + sys.argv[1] + "\r\n")
tn.read_until("{meo}=>")
tn.write("exit\r\n")

