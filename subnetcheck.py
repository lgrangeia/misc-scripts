#!/usr/bin/python

import socket
from netaddr import *
import argparse

def main():

    parser = argparse.ArgumentParser(description='Given a list of ip addreses and subnets, outputs a CSV with IP<->subnet mappings')
    parser.add_argument('--ips', type=argparse.FileType("r"), help='list of ips', required=True)
    parser.add_argument('--ranges', type=argparse.FileType("r"), help='list of ranges/subnets', required=True)

    args = parser.parse_args()

    with args.ips as file:
        ips = filter(None, (l.rstrip() for l in file))

    with args.ranges as file:
        ranges = filter(None, (l.rstrip() for l in file))

    for i in ips:
        addr = IPAddress(i)
        #print str(addr)

        for s in ranges:
            if valid_nmap_range(s):
                ip_list = list(iter_nmap_range(s))
                for x in ip_list:
                    if x == addr:
                        print str(addr) + ";" + s
                        break
            else:
                ip_network = IPNetwork(s)
                if ip_network.contains(i):
                    print str(addr) + ";" + str(ip_network)
                    break;

if __name__ == "__main__":
    main()
