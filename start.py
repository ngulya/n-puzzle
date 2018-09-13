#!/usr/bin/env python

from time import time
import sys
from dop_function import ERR,heuristic_MH,heuristic_MH_h_v,return_correct_lst, parsing_arg,closed_append,have_this_in_closed, variant
import numpy as np

sys.setrecursionlimit(10000) # DELETEEE

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

	i = len(opened) - 1
	while i >= 0:
		if opened[i][0] < min_f:
			min_f = opened[i][0]
			pos = i
			act = opened[i][5]
		i -= 1
	return pos, min_f, act

def print_pos(i):#delete
	print i[4], '\nf = ',i[0], 'g = ',i[1], 'h = ',i[2], 'parent = ',i[3]

def opened_append(closed, opened, lst_pz, parents, g, h, act):
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

	else:
		if g < opened[z][1]:
			# print '\n\nOPENED APPEND'
			# print 'CLOSED'
			# for i in closed:
			# 	print i[4], '\nf=',i[0], 'g=',i[1], 'h=',i[2], 'parent=',i[3]
			# print '---------\nOPENED'
			# for i in opened:
			# 	print i[4], '\nf=',i[0], 'g=',i[1], 'h=',i[2], 'parent=',i[3]
			# print '---------'
			# print '---------'

			# print lst_pz
			# print '---------'
			# print   '11f = ',g+h, 'g = ',g, 'h = ',h, 'parent = ',parents,'\nz = ',z,'len = ', len(opened)
			# print '---------'
			# print_pos(opened[z])
			# print '---------'
			opened[z][0] = g + h
			opened[z][1] = g
			opened[z][2] = h
			opened[z][3] = parents
			opened[z][5] = act

			# print_pos(opened[z])
			# print 'g<opened'
			# exit(1)
		

def new_variants(opened, closed, flg):
	# global ss 
	# ss += 1
	# print ss

	# print 'new_variants'
	# raw_input('\n1: ')
	last_act = -1
	
	if len(opened) == 0:
		# print '\n\nNO opened'
		# print closed
		lst_now = closed[-1][4].copy()
		g_now = closed[-1][1]
		parents_from_c_to_o = 0
		# raw_input(':->')
	else:
		
		# print '-------'
		# print 'OPENED'
		# for i in opened:
		# 	print i[4], '\nf=',i[0], 'g=',i[1], 'h=',i[2], 'parent=',i[3]
		# print '-------'
		# print 'CLOSED'
		# for i in closed:
		# 	print i[4], '\nf=',i[0], 'g=',i[1], 'h=',i[2], 'parent=',i[3]

		pos, min_f, last_act = show_minimal(opened)
		lst_now = opened[pos][4].copy()
		g_now = opened[pos][1]
		if have_this_in_closed(closed, opened[pos][4]) == True:
			print 'WE HAVE BITCH'
			exit()
		closed_append(closed = closed, lst_pz = opened[pos][4], parents = opened[pos][3], g = opened[pos][1], h = opened[pos][2])
		
		# print 'pos', pos, 'min_f = ',min_f, 'last_act = ', last_act,'\n'
		opened = opened[0:pos] + opened[pos + 1:]
		
		# print '\nOPENED'
		# for i in opened:
		# 	print i[4], '\nf=',i[0], 'g=',i[1], 'h=',i[2], 'parent=',i[3]

		# print '-------'
		# print 'CLOSED'
		# for i in closed:
		# 	print i[4], '\nf=',i[0], 'g=',i[1], 'h=',i[2], 'parent=',i[3]
		parents_from_c_to_o = len(closed) - 1

	# raw_input('2: ')
	# print '\n_--_'
	# print lst_now
	# print '_--_'
	# print 'g_now = ', g_now,'\n'
	
	
	lst_now = closed[-1][4]
	if last_act != 2:
		status, lst_r = variant(lst_now.copy(), frst_digit, 'r')
		if status:#and have_close
			if have_this_in_closed(closed, lst_r) == False:
				# print 'r', lst_r
				if flg == 0:
					h = heuristic_MH(lst_r, lst_must, frst_digit)
				elif flg == 1:
					h = heuristic_MH_h_v(lst_r, lst_must, frst_digit)
				if h == 0:
					print_answer(closed, lst_r, lst_now, parents_from_c_to_o)
					return
				# print 'g = ',g_now + 1, 'h = ', h
				opened_append(closed = closed, opened = opened, lst_pz = lst_r, parents = parents_from_c_to_o, g = g_now + 1, h = h, act = 1)
	# 		else:
	# 			print 'r closed'
	# 	else:
	# 		print 'r status'
	# else:
	# 	print 'r last'

	if last_act != 1:
		status, lst_l = variant(lst_now.copy(), frst_digit, 'l')
		if status:#and have_close
			if have_this_in_closed(closed, lst_l) == False:
				# print 'l', lst_l
				if flg == 0:
					h = heuristic_MH(lst_l, lst_must, frst_digit)
				elif flg == 1:
					h = heuristic_MH_h_v(lst_l, lst_must, frst_digit)
				if h == 0:
					print_answer(closed, lst_l, lst_now, parents_from_c_to_o)
					return
				# print 'g = ',g_now + 1, 'h = ', h
				opened_append(closed = closed, opened = opened, lst_pz = lst_l, parents = parents_from_c_to_o, g = g_now + 1, h = h, act = 2)
	# 		else:
	# 			print 'l closed'
	# 	else:
	# 		print 'l status'
	# else:
	# 	print 'l last'

	if last_act != 4:
		status, lst_d = variant(lst_now.copy(), frst_digit, 'd')
		if status:#and have_close
			if have_this_in_closed(closed, lst_d) == False:
				# print 'd', lst_d
				if flg == 0:
					h = heuristic_MH(lst_d, lst_must, frst_digit)
				elif flg == 1:
					h = heuristic_MH_h_v(lst_d, lst_must, frst_digit)
				if h == 0:
					print_answer(closed, lst_d, lst_now, parents_from_c_to_o)
					return
				# print 'g = ',g_now + 1, 'h = ', h
				opened_append(closed = closed, opened = opened, lst_pz = lst_d, parents = parents_from_c_to_o, g = g_now + 1, h = h, act = 3)
	# 		else:
	# 			print 'd closed'
	# 	else:
	# 		print 'd status'
	# else:
	# 	print 'd last'

	if last_act != 3:
		status, lst_u = variant(lst_now.copy(), frst_digit, 'u')
		if status:#and have_close and have_open
			if have_this_in_closed(closed, lst_u) == False:
				# print 'u', lst_u
				if flg == 0:
					h = heuristic_MH(lst_u, lst_must, frst_digit)
				elif flg == 1:
					h = heuristic_MH_h_v(lst_u, lst_must, frst_digit)
				if h == 0:
					
					print_answer(closed, lst_u, lst_now, parents_from_c_to_o)
					return
				# print 'g = ',g_now + 1, 'h = ', h
				opened_append(closed = closed, opened = opened, lst_pz = lst_u, parents = parents_from_c_to_o, g = g_now + 1, h = h, act = 4)
	# 		else:
	# 			print 'u closed'
	# 	else:
	# 		print 'u status'
	# else:
	# 	print 'u last'



	
	new_variants(opened, closed, flg)

def print_answer(opened, lst,lst_now, parents):

	new_lst = []
	new_lst.append(lst)
	while parents != -1:
		new_lst.append(closed[parents][4])
		# print '_____'
		# print 'p = ', parents
		# print closed[parents][4]
		# print '\n'
		parents = closed[parents][3]

	n = len(new_lst) - 1
	n2 = len(new_lst) - 1
	while n >= 0:
		print -(n - n2)
		print new_lst[n]
		print
		n -= 1


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



if __name__ == "__main__":

	
	lst_pz, frst_digit = parsing_arg()
	lst_pz = np.reshape(lst_pz, (frst_digit, frst_digit))
	lst_must = return_correct_lst(frst_digit)

	# k = return_zero_c(lst_pz, frst_digit)
	# print 'k = ',k
	# exit()


	if np.array_equal(lst_pz, lst_must):
		print 'Error 55: correct puzzle'
		sys.exit(1)

	if can_solved(lst_pz,lst_must , frst_digit) == False:
		print 'Error 65: Unsolved puzzle'
		sys.exit(1)

	# print '||||||||'
	# print lst_pz
	# print '||||||||\n'
	
	solved = False
	unsolved = False


	closed = []
	opened = []
	
	parents_c = -1
	parents_from_c_to_o = 0

	ss = 0
	closed_append(closed, lst_pz, parents = parents_c, g = 0, h = heuristic_MH(lst_pz, lst_must, frst_digit))#start
	t0 = time()
	new_variants(opened, closed,1)
	t1 = time()
	print 'time solved %f' %(t1-t0)

	# print closed[0]
	# print '___'
	# print opened[0]
	# print '___'
	# print opened[1]




# def can_solved(lst_pz, lst_must, size):
# 	print lst_pz, '\n',size
# 	nums = (size * size) - 1
# 	sums = 0
# 	while nums > 0:

# 		yes = False
# 		k = 0
# 		up = 0
# 		left = 0
# 		right = size
# 		down = size
# 		maxx = (size ** 2)
# 		i = 1
# 		while i < maxx:
# 			y2 = up
# 			x2 = left
			
# 			k += 1
# 			while x2 < right and i < maxx:
# 				if lst_pz[y2][x2] == nums:
# 					yes = True
# 				if yes and lst_pz[y2][x2] > 0 and lst_pz[y2][x2] < nums:
# 					sums += 1
# 				x2 += 1
# 				i += 1

# 			x2 -= 1
# 			y2 += 1
# 			up += 1
# 			# if yes and lst_pz[y2][x2] > 0 and lst_pz[y2][x2] < nums:
# 			# 	sums += 1

# 			while y2 < down and i < maxx:
# 				if lst_pz[y2][x2] == nums:
# 					yes = True
# 				if yes and lst_pz[y2][x2] > 0 and lst_pz[y2][x2] < nums:
# 					sums += 1
# 				y2 += 1
# 				i += 1
# 			y2 -= 1
# 			x2 -= 1
# 			right -= 1
# 			# if yes and lst_pz[y2][x2] > 0 and lst_pz[y2][x2] < nums:
# 			# 	sums += 1

# 			k += 1
# 			while  x2 >= left and i < maxx:
				
# 				if lst_pz[y2][x2] == nums:
# 					yes = True
# 				if yes and lst_pz[y2][x2] > 0 and lst_pz[y2][x2] < nums:
# 					sums += 1
# 				x2 -= 1
# 				i += 1
# 			x2 += 1
# 			y2 -= 1
# 			down -= 1
# 			# if yes and lst_pz[y2][x2] > 0 and lst_pz[y2][x2] < nums:
# 			# 	sums += 1

# 			k += 1
# 			while y2 >= up and i < maxx:
# 				if lst_pz[y2][x2] == nums:
# 					yes = True
# 				if yes and lst_pz[y2][x2] > 0 and lst_pz[y2][x2] < nums:
# 					sums += 1
# 				i += 1
# 				y2 -= 1
			
# 			y2 += 1
# 			x2 += 1
# 			left += 1
# 			# if yes and lst_pz[y2][x2] > 0 and lst_pz[y2][x2] < nums:
# 			# 	sums += 1

# 		print 'nums = ',nums, sums
# 		nums -= 1
# 	# k = return_zero_c(lst_pz, size)
# 	# x0, y0 = np.nonzero(lst_pz == 0)
# 	# x0 = x0[0]
# 	# y0 = y0[0]

# 	# xm0, ym0 = np.nonzero(lst_must == 0)
# 	# xm0 = xm0[0]
# 	# ym0 = ym0[0]


# 	# pox = x0 - xm0
# 	# poy = y0 - ym0
# 	# if pox < 0: pox = -pox
# 	# if poy <= 0: poy = -poy
# 	# k = pox	+ poy
# 	# h = heuristic_MH(lst_pz, lst_must, size)
# 	# print 'h=',h
# 	# print '->',(k + h)%2
# 	# print 'str = ',x0
# 	# print 'k = ', k
# 	print 'sums = ', sums
# 	print sums % 2, 'sums % 2'  
# 	# print ((sums + k) % 2), 'sums + k % 2'
# 	# print ((sums + x0) % 2), 'sums + x0 % 2'

# 	# print sums % 2

# 	# sums = sums + k
# 	# print '-> ',sums % 2


# def return_zero_c(lst_pz, size):###delete

# 	# print lst_pz
# 	k = 0
# 	up = 0
# 	left = 0
# 	right = size
# 	down = size
# 	maxx = (size ** 2)
# 	i = 1
# 	while i < maxx:
# 		y2 = up
# 		x2 = left
		
# 		k += 1
# 		while x2 < right and i < maxx:
# 			if lst_pz[y2][x2] == 0:
# 				# print 1
# 				return k
# 			# else:
# 			# 	print y2, x2, 'ok',lst_pz[y2][x2] 
# 			x2 += 1
# 			i += 1
# 		# print 'was k =',k
# 		# print x2, y2,'\n'
# 		x2 -= 1
# 		y2 += 1
# 		up += 1
# 		if lst_pz[y2][x2] == 0:
# 			# print 11
# 			return k + 1

# 		k += 1
# 		while y2 < down and i < maxx:
# 			if lst_pz[y2][x2] == 0:
# 				# print 2
# 				return k
# 			# else:
# 			# 	print y2, x2, 'ok',lst_pz[y2][x2] 
# 			y2 += 1
# 			i += 1
# 		# print 'was k =',k
# 		# print x2, y2,'\n'
# 		y2 -= 1
# 		x2 -= 1
# 		right -= 1
# 		if lst_pz[y2][x2] == 0:
# 			# print 21
# 			return k + 1

	
# 		k += 1
# 		while  x2 >= left and i < maxx:
			
# 			if lst_pz[y2][x2] == 0:
# 				# print 3
# 				return k
# 			# else:
# 			# 	print y2, x2, 'ok',lst_pz[y2][x2] 
			
# 			x2 -= 1
# 			i += 1
# 		# print 'was k =',k
# 		# print x2, y2,'\n'
# 		x2 += 1
# 		y2 -= 1
# 		down -= 1
# 		if lst_pz[y2][x2] == 0:
# 			# print 31
# 			return k + 1


# 		k += 1
# 		while y2 >= up and i < maxx:
# 			if lst_pz[y2][x2] == 0:
# 				# print 4
# 				return k
# 			# else:
# 			# 	print y2, x2, 'ok',lst_pz[y2][x2] 
# 			i += 1
# 			y2 -= 1
# 		# print 'was k =',k
# 		# print x2, y2,'\n'
# 		y2 += 1
# 		x2 += 1
# 		left += 1

# 		if lst_pz[y2][x2] == 0:
# 			# print 41
# 			return k + 1
# 		# print
# 	# print 'end'
# 	return k