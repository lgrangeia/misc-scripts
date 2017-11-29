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
rejects = 0;

# Line must start with an email address and have only one separator (:)
LINEREG = re.compile(r"^[^@:]+@[^@:]+\.[^@:]+:[^:]*$")

if args.reject:
	frej = open(args.reject, "w")

with open(args.inputfile, "r") as fin, open(args.outputfile, "w") as fout:
	for line in fin:
		inputlines += 1

		# discard weird line sizes
		if len(line) > max_line or len(line) < min_line:
			rejects += 1
			if args.reject:
				frej.write(line)
			continue
		# remove leading spaces
		line.strip()

		if not LINEREG.match(line):
			rejects += 1
			if args.reject:
				frej.write(line)
			continue
		
		fout.write(line)

frej.close()

print("Parsed {} input records.".format(inputlines))
print("Rejected {} illegal records.".format(rejects))
