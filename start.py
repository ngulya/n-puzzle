#!/usr/bin/env python

import sys
import argparse
import random
from pz import make_puzzle,print_pz

if __name__ == "__main__":
	if len(sys.argv) == 2:
		try:
			in_file = open(sys.argv[1], "r")
		except:
			print "ERROR. Can't read file:", sys.argv[1]
			sys.exit(1)
		text = in_file.read()
		print type(text)
		print text
		in_file.close()
	elif len(sys.argv) == 4:
		sz = 0
		solv = False
		iterr = -1

		# print(sys.argv[1]).isdigit()
		if sys.argv[1].isdigit():
			sz = int(sys.argv[1])
		if sz < 3:
			print './start.py [size] [-s, solve OR -u, unsolve] [-i, iterations]\nsize must be digit >= 3'
			sys.exit(1)

		if sys.argv[2] == '-u':
			solv = False
		elif sys.argv[2] == '-s':
			solv = True
		else:
			print './start.py [size] [-s, solve OR -u, unsolve] [-i, iterations]\n-s OR -u'
			sys.exit(1)


		if sys.argv[3].isdigit():
			iterr = int(sys.argv[3])
		if iterr <= 0:
			print './start.py [size] [-s, solve OR -u, unsolve] [-i, iterations]\niterations must be digit > 0'
			sys.exit(1)

		puzzle = make_puzzle(sz, solvable=solv, iterations=iterr)
		print(type(puzzle))
		print_pz(sz, solv, puzzle)#check solve
	else:
		print './start.py [name_file]\n./start.py [size] [-s, solve OR -u, unsolve] [-i, iterations]'
		sys.exit(1)
