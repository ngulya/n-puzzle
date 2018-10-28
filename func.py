#!/usr/bin/env python

import sys
import numpy as np
from pz import make_puzzle,print_pz

def ERR(ne):
	print ne
	sys.exit(1)


def have_this_in_opened(opened, lst):

	z = 0
	for i in opened:
		if np.array_equal(i[4], lst):
			return z
		z += 1
	return -1


def print_answer(closed, lst ,lst_now , parents, frst_digit):

	new_lst = []
	new_lst.append(lst)
	alls = 0
	while parents != -1:
		alls += 1
		new_lst.append(closed[parents][4])
		parents = closed[parents][3]
	print 'num all operations = ', alls
	
	anss = raw_input('\nstep by step Y-Yes:')
	
	write_in_file = False
	try:
		in_file = open('map_solve.txt', "w")
		write_in_file = True
	except:
		print 'Error: cant read file: map_solve.txt'
	
	w = len(str(frst_digit*frst_digit)) + 1
	n = len(new_lst) - 1
	n2 = len(new_lst) - 1

	while n >= 0:
		if write_in_file:
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
	if write_in_file:
		in_file.close()
	print 'num all operations = ', alls


def  return_her(l, lst_must, heurist, hmin, flg, frst_digit, char, linear_kof):
	h = -1
	if flg == 1:
		h = heuristic_MH(l, lst_must, frst_digit, heurist, char)
	elif flg == 2:
		h, wow = heuristic_MH_h_v(l, lst_must, frst_digit, 0, char)
		h += (wow * linear_kof)
	elif flg == 3:
		h, wow = heuristic_MH_h_v(l, lst_must, frst_digit, heurist, char)
		h += (wow * linear_kof)
	elif flg == 4:
		h = heuristic_num_no_pos(l, lst_must, frst_digit)
	if h < hmin:
		hmin = h
		print hmin
	if h <= 0 and np.array_equal(l, lst_must):
		return 0, 0
	return h, hmin
	



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

def variant(lst_pz, size, side):
	x_zero, y_zero = np.nonzero(0 == lst_pz)
	x_zero = x_zero[0]
	y_zero = y_zero[0]
	if side == 'l':
		if y_zero > 0:
			lst_pz[x_zero][y_zero] = lst_pz[x_zero][y_zero - 1]
			lst_pz[x_zero][y_zero - 1] = 0
			return True, lst_pz

	elif side == 'r':
		if y_zero < size - 1:
			lst_pz[x_zero][y_zero] = lst_pz[x_zero][y_zero + 1]
			lst_pz[x_zero][y_zero + 1] = 0
			return True, lst_pz

	elif side == 'u':
		if x_zero > 0:
			lst_pz[x_zero][y_zero] = lst_pz[x_zero - 1][y_zero]
			lst_pz[x_zero - 1][y_zero] = 0
			return True, lst_pz

	elif side == 'd':
		if x_zero < size - 1:
			lst_pz[x_zero][y_zero] = lst_pz[x_zero + 1][y_zero]
			lst_pz[x_zero + 1][y_zero] = 0
			return True, lst_pz
	return False, -1


def can_solved(lst_pz, lst_must, size):


	saved = []
	i = 0
	saved.append([])
	i2 = 0
	while i2 < size + 2:
		saved[i].append(1)
		i2 += 1
	i += 1
	while i < size + 1:
		saved.append([])
		i2 = 0
		saved[i].append(1)
		while i2 < size:
			saved[i].append(0)
			i2 += 1
		saved[i].append(1)
		i += 1
	saved.append([])
	i2 = 0
	while i2 < size + 2:
		saved[i].append(1)
		i2 += 1
	saved = np.reshape(saved, (size + 2, size + 2))


	sums = 0
	y = 1
	x = 0
	lens = 1
	
	nums = (size * size) - 1
	while nums > 0:
		lst_tmp = saved.copy()
		yes = False
		y = 1
		x = 0
		lens = 1
		# print 'nums', nums
		while lens > 0:
			x += 1
			while x < size + 2:
				# print '|',lst_pz[y-1][x-1],'|', y, x
				now = lst_pz[y-1][x-1]
				if now == nums:
					yes = True
				if yes and now != 0 and now < nums:
					sums += 1
				lst_tmp[y][x] = 1
				if lst_tmp[y][x + 1] == 1:
					break
				x += 1
			xm0, ym0 = np.nonzero(lst_tmp == 0)
			lens = len(xm0)
			y += 1
			if lens > 0:
				while y < size + 2:
					# print y, x
					now = lst_pz[y-1][x-1]
					if now == nums:
						yes = True
					if yes and now != 0 and now < nums:
						sums += 1
					lst_tmp[y][x] = 1
					if lst_tmp[y + 1][x] == 1:
						break
					y += 1
				# print 'vnz\n'
			else:
				break
			
			
			xm0, ym0 = np.nonzero(lst_tmp == 0)
			lens = len(xm0)
			x -= 1
			if lens > 0:
				while x > 0:
					now = lst_pz[y-1][x-1]
					if now == nums:
						yes = True
					if yes and now != 0 and now < nums:
						sums += 1
					lst_tmp[y][x] = 1
					if lst_tmp[y][x - 1] == 1:
						break
					x -= 1
				# print 'vlevo\n'
			else:
				break
			xm0, ym0 = np.nonzero(lst_tmp == 0)
			lens = len(xm0)
			y -= 1
			if lens > 0:	
				while y > 0:
					now = lst_pz[y-1][x-1]
					if now == nums:
						yes = True
					if yes and now != 0 and now < nums:
						sums += 1
					lst_tmp[y][x] = 1
					if lst_tmp[y - 1][x] == 1:
						break
					y -= 1
				# print 'vverh\n'
			else:
				break
			xm0, ym0 = np.nonzero(lst_tmp == 0)
			lens = len(xm0)
		nums -= 1
	if sums % 2 == 1:
		return False

	return True



def heuristic_num_no_pos(lst_pz,lst_must, sz):

	sum_not_mest = 0
	x = 0
	while x < sz:
		y = 0
		while y < sz:
			if lst_pz[x][y] != 0:#maybe
				if lst_pz[x][y] != lst_must[x][y]:
					sum_not_mest += 1
			y += 1
		x += 1
	return sum_not_mest

def heuristic_MH(lst_pz,lst_must, sz, heuristic, act):
	
	if heuristic <= 7:
		sum_e = 0
		x = 0
		while x < sz:
			y = 0
			while y < sz:
				if lst_pz[x][y] != 0:#maybe
					if lst_pz[x][y] != lst_must[x][y]:
						xmst, ymst = np.nonzero(lst_must == lst_pz[x][y])
						xmst = xmst[0]
						ymst = ymst[0]
						pox = xmst - x
						poy = ymst - y
						if pox < 0: pox = -pox
						if poy < 0: poy = -poy
						sum_e += (poy + pox)
				y += 1
			x += 1
		return sum_e
	elif heuristic != 0:
		xmst, ymst = np.nonzero(lst_pz == 0)
		xmst_was = xmst[0]
		ymst_was = ymst[0]
		if act == 'u':
			xmst_now = xmst[0] + 1
			ymst_now = ymst[0]
		elif act == 'd':
			xmst_now = xmst[0] - 1
			ymst_now = ymst[0]
		elif act == 'l':
			xmst_now = xmst[0]
			ymst_now = ymst[0] + 1
		elif act == 'r':
			xmst_now = xmst[0]
			ymst_now = ymst[0] - 1
		num_now = lst_pz[xmst_now][ymst_now]
		xmst, ymst = np.nonzero(lst_must == num_now)
		xmst_must = xmst[0]
		ymst_must = ymst[0]
		pox = xmst_must - xmst_was
		poy = ymst_must - ymst_was
		if pox < 0: pox = -pox
		if poy < 0: poy = -poy
		was = (poy + pox)
		pox = xmst_must - xmst_now
		poy = ymst_must - ymst_now
		if pox < 0: pox = -pox
		if poy < 0: poy = -poy
		now = (poy + pox)
		heuristic -= was
		heuristic += now
	return heuristic


def heuristic_MH_h_v(lst_pz,lst_must, sz, heuristic, act):
	
	k = 0
	up = 0
	left = 0
	right = sz
	down = sz
	maxx = (sz * sz)
	i = 1
	sum_e = heuristic_MH(lst_pz, lst_must, sz, heuristic, act)
	wow = 0
	lst_tmp = []
	num = 0
	while i < maxx:
		frst_t = True
		y2 = up
		x2 = left
		st = lst_must[y2][x2]
		en = st + right - x2 - 1
		while x2 < right and i < maxx:######1
			now = lst_pz[y2][x2]
			if now >= st and now <= en:
				lst_tmp.append(now)
				num += 1
			x2 += 1
			i += 1

		frst_t = True
		x2 -= 1
		up += 1
		st = lst_must[y2][x2]
		en = st + down - y2 - 1
		while y2 < down and i < maxx:######2
			now = lst_pz[y2][x2]
			if now >= st and now <= en:
				lst_tmp.append(now)
				num += 1
			y2 += 1
			i += 1

		frst_t = True
		y2 -= 1
		right -= 1
		st = lst_must[y2][x2]
		en = st + x2 - left
		while  x2 >= left and i < maxx:######3
			now = lst_pz[y2][x2]
			if now >= st and now <= en:
				lst_tmp.append(now)
				num += 1
			x2 -= 1
			i += 1

		frst_t = True
		x2 += 1
		down -= 1
		st = lst_must[y2][x2]
		en = st + y2 - up
		while y2 >= up and i < maxx:######4
			now = lst_pz[y2][x2]
			if now >= st and now <= en:
				lst_tmp.append(now)
				num += 1
			i += 1
			y2 -= 1
		y2 += 1
		left += 1
	if len(lst_tmp) > 1:
		num1 = 0
		while num1 < num:##########wow
			num2 = num1 + 1
			lst_tmp_num1 = lst_tmp[num1]
			while num2 < num:
				if lst_tmp[num2] < lst_tmp_num1:
					wow += 1
				num2 += 1
			num1 += 1
	return sum_e, wow



def parsing_arg():
	if len(sys.argv) == 2:
		try:
			in_file = open(sys.argv[1], "r")
		except:
			ERR('Error: cant read file:' + sys.argv[1])
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
						if tmp[0] > 1000:
							ERR('Error 69: invalid size must be < 1000')
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
		lst_pz = np.reshape(lst_pz, (frst_digit, frst_digit))
		print 'From file pzzl'
		print lst_pz
	elif len(sys.argv) == 4:
		frst_digit = 0
		solv = False
		iterr = -1
		if sys.argv[1].isdigit():
			frst_digit = int(sys.argv[1])
		if frst_digit < 3 or frst_digit > 50:
			ERR('./start.py [size] [-s, solve OR -u, unsolve] [iterations]\nsize must be digit >= 3 and <= 50')
		if sys.argv[2] == '-u':
			solv = False
		elif sys.argv[2] == '-s':
			solv = True
		else:
			ERR('./start.py [size] [-s, solve OR -u, unsolve] [iterations]\n-s OR -u')

		if sys.argv[3].isdigit():
			iterr = int(sys.argv[3])
		if iterr < 1 or iterr > 200000:
			ERR('./start.py [size] [-s, solve OR -u, unsolve] [iterations]\niterations must be digit > 0 and < 200000')

		lst_must = return_correct_lst(frst_digit)
		
		bad = True
		while bad:
			lst_pz_str = make_puzzle(frst_digit, solvable=solv, iterations=iterr)#-s and his solved correct
			lst_pz = np.reshape(lst_pz_str, (frst_digit, frst_digit))
			if np.array_equal(lst_pz, lst_must) == False:
				bad = False
				print_pz(frst_digit, solv, lst_pz_str)
			else:
				print 'VBAD'
	else:
		ERR('./start.py [name_file]\n./start.py [size] [-s, solve OR -u, unsolve] [iterations]')
	return lst_pz, frst_digit


def closed_append(closed, lst_pz, parents, g, h):
	closed.append([])
	f = g + h
	num_closed = len(closed) - 1
	closed[num_closed].append(f)#0
	closed[num_closed].append(g)#1
	closed[num_closed].append(h)#2
	closed[num_closed].append(parents)#3
	closed[num_closed].append(lst_pz)#4


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

	k = 0
	up = 0
	left = 0
	right = size
	down = size
	maxx = (size * size)
	i = 1
	while i < maxx:
		y2 = up
		x2 = left
		while x2 < right and i < maxx:
			lst_must[y2][x2] = i
			x2 += 1
			i += 1
		x2 -= 1
		y2 += 1
		up += 1
		while y2 < down and i < maxx:
			lst_must[y2][x2] = i
			y2 += 1
			i += 1
		y2 -= 1
		x2 -= 1
		right -= 1
		while  x2 >= left and i < maxx:
			lst_must[y2][x2] = i
			x2 -= 1
			i += 1
		x2 += 1
		y2 -= 1
		down -= 1
		while y2 >= up and i < maxx:
			lst_must[y2][x2] = i
			i += 1
			y2 -= 1

		y2 += 1
		x2 += 1
		left += 1
	return lst_must


def from_input_to_int(variant):
	if variant == 'g':
		g_input = 1
		bad = True
		while bad:
			gm = raw_input('\ndef = 1, input g >= 0: ')
			try:
				int(gm)
			except Exception as e:
				g_input = 1
				# print 'g_input = 1'
				break
			if int(gm) >= 0 and int(gm) < 10:
				g_input = int(gm)
				break
			else:
				print 'Error: g >= 0 and g < 10'
		return g_input
	elif variant == 'l':
		linear_kof = 2
		bad = True
		while bad:
			gm = raw_input('\ndef = 2, input linear_kof >= 0: ')
			try:
				int(gm)
			except Exception as e:
				linear_kof = 2
				# print 'linear_kof = 2'
				break
			
			if int(gm) >= 0 and int(gm) < 10:
				linear_kof = int(gm)
				break
			else:
				print 'Error: linear_kof >= 0 and linear_kof < 10'
		return linear_kof
	elif variant == 'f':
		flg = 1
		bad = True
		print '\n0-greedy\n1-heuristic_MH\n2-heuristic_MH_h_v\n3-heuristic_MH_h_v_history\n4-heuristic_num_no_pos'
		while bad:
			gm = raw_input('def = 1, input heuristic 1/2/3/4: ')
			try:
				int(gm)
			except Exception as e:
				flg = 1
				# print 'heuristic = 1'
				break
			
			if int(gm) >= 0 and int(gm) < 5:
				flg = int(gm)
				break
			else:
				print 'Error: heuristic >= 0 and heuristic < 5'
		return flg


 
