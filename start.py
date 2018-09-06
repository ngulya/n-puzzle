#!/usr/bin/env python

import sys
from pz import make_puzzle,print_pz
from dop_function import ERR,heuristic_MH,return_correct_lst, parsing_arg,closed_append,have_this_in_closed
import numpy as np
# 2x2

def have_this_in_opened(opened, lst):

	z = 0
	for i in opened:
		if np.array_equal(i[4], lst):
			return z
		z += 1
	return -1


def opened_append(closed, opened, num_opened, lst_pz, parents, g, h):
	z = have_this_in_opened(opened, lst_pz)
	if z == -1:
		opened.append([])
		f = g + h
		opened[num_opened].append(f)#0
		opened[num_opened].append(g)#1
		opened[num_opened].append(h)#2
		opened[num_opened].append(parents)#3
		opened[num_opened].append(lst_pz)#4
		num_opened += 1
	else:
		print 'OPENED'
		exit(1)


def variant(lst_pz, size, side):
	if side == 'l':
		x_zero, y_zero = np.nonzero(0 == lst_pz)
		x_zero = x_zero[0]
		y_zero = y_zero[0]
		if y_zero > 0:
			lst_pz[x_zero][y_zero] = lst_pz[x_zero][y_zero - 1]
			lst_pz[x_zero][y_zero - 1] = 0
			return True, lst_pz

	elif side == 'r':
		x_zero, y_zero = np.nonzero(0 == lst_pz)
		x_zero = x_zero[0]
		y_zero = y_zero[0]
		if y_zero < size - 1:
			lst_pz[x_zero][y_zero] = lst_pz[x_zero][y_zero + 1]
			lst_pz[x_zero][y_zero + 1] = 0
			return True, lst_pz

	elif side == 'u':
		x_zero, y_zero = np.nonzero(0 == lst_pz)
		x_zero = x_zero[0]
		y_zero = y_zero[0]
		if x_zero > 0:
			lst_pz[x_zero][y_zero] = lst_pz[x_zero - 1][y_zero]
			lst_pz[x_zero - 1][y_zero] = 0
			return True, lst_pz

	elif side == 'd':
		x_zero, y_zero = np.nonzero(0 == lst_pz)
		x_zero = x_zero[0]
		y_zero = y_zero[0]
		if x_zero < size - 1:
			lst_pz[x_zero][y_zero] = lst_pz[x_zero + 1][y_zero]
			lst_pz[x_zero + 1][y_zero] = 0
			return True, lst_pz

	return False, -1
	exit()

if __name__ == "__main__":
	
	lst_pz, frst_digit = parsing_arg()
	lst_pz = np.reshape(lst_pz, (frst_digit, frst_digit))
	lst_must = return_correct_lst(frst_digit)

	if np.array_equal(lst_pz, lst_must):
		print 'Error 55: correct puzzle'
		sys.exit(1)

	# print np.array_equal(lst_pz, lst_must)
	# heuristic_MH(lst_pz, lst_must, frst_digit)

	print frst_digit
	print 
	print lst_pz
	print 
	print lst_must
	print 
	exit()
	solved = False
	unsolved = False


	closed = []
	opened = []
	
	num_closed = 0
	parents = 0
	# closed_append(closed, num_closed, lst_pz, parents = parents, g = 1, h = heuristic_MH(lst_pz, lst_must, frst_digit))
	
	print '____'
	print opened
	num_opened = 0
	parents = 0
	opened_append(opened, num_opened, lst_pz, parents = parents, g = 1, h = heuristic_MH(lst_pz, lst_must, frst_digit))
	print opened

	# print np.array_equal(lst_pz, lst_must)


	exit()	
	status, lst_r = variant(lst_pz.copy(), frst_digit, 'r')
	print 'have = ',have_this_in_closed(closed, lst_must.copy())

	if status:
		print lst_r
		# if have_this_in_closed() == False:

	# status, lst_l = variant(lst_pz.copy(), frst_digit, 'l')
	# if status:
			
	# status, lst_d = variant(lst_pz.copy(), frst_digit, 'd')
	# if status:
			
	# status, lst_u = variant(lst_pz.copy(), frst_digit, 'u')
	# if status:
		

	exit()
	while solved == False and unsolved == False:


		status, lst_r = variant(lst_pz.copy(), frst_digit, 'r')
		if status:#and have_close
			print 'r', lst_r
			print

		status, lst_l = variant(lst_pz.copy(), frst_digit, 'l')
		if status:#and have_close
			print 'l', lst_r
			print
		status, lst_d = variant(lst_pz.copy(), frst_digit, 'd')
		if status:#and have_close
			print 'd', lst_r
			print
		status, lst_u = variant(lst_pz.copy(), frst_digit, 'u')
		if status:#and have_close and have_open
			print 'u', lst_r
			print

		exit()
		raw_input('\n:')























