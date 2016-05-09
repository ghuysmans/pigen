#!/usr/bin/env python2
from scipy.stats import chisquare
import math

class Coupon(object):
	def process(self, stream):
		"""
		Process k digits in the given array.
		"""
		tab_length = [0 for _ in range(self.max_length-self.coupons+1)]
		for _ in range(self.n):
			flags = [False for _ in range(self.coupons)]
			count = 0 #different values = class
			length = 0
			while count != self.coupons and length < self.max_length:
				n = stream.read(1)
				if n.isdigit():
					length += 1
					n = int(n)
					if not flags[n]:
						flags[n] = True
						count += 1
				elif not len(n):
					return
			tab_length[length-self.coupons] += 1
		return tab_length

	def probabilities(self):
		l = []
		fact = math.factorial(self.coupons)
		for r in range(self.coupons, self.max_length+1):
			p = stir(r-1, self.coupons-1) * float(fact) / pow(self.coupons,r)
			if r == self.max_length:
				l.append(1-p)
			else:
				l.append(p)
		return l
	def __init__(self,n,nbr_of_coupons,max_length):
		"""
		Create an object processing blocks of k digits.
		"""
		self.n = n
		self.coupons = nbr_of_coupons
		self.max_length = max_length

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
	parser.add_argument("n", type=int, help="coupons size: ?")
	parser.add_argument("m", type=int, help="max length: 10?")
	parser.add_argument("s", type=int, help="nbr of coupons")
	parser.add_argument("t", type=int, help="nbr of tests")
	parser.add_argument("--decimals", action="store_true")
	parser.add_argument("--alpha", type=float, help="alpha test value", default=0.05)
	args = parser.parse_args()
	count = 0
	success = 0
	if args.decimals:
		clean(sys.stdin, ".")
	coup = Coupon(args.n,args.s,args.m)
	expected = map(lambda x: int(args.n*x), coup.probabilities())
	for _ in range(args.t):
		l = coup.process(sys.stdin)
		print l, expected
		chisq = chisquare(l, expected)
		s = "%5.2f %5.2f" % (chisq.statistic, chisq.pvalue)
		#print l, expected, s
		if chisq.pvalue >= args.alpha:
			success += 1
		count += 1
	print "rate:", float(success)/count
