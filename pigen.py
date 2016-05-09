#!/usr/bin/env python2
import re
import time
import sys

with open("pi6.txt","r") as f:
	f = f.read()
f = re.sub(r'[^0-9]', '', f)
start = int(time.time()%len(f))

sys.stdout.write(".")
while True:
	seed = 0
	digits = 10
	for i in range(digits):
		seed = seed*10 + int(f[start])
		start = (start + 1) % len(f)
	#ax+c mod m
	a=1234567891
	c=42
	m=2**20
	for _ in range(100):
		seed = (a*seed + c) % m
		#print float(seed)/m
		sys.stdout.write(str(int(seed*10)))
