#!/usr/bin/env python2
import sys
print "."
while True:
	d = sys.stdin.read(1)
	if d == "":
		break
	elif d.isdigit():
		d = int(float(d)/10*6)
		sys.stdout.write(str(d))
print
