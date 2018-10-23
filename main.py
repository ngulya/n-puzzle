#!/usr/bin/env python

from time import time
import sys
from dop_function import *#ERR,heuristic_MH,heuristic_MH_h_v,heuristic_num_no_pos,from_input_to_int,can_solved,return_correct_lst, parsing_arg,closed_append,have_this_in_closed, variant
import numpy as np

sys.setrecursionlimit(1000000000) # DELETEEE

# print np.array_equal(lst_pz, lst_must)
# heuristic_MH(lst_pz, lst_must, frst_digit)

def have_this_in_opened(opened, lst):

	z = 0
	for i in opened:
		if np.array_equal(i[4], lst):
			return z
		z += 1
	return -1

def show_minimal(opened):
	
	min_f = opened[0][0]
	pos = 0
	act = opened[0][5]
	heurist = opened[0][2]
	i = len(opened) - 1
	while i >= 0:
		if opened[i][0] < min_f:
			min_f = opened[i][0]
			pos = i
			act = opened[i][5]
			heurist = opened[i][2]
		i -= 1
	return pos, min_f, act, heurist

def print_pos(i):#delete
	print i[4], '\nf = ',i[0], 'g = ',i[1], 'h = ',i[2], 'parent = ',i[3]

def opened_append(closed, opened, lst_pz, parents, g, h, act, nums_opened):
	z = have_this_in_opened(opened, lst_pz)
	if z == -1:
		opened.append([])
		f = g + h
		num_opened = len(opened) - 1
		opened[num_opened].append(f)#0
		opened[num_opened].append(g)#1
		opened[num_opened].append(h)#2
		opened[num_opened].append(parents)#3
		opened[num_opened].append(lst_pz)#4
		opened[num_opened].append(act)#5
		return nums_opened + 1

	else:
		if g < opened[z][1]:
			opened[z][0] = g + h
			opened[z][1] = g
			opened[z][2] = h
			opened[z][3] = parents
			opened[z][5] = act
	return nums_opened
		

def new_variants(opened, closed, flg):
	global nums_opened,t1, g_input,hmin,linear_kof
	# global ss 
	# ss += 1
	# print ss

	# print 'new_variants'
	# raw_input('->')
	last_act = -1
	heurist = 0
	if len(opened) == 0:
		# print '\n\nNO opened'
		# print closed
		lst_now = closed[-1][4].copy()

		g_now = closed[-1][1]
		parents_from_c_to_o = 0
		# raw_input(':->')
	else:
		pos, min_f, last_act, heurist = show_minimal(opened)
		lst_now = opened[pos][4].copy()
		g_now = opened[pos][1]
		if have_this_in_closed(closed, opened[pos][4]) == True:
			print 'WE HAVE IN CLOSED'
			exit()
		# print 'pos = ', pos, 'min_f = ', min_f, 'last_act = ', last_act, 'heurist = ', heurist
		# print lst_now
		closed_append(closed = closed, lst_pz = opened[pos][4], parents = opened[pos][3], g = opened[pos][1], h = opened[pos][2])
		opened = opened[0:pos] + opened[pos + 1:]
		parents_from_c_to_o = len(closed) - 1


	lst_now = closed[-1][4]
	if last_act != 2:
		status, lst_r = variant(lst_now.copy(), frst_digit, 'r')
		if status:#and have_close
			if have_this_in_closed(closed, lst_r) == False:
				# print 'r', lst_r
				h = -1
				if flg == 1:
					h = heuristic_MH(lst_r, lst_must, frst_digit, heurist, 'r')
				elif flg == 2:
					h, wow = heuristic_MH_h_v(lst_r, lst_must, frst_digit, 0, 'r')
					h += (wow * linear_kof)
				elif flg == 3:
					h, wow = heuristic_MH_h_v(lst_r, lst_must, frst_digit, heurist, 'r')
					h += (wow * linear_kof)
				elif flg == 4:
					h = heuristic_num_no_pos(lst_r, lst_must, frst_digit)
				if h < hmin:
					hmin = h
				print hmin, h
				if h == 0 or (h == -1 and np.array_equal(lst_r, lst_must)):
					t1 = time()
					print_answer(closed, lst_r, lst_now, parents_from_c_to_o)
					return
				nums_opened = opened_append(closed = closed, opened = opened, lst_pz = lst_r, parents = parents_from_c_to_o, g = g_now + g_input, h = h, act = 1, nums_opened = nums_opened)

	if last_act != 1:
		status, lst_l = variant(lst_now.copy(), frst_digit, 'l')
		if status:#and have_close
			if have_this_in_closed(closed, lst_l) == False:
				# print 'l', lst_l
				h = -1
				if flg == 1:
					h = heuristic_MH(lst_l, lst_must, frst_digit, heurist, 'l')
				elif flg == 2:
					h, wow = heuristic_MH_h_v(lst_l, lst_must, frst_digit, 0, 'l')
					h += (wow * linear_kof)
				elif flg == 3:
					h, wow = heuristic_MH_h_v(lst_l, lst_must, frst_digit, heurist, 'l')
					h += (wow * linear_kof)
				elif flg == 4:
					h = heuristic_num_no_pos(lst_l, lst_must, frst_digit)
				if h < hmin:
					hmin = h
				print hmin, h
				if h == 0 or (h == -1 and np.array_equal(lst_l, lst_must)):
					t1 = time()
					print_answer(closed, lst_l, lst_now, parents_from_c_to_o)
					return
				nums_opened = opened_append(closed = closed, opened = opened, lst_pz = lst_l, parents = parents_from_c_to_o, g = g_now + g_input, h = h, act = 2, nums_opened = nums_opened)


	if last_act != 4:
		status, lst_d = variant(lst_now.copy(), frst_digit, 'd')
		if status:#and have_close
			if have_this_in_closed(closed, lst_d) == False:
				# print 'd', lst_d
				h = -1
				if flg == 1:
					h = heuristic_MH(lst_d, lst_must, frst_digit, heurist, 'd')
				elif flg == 2:
					h, wow = heuristic_MH_h_v(lst_d, lst_must, frst_digit, 0, 'd')
					h += (wow * linear_kof)
				elif flg == 3:
					h, wow = heuristic_MH_h_v(lst_d, lst_must, frst_digit, heurist, 'd')
					h += (wow * linear_kof)
				elif flg == 4:
					h = heuristic_num_no_pos(lst_d, lst_must, frst_digit)
				if h < hmin:
					hmin = h
				print hmin, h
				if h == 0 or (h == -1 and np.array_equal(lst_d, lst_must)):
					t1 = time()
					print_answer(closed, lst_d, lst_now, parents_from_c_to_o)
					return
				nums_opened = opened_append(closed = closed, opened = opened, lst_pz = lst_d, parents = parents_from_c_to_o, g = g_now + g_input, h = h, act = 3, nums_opened = nums_opened)

	if last_act != 3:
		status, lst_u = variant(lst_now.copy(), frst_digit, 'u')
		if status:#and have_close and have_open
			if have_this_in_closed(closed, lst_u) == False:
				# print 'u', lst_u
				h = -1
				if flg == 1:
					h = heuristic_MH(lst_u, lst_must, frst_digit, heurist, 'u')
				elif flg == 2:
					h, wow = heuristic_MH_h_v(lst_u, lst_must, frst_digit, 0, 'u')
					h += (wow * linear_kof)
				elif flg == 3:
					h, wow = heuristic_MH_h_v(lst_u, lst_must, frst_digit, heurist, 'u')
					h += (wow * linear_kof)
				elif flg == 4:
					h = heuristic_num_no_pos(lst_u, lst_must, frst_digit)
				if h < hmin:
					hmin = h
				print hmin, h
				if h == 0 or (h == -1 and np.array_equal(lst_u, lst_must)):
					t1 = time()
					print_answer(closed, lst_u, lst_now, parents_from_c_to_o)
					return
				nums_opened = opened_append(closed = closed, opened = opened, lst_pz = lst_u, parents = parents_from_c_to_o, g = g_now + g_input, h = h, act = 4, nums_opened = nums_opened)


	new_variants(opened, closed, flg)

def print_answer(opened, lst,lst_now, parents):
	global frst_digit

	new_lst = []
	new_lst.append(lst)
	alls = 0
	while parents != -1:
		alls += 1
		new_lst.append(closed[parents][4])
		parents = closed[parents][3]
	print 'num all operations = ', alls
	
	try:
		in_file = open('map_solve.txt', "w")
	except:
		ERR('Error: cant read file: map_solve.txt')
		sys.exit(1)
	
	w = len(str(frst_digit*frst_digit)) + 1
	anss = raw_input('\nstep by step Y-Yes:')
	n = len(new_lst) - 1
	n2 = len(new_lst) - 1

	while n >= 0:
		in_file.write(str(-(n - n2)))
		in_file.write('\n')
		for i1 in new_lst[n]:
			for i2 in i1:
				in_file.write((str(i2).rjust(w)))
			in_file.write('\n')
		in_file.write('\n')

		print -(n - n2)
		print new_lst[n]
		print

		if anss == 'Y' or anss == 'y':
			raw_input('enter:')
		n -= 1
	in_file.close()
	print 'num all operations = ', alls



if __name__ == "__main__":
	
	lst_pz, frst_digit = parsing_arg()
	lst_must = return_correct_lst(frst_digit)

	if np.array_equal(lst_pz, lst_must):
		print 'Error 55: correct puzzle'
		sys.exit(1)

	if can_solved(lst_pz,lst_must , frst_digit) == False:
		print 'Error 65: Unsolved puzzle'
		sys.exit(1)


	try:
		in_file = open('map.txt', "w")
	except:
		ERR('Error: cant read file: map.txt')
		sys.exit(1)
	in_file.write(str(frst_digit) + '\n')
	w = len(str(frst_digit*frst_digit)) + 1
	for i1 in lst_pz:
		for i2 in i1:
			in_file.write((str(i2).rjust(w)))
		in_file.write('\n')
	in_file.close()

	try:
		in_file = open('map_solve.txt', "w")
	except:
		ERR('Error: cant read file: map_solve.txt')
		sys.exit(1)
	in_file.write('Not yet solved...\n')
	in_file.close()

	solved = False
	unsolved = False

	closed = []
	opened = []
	
	parents_c = -1
	parents_from_c_to_o = 0

	# lst_pz = [list(i) for i in lst_pz]
	# lst_must = [list(i) for i in lst_must]
	
	# print lst_pz, type(lst_pz)
	# exit()

	closed_append(closed, lst_pz, parents = parents_c, g = 0, h = heuristic_MH(lst_pz, lst_must, frst_digit, 0, '0'))#start

	nums_opened = 0
	bad = True
	g_input = from_input_to_int('g')
	linear_kof = 2
	flg = from_input_to_int('f')
	if flg == 2 or flg == 3:
		linear_kof = from_input_to_int('l')
	t0 = time()
	t1 = 0
	hmin = frst_digit ** 3
	new_variants(opened, closed,flg)

	print 'time solved %f' %(t1-t0)
	print 'in opened = ',nums_opened#?
	print 'in closed = ',len(closed)#?


	# num all operations =  30
	# time solved 2.232760
	# in opened =  1145
	# in closed =  566