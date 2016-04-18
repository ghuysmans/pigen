#!/usr/bin/env python2
import sys
k=5
d=10
classes = [0 for _ in range(k)]
while True:
	flags = [False for _ in range(d)]
	count = 0 #different values = class
	stop = False #to leave the outer loop
	for _ in range(k):
		digit = sys.stdin.read(1)
		if digit == "":
			stop = True
			break
		elif digit.isdigit():
			digit = int(digit)
			if not flags[digit]:
				flags[digit] = True
				count += 1
	if stop:
		break
	else:
		classes[count-1] += 1
print classes
