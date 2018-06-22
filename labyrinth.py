# -*- coding: utf-8 -*-

bool3 = {
	1: 'true',
	0: 'undefined',
	-1: 'false'
}

class Labyrinth:

	def __init__(self, fname='labymap.lmap'):
		self.filename = fname
		self.labymap = []
		self.robotPosI = None
		self.robotPosJ = None
		self.inited = False
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
				if self.labymap[i][j][-1] == '1':
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
				print_laby(self.labymap)
				print('Выход: [%s][%s]' % (self.robotPosI, self.robotPosJ))
			self.robotPosI -= step
			return bool3[step]
		else:
			return bool3[0]

	def left(self):
		# перемещение по j
		mapp = self.labymap
		i = self.robotPosI
		j = self.robotPosJ
		step = -1
		if mapp[i][j][1] == '0':
			if (self.robotPosJ + step) == -1:
				print('ВЫШЛИ ИЗ ЛАБИРИНТА! УРА')
				print_laby(self.labymap)
				print('Выход: [%s][%s]' % (self.robotPosI, self.robotPosJ))
			self.robotPosJ += step
			return bool3[step]
		else:
			return bool3[0]

	def right(self):
		# перемещение по j
		mapp = self.labymap
		i = self.robotPosI
		j = self.robotPosJ
		step = 1
		if mapp[i][j][3] == '0':
			if (self.robotPosJ + step) == self.elems:
				print('ВЫШЛИ ИЗ ЛАБИРИНТА! УРА')
				print_laby(self.labymap)
				print('Выход: [%s][%s]' % (self.robotPosI, self.robotPosJ))
			self.robotPosJ += step
			return bool3[step]
		else:
			return bool3[0]

	def lms(self):
		i = self.robotPosI
		j = self.robotPosJ
		rad = self.radius + 1
		mod = self.first % 2;
		self.first += 1
		if mod == 0:
			for it in range(rad):
				if (j - it) == 0:
					print('НАШЛИ ВЫХОД ИЗ ЛАБИРИНТА! УРА')
					print_laby(self.labymap)
					print('Выход: [%s][%s]' % (self.robotPosI, self.robotPosJ - it))
					return it
				if self.labymap[i][j - it][1] == '1':
					return -it
		else:
			for it in range(rad):
				if (j + it) == self.elems:
					print('НАШЛИ ВЫХОД ИЗ ЛАБИРИНТА! УРА')
					print_laby(self.labymap)
					print('Выход: [%s][%s]' % (self.robotPosI, self.robotPosJ + it))
					return -it
				if self.labymap[i][j + it][3] == '1':
					return it
		return 0


def print_laby(lab):
	print('--- Labyrinth ---')
	for line in lab:
		print(line)


# just test
def algo(l):
	l.right()
	l.right()
	l.right()
	l.right()
	l.move()
	l.right()
	l.right()
	l.move()
	l.left()
	l.move()
	print('lms:', l.lms())
	# l.left()
	# l.left()
	# l.left()
	# l.left()
	# l.left()
	# l.left()
	return 1


if __name__ == '__main__':
	l = Labyrinth()
	print('robPos:', '[', l.robotPosI, '][', l.robotPosJ, ']', '\n')
	print_laby(l.labymap)
	print()
	algo(l)
