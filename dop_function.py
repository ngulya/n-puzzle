#!/usr/bin/env python

import sys
import numpy as np

def ERR(ne):
	print ne
	sys.exit(1)

def heuristic_MH(lst_pz,lst_must, sz):
	# print 'heuristic_MH'
	sum_e = 0
	sum_not_mest = 0
	x = 0
	while x < sz:
		y = 0
		while y < sz:
			if lst_pz[x][y] != 0:#maybe
				if lst_pz[x][y] != lst_must[x][y]:
					sum_not_mest += 1
					# print lst_pz[x][y]
					xmst, ymst = np.nonzero(lst_must == lst_pz[x][y])
					xmst = xmst[0]
					ymst = ymst[0]
					# print x, y
					# print xmst, ymst
					pox = xmst - x
					poy = ymst - y
					if pox < 0: pox = -pox
					if poy <= 0: poy = -poy
					# print 'poy = ',poy ,' pox = ', pox
					# print 'H = ', poy + pox,'\n'
					sum_e += (poy + pox)
			y += 1
		x += 1
	# print sum_e
	# print sum_not_mest
	return sum_e


def parsing_arg():
	if len(sys.argv) == 2:
		try:
			in_file = open(sys.argv[1], "r")
		except:
			ERR('Error: cant read file:' + sys.argv[1])
			sys.exit(1)
		snos = -1
		lst_pz = []
		frst_digit = 0
		for line in in_file.readlines():
			pos = line.find('#')
			if pos > 0:
				line = line[:pos]
			elif pos == 0:
				line = ''
			if line:
				line = 	line.replace('\n', ' ')
				tmp = [str(s) for s in line.split() if s.isdigit() == False]
				# print tmp
				if len(tmp) != 0:
					ERR('Error 11: invalid map')
				tmp = [int(s) for s in line.split() if s.isdigit()]
				if len(tmp) != 0:
					snos += 1
					if frst_digit == 0:
						if len(tmp) != 1 or tmp[0] < 3:
							ERR('Error 21: invalid map')
						if tmp[0] > 50:
							ERR('Error 69: invalid size must be < 50')
						frst_digit = tmp[0]
					else:
						if len(tmp) != frst_digit:		
							ERR('Error 31: invalid map')
						lst_pz += tmp

		in_file.close()
		if frst_digit != snos:
			ERR('Error 41: invalid map')
		start = (frst_digit * frst_digit) - 1
		while  start >= 0:
			ok = 0
			for i in lst_pz:
				if i == start:
					ok = 1
			if ok == 0:
				ERR('Error 42: invalid map')
			start -= 1
	elif len(sys.argv) == 4:
		frst_digit = 0
		solv = False
		iterr = -1
		if sys.argv[1].isdigit():
			frst_digit = int(sys.argv[1])
			if frst_digit > 50:#?
				print 'Error: size > 50'
				sys.exit(1)
		if frst_digit < 3 or frst_digit > 50:
			print './start.py [size] [-s, solve OR -u, unsolve] [iterations]\nsize must be digit >= 3 and <= 50'
			sys.exit(1)
		if sys.argv[2] == '-u':
			solv = False
		elif sys.argv[2] == '-s':
			solv = True
		else:
			print './start.py [size] [-s, solve OR -u, unsolve] [iterations]\n-s OR -u'
			sys.exit(1)


		if sys.argv[3].isdigit():
			iterr = int(sys.argv[3])
		if iterr < 0 or iterr > 200000:
			print './start.py [size] [-s, solve OR -u, unsolve] [iterations]\niterations must be digit > 0 and < 200000'
			sys.exit(1)
		lst_pz = make_puzzle(frst_digit, solvable=solv, iterations=iterr)#-s and his solved correct
		print_pz(frst_digit, solv, lst_pz)#check solve
		
	else:
		print './start.py [name_file]\n./start.py [size] [-s, solve OR -u, unsolve] [iterations]'
		sys.exit(1)
	return lst_pz, frst_digit


def closed_append(closed, num_closed, lst_pz, parents, g, h):
	closed.append([])
	f = g + h
	closed[num_closed].append(f)#0
	closed[num_closed].append(g)#1
	closed[num_closed].append(h)#2
	closed[num_closed].append(parents)#3
	closed[num_closed].append(lst_pz)#4
	num_closed += 1

def have_this_in_closed(closed, lst):

	for i in closed:
		if np.array_equal(i[4], lst):
			return True
	return False

def return_correct_lst(size):
	lst_must = []
	i = 0
	while i < size:
		lst_must.append([])
		i2 = 0
		while i2 < size:
			lst_must[i].append(0)
			i2 += 1
		i += 1
	lst_must = np.reshape(lst_must, (size, size))
	
	up = 0
	left = 0
	right = size
	down = size
	maxx = (size ** 2)
	i = 1
	while i < maxx:
		u2 = up
		l2 = left
		while u2 < down - 1:
			while l2 < right - 1:
				if i < maxx:
					lst_must[u2][l2] = i
				i += 1
				l2 += 1
			if i < maxx:
				lst_must[u2][l2] = i
			i += 1
			u2 += 1

		while u2 > up:
			while l2 > left:
				if i < maxx:
					lst_must[u2][l2] = i
				i += 1
				l2 -= 1
			if i < maxx:
				lst_must[u2][l2] = i
			i += 1
			u2 -= 1
		up += 1
		down -= 1
		left += 1
		right -= 1
	return lst_must
