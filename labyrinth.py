# -*- coding: utf-8 -*-

# TODO:
class Labyrinth:

	def __init__(self, fname='labymap.lmap'):
		self.filename = fname
		self.labymap = None
		self.inited = False
		self.init_labyrinth()

	# true / false
	def init_labyrinth(self):
		pass

	# true / false / undefined
	def move(self):
		pass

	# true / false / undefined
	def left(self):
		pass

	# true / false / undefined
	def right(self):
		pass

	# INT
	def lms(self):
		pass


def algo(lab):
	pass

if __name__ == '__main__':
	l = Labyrinth()
	print(algo(l))
