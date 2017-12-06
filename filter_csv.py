#!/usr/bin/python3

# Filters and sanitizes a ":" CSV file of the type <emailaddr>:<data> for importing into a database.
# Saves lines that can't be sanitized into a rejects file for further analysis

import argparse
import re

max_line = 512
min_line = 4

parser = argparse.ArgumentParser()
parser.add_argument("inputfile", help="file to read")
parser.add_argument("outputfile", help="file to write")
parser.add_argument("--rejects", help="file to save rejectsed records")
args = parser.parse_args()

inputlines = 0;
rejectss = 0;

# Line must start with an email address and have only one separator (:)
regex_email = re.compile(r"^[^@:]+@[^@:]+\.[^@:]+:[^:]*$")

regex_null = re.compile(r"[\x00]+")

if args.rejects:
	frej = open(args.rejects, "w")

with open(args.inputfile, "r", encoding='utf-8', errors='replace') as fin, open(args.outputfile, "w") as fout:
	for line in fin:
		inputlines += 1

		line = re.sub(regex_null, ' ', line)

		# discard weird line sizes
		if len(line) > max_line or len(line) < min_line:
			rejectss += 1
			if args.rejects:
				frej.write(line)
			continue
		# remove leading spaces
		line.strip()

		if not regex_email.match(line):
			rejectss += 1
			if args.rejects:
				frej.write(line)
			continue
		
		fout.write(line)

if args.rejects:
	frej.close()

print("Parsed {} input records.".format(inputlines))
print("rejectsed {} illegal records.".format(rejectss))

