#!/usr/bin/python3

import argparse
import re

max_line = 512
min_line = 4

parser = argparse.ArgumentParser()
parser.add_argument("inputfile", help="file to read")
parser.add_argument("outputfile", help="file to write")
parser.add_argument("--reject", help="file to save rejected records")
args = parser.parse_args()

inputlines = 0;
outputlines = 0;

# Line must start with an email address and have only one separator (:)
LINEREG = re.compile(r"^[^@:]+@[^@:]+\.[^@:]+:[^:]*$")

if args.reject:
	frej = open(args.reject, "w")

with open(args.inputfile, "r") as fin, open(args.outputfile, "w") as fout:
	for line in fin:
		inputlines += 1

		# discard weird line sizes
		if len(line) > max_line or len(line) < min_line:
			if args.reject:
				frej.write(line)
			continue
		# remove leading spaces
		line.strip()

		if not LINEREG.match(line):
			if args.reject:
				frej.write(line)
			continue
		
		fout.write(line)
		outputlines += 1

frej.close()

#print ("parsed " + inputlines + "lines.")
#print ("written " + outputlines + "lines.")
