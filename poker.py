#!/usr/bin/env python2

class Poker(object):
	def process(self, digits):
		flags = [False for _ in range(self.d)]
		count = 0 #different values = class
		assert(len(digits) == self.k)
		for digit in digits:
			if not flags[digit]:
				flags[digit] = True
				count += 1
		self.classes[count-1] += 1
	def __init__(self, k):
		self.k = k
		self.d = 10
		self.classes = [0 for _ in range(self.d)]

def read(stream, k, wait_point=True):
	poker = Poker(k)
	while True:
		l = []
		while len(l)<k:
			c = stream.read(1)
			if c == "":
				return poker.classes
			elif c == ".":
				wait_point = False
			elif c.isdigit() and not wait_point:
				l.append(int(c))
		poker.process(l)
	return poker.classes

import sys
k=5
print read(sys.stdin, k)
