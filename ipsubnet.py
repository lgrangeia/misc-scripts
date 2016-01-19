#!/usr/bin/python

import sys
import os
from netaddr import IPNetwork, IPAddress

if (len(sys.argv) != 3):
    print ('takes a list of IP addresses and subnets and returns a CSV of ip;subnet1;subnet2')
    print ('usage: {:s} <iplist> <subnetlist>'.format(sys.argv[0]))
    sys.exit(-1)

# read ips from first file:
with open(sys.argv[1], 'r') as f:
    iplist = f.read().splitlines() 
    f.close()

# read subnets from second file:
with open(sys.argv[2], 'r') as f:
    subnetlist = f.read().splitlines() 
    f.close()

for ip in iplist:
    line = ip + ";"
    for subnet in subnetlist:
        if IPAddress(ip) in IPNetwork(subnet):
            line = line + subnet + ";"
    print(line)

