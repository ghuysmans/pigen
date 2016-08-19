#!/usr/bin/env python2
from scipy.stats import chisquare

def formatTex(tab):
	list = " & ".join(str(x) for x in tab)
	list += "\\\\ \\hline"
	return list
def clean(stream, until):
	"""
	Discard bytes from the given stream until a character is found.
	"""
	while True:
		c = stream.read(1)
		if c in ["", until]:
			break

def real(stream, d):
	"""
	Create a real number from d ASCII digits in stream.
	"""
	acc = 0
	while d>0:
		digit = stream.read(1)
		if not digit:
			return
		elif digit.isdigit():
			acc = (acc+float(digit)) / 10
			d -= 1
	return acc

def probabilities(a,b,r):
	prob_table = []
	p = b-a
	acc = p
	prob_table.append(p)
	assert(p>0)
	for _ in range(r-1):
		acc *= (1-p)
		prob_table.append(acc)
	prob_table.append(acc*(1-p))
	return prob_table

def expected(a, b, r, s):
	return map(lambda x: s*(b-a)*x, probabilities(a, b, r))


if __name__ == "__main__":
	import sys
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-a", type=float, help="lower bound", default=0)
	parser.add_argument("-b", type=float, help="upper bound", default=0.5)
	parser.add_argument("--digits", "-d", type=int, help="digits after '0.'", default=5)
	parser.add_argument("r", type=int, help="maximum sequence length")
	parser.add_argument("s", type=int, help="test size")
	parser.add_argument("t", type=int, help="tests")
	parser.add_argument("--alpha", type=float, help="alpha test value", default=0.05)
	args = parser.parse_args()
	expected = expected(args.a, args.b, args.r, args.s)
	success = 0
	count = 0
	print formatTex(expected)
	gtfo = False
	for _ in range(args.t):
		lengths = [0 for _ in range(args.r+1)]
		max_seq_length = 0
		for _ in range(args.s):
			n = real(sys.stdin, args.digits)
			if n == None:
				print >>sys.stdout, "not enough input"
				gtfo = True
				break
			if args.a<=n and n<=args.b:
				lengths[max_seq_length] += 1
				max_seq_length = 0
			else:
				max_seq_length = min(args.r, max_seq_length+1)
			#print lengths, max_seq_length
		if gtfo:
			break
		chisq = chisquare(lengths, expected)
		s = "%5.2f %5.2f" % (chisq.statistic, chisq.pvalue)
		lengths.append("%5.2f" % chisq.statistic)
		lengths.append("%5.2f" % chisq.pvalue)
		print formatTex(lengths)
		if chisq.pvalue >= args.alpha:
			success += 1
		count += 1
	print "rate:", float(success)/count
