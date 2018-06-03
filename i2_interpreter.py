from i2_lexer import SO_BOOL, SO_INT, SO_SHORT, MAX_SHORT, MAX_INT

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
			'warning: labirinth not initialized',
			'# 1: no program entry point',
			'# 2: incompatible types',
			'# 3: uninitialized variable',
			'# 4: incorrect call params'
		)

	def run(self):
		if 'work' not in self.prog:
			print(self.errorList[1])
			self.error = 1
			raise RuntimeError

		if not self.__init_labyrinth():
			print(self.errorList[0])

		return self.__call_func('work', None)

	# TODO написать здесь инициализацию лабиринта
	def __init_labyrinth(self):

		return False

	def __call_func(self, funcID, funcParams):
		# TODO реализовать здесь sizeof

		localVariables = {}

		# TODO проверить funcParams с тем что должно быть в self.prog[funcID][2]
		# если ошибка - вызвать self.errorList[4]
		# иначе занести их в localVariables

		self.__sentencess(self.prog[funcID][3][1], localVariables) # ('SENTGROUP', p[2]) -> sentencess = [ ('SENTENCE', p[1]), ... ]
		print()
		print(localVariables)

	def __sentencess(self, sentencess, varsDict):
		for sentence in sentencess:
			print(sentence)
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
					self.__call_func(sent[1], sent[2])

				elif sent[0] == 'STD':
					self.__std_func(sent)
			else:
				pass

	def __init_variables(self, sentence, varsDict):
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
				print(self.errorList[0])
		else:
			if sent[1].lower() == 'print':
				pass
			else:
				pass
