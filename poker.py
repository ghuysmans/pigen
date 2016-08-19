#!/usr/bin/env python2
from scipy.stats import chisquare

def formatTex(tab):
	list = " & ".join(str(x) for x in tab)
	list += "\\\\ \\hline"
	return list
class Poker(object):
	def process(self, digits):
		"""
		Process k digits in the given array.
		"""
		flags = [False for _ in range(self.d)]
		count = 0 #different values = class
		assert(len(digits) == self.k)
		for digit in digits:
			digit = digit / (10/self.d)
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
	def __init__(self, k, d):
		"""
		Create an object processing blocks of k digits.
		"""
		self.k = k
		self.d = d
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

def read(stream, k, n, d):
	"""
	Process n blocks of k digits from a stream.
	Returns whether there is maybe more data.
	"""
	poker = Poker(k, d)
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


if __name__ == "__main__":
	import sys
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("d", type=int, help="digits (2, 5, 10)")
	parser.add_argument("k", type=int, help="hand size: at least d")
	parser.add_argument("n", type=int, help="test count")
	parser.add_argument("--alpha", type=float, help="alpha test value", default=0.05)
	parser.add_argument("--decimals", action="store_true")
	args = parser.parse_args()
	if args.decimals:
		clean(sys.stdin, ".")
	cont=True
	expected = map(lambda x: args.n*x, Poker(args.k, args.d).probabilities())
	count = 0
	success = 0
	print formatTex(expected)
	while cont:
		l, cont = read(sys.stdin, args.k, args.n, args.d)
		if cont:
			chisq = chisquare(l, expected)
			s = "%5.2f %5.2f" % (chisq.statistic, chisq.pvalue)
			l.append("%5.2f" % chisq.statistic)
			l.append("%5.2f" % chisq.pvalue)
			print formatTex(l)
			if chisq.pvalue >= args.alpha:
				success += 1
			count += 1
	print "rate:", float(success)/count
