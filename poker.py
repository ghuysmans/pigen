#!/usr/bin/env python2
from scipy.stats import chisquare

class Poker(object):
	def process(self, digits):
		"""
		Process k digits in the given array.
		"""
		flags = [False for _ in range(self.d)]
		count = 0 #different values = class
		assert(len(digits) == self.k)
		for digit in digits:
			if not flags[digit]:
				flags[digit] = True
				count += 1
		self.classes[count-1] += 1
	def probabilities(self):
		#TODO extract this
		l = []
		dprod = self.d
		denom = self.d**self.k
		d = self.d
		for r in range(1, d+1):
			l.append(stir(self.k, r) * float(dprod) / denom)
			d = d - 1
			dprod *= d
		return l
	def __init__(self, k):
		"""
		Create an object processing blocks of k digits.
		"""
		self.k = k
		self.d = 10
		assert(k>=self.d)
		self.classes = [0 for _ in range(min(self.d, k))]

def clean(stream, until):
	"""
	Discard bytes from the given stream until a character is found.
	"""
	while True:
		c = stream.read(1)
		if c in ["", until]:
			break

def stir(k,r):
	assert(k>0)
	assert(r>0)
	if k == r or r == 1:
		return 1
	else:
		return stir(k-1,r-1) + r*stir(k-1,r)

def read(stream, k, n):
	"""
	Process n blocks of k digits from a stream.
	Returns whether there is maybe more data.
	"""
	poker = Poker(k)
	while n>0:
		l = []
		while len(l)<k:
			c = stream.read(1)
			if c == "":
				return poker.classes, False
			elif c.isdigit():
				l.append(int(c))
		poker.process(l)
		n -= 1
	return poker.classes, True

def regroup(l):
	return [sum(l[:4])+sum(l[-2:])] + l[4:-2]


if __name__ == "__main__":
	import sys
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("k", type=int, help="block size: 10?")
	parser.add_argument("n", type=int, help="test size: 1000?")
	parser.add_argument("--alpha", type=float, help="alpha test value", default=0.05)
	parser.add_argument("--decimals", action="store_true")
	args = parser.parse_args()
	if args.decimals:
		clean(sys.stdin, ".")
	cont=True
	expected = map(lambda x: int(args.n*x), Poker(args.k).probabilities())
	expected = regroup(expected)
	count = 0
	success = 0
	while cont:
		l, cont = read(sys.stdin, args.k, args.n)
		if cont:
			l = regroup(l)
			chisq = chisquare(l, expected)
			s = "%5.2f %5.2f" % (chisq.statistic, chisq.pvalue)
			print l, expected, s
			if chisq.pvalue >= 1-args.alpha:
				success += 1
			count += 1
	print "rate:", float(success)/count
