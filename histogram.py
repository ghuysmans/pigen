#!/usr/bin/env python2
import sys
import argparse
from scipy.stats import chisquare

def formatTex(tab):
	list = " & ".join(str(x) for x in tab)
	list += "\\\\ \\hline"
	return list

def process(stream):
	d = [0 for _ in range(10)]
	t = 0
	while True:
		c = stream.read(1)
		if not len(c):
			break
		elif c.isdigit():
			t += 1
			d[ord(c)-ord('0')] += 1
	expected = [t/10 for _ in range(10)]
	return expected, d


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--alpha", type=float, default=0.05)
	args = parser.parse_args()
	expected, histogram = process(sys.stdin)
	print formatTex(expected)
	chisq = chisquare(histogram, expected)
	histogram.append("%5.2f" % chisq.statistic)
	histogram.append("%5.2f" % chisq.pvalue)
	print formatTex(histogram)
	if chisq.pvalue >= args.alpha:
		print "success"
	else:
		print "failure"
