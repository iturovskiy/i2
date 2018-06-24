# -*- coding: utf-8 -*-

bool3_int = {
	1: 'true',
	0: 'undefined',
	-1: 'false'
}

bool3_str = {
	'true': 1,
	'undefined': 0,
	'false': -1
}

class Labyrinth:

	def __init__(self, fname='labymap.lmap'):
		self.filename = fname
		self.labymap = []
		self.robotPosI = None
		self.robotPosJ = None
		self.inited = False
		self.ended = False
		self.radius = 5
		self.first = 0
		self.lines = 0
		self.elems = 0
		self.init_labyrinth()

	def init_labyrinth(self):
		try:
			file = open(self.filename, 'r')
		except FileNotFoundError:
			self.inited = False
			return

		for line in file:
			buf = line.split('[')
			buf = ''.join(buf)
			buf = buf.split(']')
			llist = buf[0:-1]
			self.labymap.append(llist)
		file.close()
		self.lines = len(self.labymap)
		self.elems = len(self.labymap[0])
		for i in range(len(self.labymap)):
			for j in range(len(self.labymap[i])):
				if self.labymap[i][j][-1] == '1' or self.labymap[i][j][-1] == 'R':
					self.robotPosI = i
					self.robotPosJ = j
					break

		self.inited = True

	def move(self):
		# перемещение по i
		mapp = self.labymap
		i = self.robotPosI
		j = self.robotPosJ
		step = 0
		if mapp[i][j][0] == '0':
			step = 1
		else:
			step = -1

		if mapp[i][j][2] == '0':
			if (self.robotPosI - step) == -1 or (self.robotPosI - step) == self.lines:
				print('ВЫШЛИ ИЗ ЛАБИРИНТА! УРА')
				print('Выход: [%s][%s]' % (self.robotPosI, self.robotPosJ))
				raise EOFError
				# return bool3_int[-step]
				raise EOFError
			self.robotPosI -= step
			print('m R: [%s][%s]' % (self.robotPosI, self.robotPosJ))
			return bool3_int[step]
		else:
			print('m R: [%s][%s]' % (self.robotPosI, self.robotPosJ))
			return bool3_int[0]

	def left(self):
		# перемещение по j
		mapp = self.labymap
		i = self.robotPosI
		j = self.robotPosJ
		step = -1
		if mapp[i][j][1] == '0':
			if (self.robotPosJ + step) == -1:
				print('ВЫШЛИ ИЗ ЛАБИРИНТА! УРА')
				print('Выход: [%s][%s]' % (self.robotPosI, self.robotPosJ))
				# return bool3_int[-step]
				self.ended = True
				raise EOFError
			self.robotPosJ += step
			print('l R: [%s][%s]' % (self.robotPosI, self.robotPosJ))
			return bool3_int[step]
		else:
			print('l R: [%s][%s]' % (self.robotPosI, self.robotPosJ))
			return bool3_int[0]

	def right(self):
		# перемещение по j
		mapp = self.labymap
		i = self.robotPosI
		j = self.robotPosJ
		step = 1
		if mapp[i][j][3] == '0':
			if (self.robotPosJ + step) == self.elems:
				print('ВЫШЛИ ИЗ ЛАБИРИНТА! УРА')
				print('Выход: [%s][%s]' % (self.robotPosI, self.robotPosJ))
				# return bool3_int[-step]
				self.ended = True
				raise EOFError
			self.robotPosJ += step
			print('r R: [%s][%s]' % (self.robotPosI, self.robotPosJ))
			return bool3_int[step]
		else:
			print('r R: [%s][%s]' % (self.robotPosI, self.robotPosJ))
			return bool3_int[0]

	def lms(self):
		i = self.robotPosI
		j = self.robotPosJ
		rad = self.radius + 1
		mod = self.first % 2;
		self.first += 1
		if mod == 0:
			for it in range(rad):
				if (j - it) == -1:
					print('НАШЛИ ВЫХОД ИЗ ЛАБИРИНТА! УРА')
					print('Выход: [%s][%s]' % (self.robotPosI, self.robotPosJ - it))
					self.ended = True
					return it
				if self.labymap[i][j - it][1] == '1':
					return -it
		else:
			for it in range(rad):
				if (j + it) == self.elems:
					print('НАШЛИ ВЫХОД ИЗ ЛАБИРИНТА! УРА')
					print('Выход: [%s][%s]' % (self.robotPosI, self.robotPosJ + it))
					self.ended = True
					return -it
				if self.labymap[i][j + it][3] == '1':
					return it
		return 0


def print_laby(lab):
	print('--- Labyrinth ---')
	for line in lab:
		print(line)


# простейший алгоритм поиска выхода

def algo_(l):
	rFlag = False
	lFlag = False
	vFlag = False
	vValue = 0
	hValue = 0

	it = 0

	while it <= 1000:

		if rFlag == False and lFlag == False and vFlag == False:
			print(0)
			hValue = l.right()
			if (bool3_str[hValue] == 0):
				rFlag = True

		if rFlag == False and lFlag == False and vFlag == True:
			print(2)
			hValue = l.right()
			if (bool3_str[hValue] == 0):
				rFlag = True
			else:
				vFlag = False

		###
		if rFlag == False and lFlag == True and vFlag == False:
			pass

		###
		if rFlag == False and lFlag == True and vFlag == True:
			pass

		if rFlag == True and lFlag == False and vFlag == False:
			print(1)
			vValue = l.move()
			if bool3_str[vValue] == 0:
				hValue = l.left()
				if bool3_str[hValue] == 0:
					lFlag = True
			else:
				rFlag = False
				vFlag = True

		if rFlag == True and lFlag == False and vFlag == True:
			print(3)
			hValue = l.left()
			if bool3_str[hValue] == 0:
				lFlag = True
			else:
				vFlag = False

		###
		if rFlag == True and lFlag == True and vFlag == True:
			print(5)
			rFlag = False
			vFlag = False
			lFlag = False

		###
		if rFlag == True and lFlag == True and vFlag == False:
			print(4)
			vValue = l.move()
			if bool3_str[vValue] == 0:
				hValue = l.right()
				if bool3_str[hValue] == 0:
					rFlag = True
			else:
				lFlag = False
				vFlag = True

		it += 1


if __name__ == '__main__':
	l = Labyrinth()
	print('robPos:', '[', l.robotPosI, '][', l.robotPosJ, ']', '\n')
	print_laby(l.labymap)
	print()
	try:
		algo_(l)
	except RecursionError:
		print('\n\nINF RECURSION!!!')
	except EOFError:
		print('Alles gut')
