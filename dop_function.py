#!/usr/bin/env python

import sys
import numpy as np
from pz import make_puzzle,print_pz

def ERR(ne):
	print ne
	sys.exit(1)


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
	# print saved, '\n'


	# print lst_pz, '\n'

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
				# for h in mas:
				# 	if h > now:
				# 		sums += 1
				lst_tmp[y][x] = 1
				if lst_tmp[y][x + 1] == 1:
					break
				x += 1
			# print 'vpravo\n'
			
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
					# print '|',lst_pz[y-1][x-1],'|'
					# now = lst_pz[y-1][x-1]
					# for h in mas:
					# 	if h > now:
					# 		sums += 1
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
					# print '|',lst_pz[y-1][x-1],'|'
					# now = lst_pz[y-1][x-1]
					# for h in mas:
					# 	if h > now:
					# 		sums += 1
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

					# print '|',lst_pz[y-1][x-1],'|'
					# now = lst_pz[y-1][x-1]
					# for h in mas:
					# 	if h > now:
					# 		sums += 1
					lst_tmp[y][x] = 1
					if lst_tmp[y - 1][x] == 1:
						break
					y -= 1
				# print 'vverh\n'
			else:
				break
			xm0, ym0 = np.nonzero(lst_tmp == 0)
			lens = len(xm0)
			# print '\n'
			# print 'xm0 = ',xm0, lens
			# exit()
		# print 'nums',nums , sums
		nums -= 1
	# print 'sums = ',sums
	# print sums % 2, 'sums % 2' 

	if sums % 2 == 1:
		# print 'Unsolved'
		return False
	# else:
	# 	print 'Can solved'
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

def heuristic_MH(lst_pz,lst_must, sz):
	# print 'heuristic_MH'
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
					if poy <= 0: poy = -poy
					sum_e += (poy + pox)
			y += 1
		x += 1
	return sum_e


def heuristic_MH_h_v(lst_pz,lst_must, sz):
	
	k = 0
	up = 0
	left = 0
	right = sz
	down = sz
	maxx = (sz ** 2)
	i = 1
	sum_e = heuristic_MH(lst_pz, lst_must, sz)
	wow = 0
	while i < maxx:

		frst_t = True
		y2 = up
		x2 = left
		lst_tmp = []
		num = 0
		while x2 < right and i < maxx:######1
			now = lst_pz[y2][x2]
			if frst_t:
				frst_t = False
				st = lst_must[y2][x2]
				en = st + right - x2 - 1
			if now >= st and now <= en:
				lst_tmp.append(now)
				num += 1
			x2 += 1
			i += 1
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
		##############################

		frst_t = True
		x2 -= 1
		y2 += 1
		up += 1
		lst_tmp = []
		while y2 < down and i < maxx:######2
			if frst_t:
				frst_t = False
				st = lst_must[y2][x2]
				en = st + down - y2 - 1
			y2 += 1
			i += 1
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
			#################################

		frst_t = True
		lst_tmp = []
		y2 -= 1
		x2 -= 1
		right -= 1
		while  x2 >= left and i < maxx:######3
			if frst_t:
				frst_t = False
				st = lst_must[y2][x2]
				en = st + x2 - left
			x2 -= 1
			i += 1
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
		#################################

		frst_t = True
		lst_tmp = []
		x2 += 1
		y2 -= 1
		down -= 1
		while y2 >= up and i < maxx:######4
			# print y2, up
			if frst_t:
				frst_t = False
				st = lst_must[y2][x2]
				en = st + y2 - up
			i += 1
			y2 -= 1
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
		y2 += 1
		x2 += 1
		left += 1

	return sum_e, wow



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
		lst_pz = np.reshape(lst_pz, (frst_digit, frst_digit))
		print 'From file pzzl'
		print lst_pz
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
		if iterr < 1 or iterr > 200000:
			print './start.py [size] [-s, solve OR -u, unsolve] [iterations]\niterations must be digit > 0 and < 200000'
			sys.exit(1)
		
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
		print './start.py [name_file]\n./start.py [size] [-s, solve OR -u, unsolve] [iterations]'
		sys.exit(1)
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
	maxx = (size ** 2)
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
			gm = raw_input('\ninput g > 0: ')
			try:
				int(gm)
			except Exception as e:
				g_input = 1
				print 'g_input = 1'
				break
			if int(gm) > 0 and int(gm) < 10:
				g_input = int(gm)
				break
			else:
				print 'Error: g > 0 and g < 10'
		return g_input
	elif variant == 'l':
		linear_kof = 2
		bad = True
		while bad:
			gm = raw_input('\ninput linear_kof >= 0: ')
			try:
				int(gm)
			except Exception as e:
				linear_kof = 2
				print 'linear_kof = 2'
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
		print '\n1-heuristic_MH\n2-heuristic_MH_h_v\n3-heuristic_num_no_pos'
		while bad:
			gm = raw_input('input flg 1/2/3: ')
			try:
				int(gm)
			except Exception as e:
				flg = 1
				print 'flg = 1'
				break
			
			if int(gm) > 0 and int(gm) < 4:
				flg = int(gm)
				break
			else:
				print 'Error: flg > 0 and flg < 4'
		return flg
