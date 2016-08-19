#!/usr/bin/env python2
from scipy.stats import chisquare
import math

def formatTex(tab):
	list = " & ".join(str(x) for x in tab)
	list += "\\\\ \\hline"
	return list

class Coupon(object):
	def process(self, stream):
		tab_length = [0 for _ in range(self.max_length-self.coupons+1)]
		while True:
			self.tests += 1
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
					return tab_length
			tab_length[length-self.coupons] += 1
	def probabilities(self):
		l = []
		fact = math.factorial(self.coupons)
		for r in range(self.coupons, self.max_length+1):
			if r == self.max_length:
				l.append(1-(stir(r-1, self.coupons) * float(fact) / pow(self.coupons,r-1)))
			else:
				l.append(stir(r-1, self.coupons-1) * float(fact) / pow(self.coupons,r))
		return l
	def __init__(self,nbr_of_coupons,max_length):
		"""
		Create an object processing blocks of k digits.
		"""
		self.tests = 0
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


if __name__ == "__main__":
	import sys
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("m", type=int, help="maximum sequence length (> 10)")
	parser.add_argument("--decimals", action="store_true")
	parser.add_argument("--alpha", type=float, help="alpha test value", default=0.05)
	args = parser.parse_args()
	if args.decimals:
		clean(sys.stdin, ".")
	coup = Coupon(10, args.m)
	l = coup.process(sys.stdin)
	expected = map(lambda x: coup.tests*x, coup.probabilities())
	print formatTex(expected)
	chisq = chisquare(l, expected)
	l.append("%5.2f" % chisq.statistic)
	l.append("%5.2f" % chisq.pvalue)
	print formatTex(l)
	if chisq.pvalue >= args.alpha:
		print "success"
	else:
		print "failure"
