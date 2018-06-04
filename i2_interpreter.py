from numpy import array

def ternary_AND(tup1, tup2):
	x1 = tup1[1]
	x2 = tup2[1]
	logtable = {
		'undefined' : ('false', 'undefined', 'undefined'),
		'true' : ('false', 'true', 'undefined'),
		'false' : ('false', 'false', 'false')
	}
	if x2 == 'false':
		index = 0
	if x2 == 'true':
		index = 1
	if x2 == 'undefined':
		index = 2
	return ('BOOL', logtable[x1][index])


def ternary_NAND(tup1, tup2):
	x1 = tup1[1]
	x2 = tup2[1]
	logtable = {
		'undefined': ('true', 'undefined', 'undefined'),
		'true': ('true', 'false', 'undefined'),
		'false': ('true', 'true', 'true')
	}
	if x2 == 'false':
		index = 0
	if x2 == 'true':
		index = 1
	if x2 == 'undefined':
		index = 2
	return ('BOOL', logtable[x1][index])


def ternary_OR(tup1, tup2):
	x1 = tup1[1]
	x2 = tup2[1]
	logtable = {
		'undefined': ('undefined', 'true', 'undefined'),
		'true': ('true', 'true', 'true'),
		'false': ('false', 'true', 'undefined')
	}
	if x2 == 'false':
		index = 0
	if x2 == 'true':
		index = 1
	if x2 == 'undefined':
		index = 2
	return ('BOOL', logtable[x1][index])


def ternary_NOR(tup1, tup2):
	x1 = tup1[1]
	x2 = tup2[1]
	logtable = {
		'undefined': ('undefined', 'false', 'undefined'),
		'true': ('false', 'false', 'false'),
		'false': ('true','false', 'undefined')
	}
	if x2 == 'false':
		index = 0
	if x2 == 'true':
		index = 1
	if x2 == 'undefined':
		index = 2
	return ('BOOL', logtable[x1][index])


def logic_to_arithm(tup):
	if tup[1] == 'true':
		return ('SHORT', 1)
	elif tup[1] == 'false':
		return ('SHORT', -1)
	elif tup[1] == 'undefined':
		return ('SHORT', 0)


def arithm_to_logic(tup):
	if tup[1] >= 1:
		return ('BOOL', 'true')
	elif tup[1] <= -1 :
		return ('BOOL', 'false')
	elif tup[1] == 0:
		return ('BOOL', 'undefined')


class Interpreter:

	def __init__(self, prog):
		self.prog = prog
		self.error = 0
		self.isLabyrinthInit = False
		self.errorList = (
			'Предупреждение: Лабиринт неинициплизирован!',
			'# 1: Отсутствует точка входа в программу.',
			'# 2: Несовпадение типов.',
			'# 3: Неинициализированная переменная.',
			'# 4: Некорректные параметры вызова.'
			'# 5: Несовпадение размерностей vector.'
		)

	def run(self):
		if 'work' not in self.prog:
			print(self.errorList[1])
			self.error = 1
			raise RuntimeError

		if not self._init_labyrinth():
			print(self.errorList[0])

		return self._call_func('work', None)

	# TODO написать здесь инициализацию лабиринта
	def _init_labyrinth(self):

		return False

	def _call_func(self, funcID, funcParams):
		# TODO реализовать здесь sizeof

		localVariables = {}

		# TODO проверить funcParams с тем что должно быть в self.prog[funcID][2]
		# если ошибка - вызвать self.errorList[4]
		# иначе занести их в localVariables

		self._sentencess(self.prog[funcID][3][1],
		                 localVariables)  # ('SENTGROUP', p[2]) -> sentencess = [ ('SENTENCE', p[1]), ... ]
		print()
		print(localVariables)

	def _sentencess(self, sentencess, varsDict):
		for sentence in sentencess:
			if sentence[1] is not None:
				sent = sentence[1]
				if sent[0] == 'INITVARS':
					self.__init_variables(sent, varsDict)

				elif sent[0] == 'EXPRESSION':
					self.__expression(sent, varsDict)

				elif sent[0] == 'DOWHILE':
					self.__do_while(sent, varsDict)

				elif sent[0] == 'IFCOND':
					self.__ifcond(sent, varsDict)

				elif sent[0] == 'CALLFUNC':
					self._call_func(sent[1], sent[2])

				elif sent[0] == 'STD':
					self.__std_func(sent)
			else:
				pass

	def __init_variables(self, sentence, varsDict):
		print(sentence)
		typ = None
		dims = None
		# TODO инициализация вектора
		if type(sentence[1]) is list:
			typ = 'VECTOR'
			expected_type = sentence[1][2].upper()
			dims = sentence[1][1]
			for var in sentence[2]:
				# TODO проверка наличия переменной?
				if var[2] is None and var[3] is not None:
					a = array(var[3])
					if len(a.shape) != dims:
						print(self.errorList[5])
						raise RuntimeError
				# TODO

				elif var[2] is not None:
					if len(var[2]) != dims:
						print(self.errorList[5])
						raise RuntimeError
					sizes = [self.__exps(it, varsDict, sentence[1][2]) for it in var[2]]
					sizess = [i[1] for i in sizes]
					sizess = tuple(sizess)
					result = [sentence[1][2], sizess, None]

					if var[3] is None:
						varsDict[var[1]] = result

					else:
						a = array(var[3])
						if len(a.shape) != dims or a.shape != sizess:
							print(self.errorList[5])
							raise RuntimeError
					# TODO

		else:
			expected_type = sentence[1].upper()
			for var in sentence[2]:
				if var[2] is None:
					varsDict[var[1]] = (expected_type, var[2])
				else:
					if len(var[2]) == 2:
						varsDict[var[1]] = var[2]
					else:
						varsDict[var[1]] = self.__exps(var[2], varsDict, expected_type)

	# TODO: рекурсивно, ога
	def __exps(self, sentence, varDict, expected_type):
		pass

	# TODO: обращение к переменной по минимальному набору символов
	def __expression(self, sentence, varsDict):
		if len(sentence[1]) > 1:
			if sentence[1][1] in varsDict:

				pass
			else:
				print(self.errorList[3])
				raise RuntimeError

		else:
			if sentence[1] in varsDict:
				expected_type = varsDict[var[1]][0]
				varsDict[var[1]] = self.__exps(var[2], varsDict, expected_type)
			else:
				print(self.errorList[3])
				raise RuntimeError

	# TODO:
	def __do_while(self, sentence, varsDict):
		pass

	# TODO:
	def __ifcond(self, sentence, varsDict):
		pass

	# TODO:
	def __std_func(self, sentence):
		if len(sent) == 2:
			if self.isLabyrinthInit:
				# TODO методы лабиринта
				pass
			else:
				print('Error!' + self.errorList[0][8:])
				raise RuntimeError
		else:
			if sent[1].lower() == 'print':
				pass
			else:
				pass
