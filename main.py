#!/usr/bin/env python

from time import time
import sys
from func import *
import numpy as np

sys.setrecursionlimit(1000000000)
		

def new_variants(opened, closed, flg, g_input, hmin, linear_kof, frst_digit):
	# global nums_opened, g_input, hmin, linear_kof, frst_digit
	global nums_opened
	last_act = -1
	heurist = 0
	if len(opened) == 0:
		lst_now = closed[-1][4].copy()
		g_now = closed[-1][1]
		parents_from_c_to_o = 0
	else:
		pos, min_f, last_act, heurist = show_minimal(opened)
		lst_now = opened[pos][4].copy()
		g_now = opened[pos][1]
		# if have_this_in_closed(closed, opened[pos][4]) == True:
		# 	print 'WE HAVE IN CLOSED'
		# 	exit()
		closed_append(closed = closed, lst_pz = opened[pos][4], parents = opened[pos][3], g = opened[pos][1], h = opened[pos][2])
		opened = opened[0:pos] + opened[pos + 1:]
		parents_from_c_to_o = len(closed) - 1

	if last_act != 2:
		status, lst_r = variant(lst_now.copy(), frst_digit, 'r')
		if status:
			if have_this_in_closed(closed, lst_r) == False:
				h, hmin = return_her(lst_r, lst_must, heurist, hmin, flg, frst_digit, 'r', linear_kof)
				if h == 0 and hmin == 0:
					t1 = time()
					print_answer(closed, lst_r, lst_now, parents_from_c_to_o, frst_digit)
					return t1
				nums_opened = opened_append(closed, opened, lst_r, parents_from_c_to_o, g_now + g_input, h, 1, nums_opened)

	if last_act != 1:
		status, lst_l = variant(lst_now.copy(), frst_digit, 'l')
		if status:
			if have_this_in_closed(closed, lst_l) == False:
				h, hmin = return_her(lst_l, lst_must, heurist, hmin, flg, frst_digit, 'l', linear_kof)
				if h == 0 and hmin == 0:
					t1 = time()
					print_answer(closed, lst_l, lst_now, parents_from_c_to_o, frst_digit)
					return t1
				nums_opened = opened_append(closed, opened, lst_l, parents_from_c_to_o, g_now + g_input, h, 2, nums_opened)


	if last_act != 4:
		status, lst_d = variant(lst_now.copy(), frst_digit, 'd')
		if status:
			if have_this_in_closed(closed, lst_d) == False:
				h, hmin = return_her(lst_d, lst_must, heurist, hmin, flg, frst_digit, 'd', linear_kof)
				if h == 0 and hmin == 0:
					t1 = time()
					print_answer(closed, lst_d, lst_now, parents_from_c_to_o, frst_digit)
					return t1
				nums_opened = opened_append(closed, opened, lst_d, parents_from_c_to_o, g_now + g_input, h, 3, nums_opened)

	if last_act != 3:
		status, lst_u = variant(lst_now.copy(), frst_digit, 'u')
		if status:
			if have_this_in_closed(closed, lst_u) == False:
				h, hmin = return_her(lst_u, lst_must, heurist, hmin, flg, frst_digit, 'u', linear_kof)
				if h == 0 and hmin == 0:
					t1 = time()
					print_answer(closed, lst_u, lst_now, parents_from_c_to_o, frst_digit)
					return t1
				nums_opened = opened_append(closed, opened, lst_u, parents_from_c_to_o, g_now + g_input, h, 4, nums_opened)


	return new_variants(opened, closed, flg, g_input, hmin, linear_kof, frst_digit)



if __name__ == "__main__":
	
	lst_pz, frst_digit = parsing_arg()
	lst_must = return_correct_lst(frst_digit)

	if np.array_equal(lst_pz, lst_must):
		ERR('Error 55: correct puzzle')

	if can_solved(lst_pz,lst_must , frst_digit) == False:
		ERR('Error 65: Unsolved puzzle')
	try:
		in_file = open('map.txt', "w")
	except:
		ERR('Error: cant read file: map.txt')
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
	in_file.write('Not yet solved...\n')
	in_file.close()

	solved = False
	unsolved = False

	closed = []
	opened = []
	
	parents_c = -1
	parents_from_c_to_o = 0

	nums_opened = 0
	bad = True
	g_input = from_input_to_int('g')
	linear_kof = 2
	flg = from_input_to_int('f')
	h = 0
	if flg == 1:
		h = heuristic_MH(lst_pz, lst_must, frst_digit, 0, 0)
	elif flg == 4:
		h = heuristic_num_no_pos(lst_pz, lst_must, frst_digit)
	
	if flg == 2 or flg == 3:
		linear_kof = from_input_to_int('l')
		h, wow = heuristic_MH_h_v(lst_pz, lst_must, frst_digit, 0, 0)
		h += (wow * linear_kof)


	closed_append(closed, lst_pz, parents_c, 0,h)


	hmin = h + 1
	t0 = time()
	t1 = new_variants(opened, closed,flg, g_input, hmin, linear_kof, frst_digit)

	print 'time solved %f' %(t1-t0)
	print 'in opened = ',nums_opened#?
	print 'in closed = ',len(closed)#?
