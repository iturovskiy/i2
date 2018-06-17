from numpy import array

MAX_SHORT = 2 ** 8
MAX_INT = 2 ** 12

SO_INT = 4
SO_SHORT = 2
SO_BOOL = 1

def ternary_AND(tup1, tup2):
	x1 = tup1[1]
	x2 = tup2[1]
	logtable = {
		'undefined': ('false', 'undefined', 'undefined'),
		'true': ('false', 'true', 'undefined'),
		'false': ('false', 'false', 'false')
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
		'false': ('true', 'false', 'undefined')
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
	elif tup[1] <= -1:
		return ('BOOL', 'false')
	elif tup[1] == 0:
		return ('BOOL', 'undefined')


def short_to_int(tup):
	pass


def int_to_short(tup):
	pass


class Interpreter:

	def __init__(self, prog):
		self.prog = prog
		self.isLabyrinthInit = False
		self.errorList = (
			'Предупреждение: Лабиринт неинициализирован! Попытки вызова методов работы с лабиринтом вызовут ошибку.',
			'Ошибка # 1: Отсутствует точка входа в программу.',
			'Ошибка # 2: Несовпадение типов.',
			'Ошибка # 3: Неинициализированная переменная.',
			'Ошибка # 4: Несовпадение размерностей vector.',
			'Ошибка # 5: Некорректные параметры вызова функции.',
			'Ошибка # 6: Вызов неизвестной функции.'
		)
		self.error = 0

	def run(self):
		self.__check_SyntaxError()
		if self.error:
			print()
			print('Total syntax errors have found: ' + str(self.error))
			raise RuntimeError

		if 'work' not in self.prog:
			print(self.errorList[1])
			self.error = 1
			raise RuntimeError

		if not self.__init_labyrinth():
			print(self.errorList[0])

		return self.__call_func('work', None)

	# TODO:
	def __check_SyntaxError(self):
		if 0 in self.prog:
			print('-----FUNCS------')
			self.error += len(self.prog[0])
			for it in self.prog[0]:
				print(it[1])
			print('------SYNTAX-----')

		for func in self.prog:
			if func != 0:
				for sent in self.prog[func][3][1]:
					if sent[1][0] == 'ERR':
						print(sent[1][1])
						self.error += 1

	# TODO инициализация лабиринта
	# перенести в отдельный класс ?
	def __init_labyrinth(self):
		return False

	def __lab_move(self):
		pass

	def __lab_left(self):
		pass

	def __lab_right(self):
		pass

	def __lab_lms(self):
		pass

	def __call_func(self, funcID, funcParams):
		if funcID == 'work':
			pass
		else:
			# TODO проверить funcParams с тем что должно быть в self.prog[funcID][2]
			# TODO если ошибка - вызвать self.errorList[4]
			# TODO иначе занести их в localVariables
			pass

		localVariables = {}

		self.__sentencess(self.prog[funcID][3][1],
		                  localVariables)  # ('SENTGROUP', p[2]) -> sentencess = [ ('SENTENCE', p[1]), ... ]

		print('\nLocals of function "%s":' % funcID)
		for item in localVariables:
			print("%s : %s" % (item, localVariables[item]))

	def __sentencess(self, sentencess, varsDict):
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
					if sent[1] == 'sizeof':
						pass
					else:
						self.__call_func(sent[1], sent[2])

				elif sent[0] == 'STD':
					if sent[1] == 'print':
						if sent[2][0] == 'INT' or sent[2][0] == 'ARMEXP':
							expected_type = 'INT'
						elif sent[2][0] == 'BOOL' or sent[2][0] == 'LOGEXP':
							expected_type = 'BOOL'
						elif sent[2][0] == 'SHORT':
							expected_type = 'SHORT'

						res = self.__exps(sent[2], varsDict, expected_type)
						print(res[1])
					elif sent[1] == 'return':
						if sent[2][0] == 'INT' or sent[2][0] == 'ARMEXP':
							expected_type = 'INT'
						elif sent[2][0] == 'BOOL' or sent[2][0] == 'LOGEXP':
							expected_type = 'BOOL'
						elif sent[2][0] == 'SHORT':
							expected_type = 'SHORT'

						res = self.__exps(sent[2], varsDict, expected_type)
						return res
					else:
						self.__std_func(sent)

				elif sent[0] == 'EMPTY':
					pass

	def __init_variables(self, sentence, varsDict):
		print(sentence)
		dims = None
		# TODO инициализация вектора
		if type(sentence[1]) is list:
			expected_type = sentence[1][2].upper()
			dims = sentence[1][1]
			for var in sentence[2]:
				# TODO проверка наличия переменной?
				if var[2] is None and var[3] is not None:
					a = array(var[3])
					if len(a.shape) != dims:
						print(self.errorList[4])
						raise RuntimeError
				# TODO

				elif var[2] is not None:
					if len(var[2]) != dims:
						print(self.errorList[4])
						raise RuntimeError
					sizes = [(self.__exps(it, varsDict, expected_type)) for it in var[2]]
					print(sizes)
					sizess = [i[1] for i in sizes]
					sizess = tuple(sizess)
					result = [expected_type, sizess, None]  # [тип. (размерность), [значения]]

					if var[3] is None:
						varsDict[var[1]] = result

					else:
						a = array(var[3])
						if len(a.shape) != dims or a.shape != sizess:
							print(self.errorList[4])
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


	def __exps(self, expression, varDict, expected_type):

		if expression[0] == 'ARMEXP':
			par1 = self.__exps(expression[1], varDict, expected_type)
			par2 = self.__exps(expression[3], varDict, expected_type)

			if expression[2] == 'add':
				# TODO: переполнение
				return (expected_type, par1[1] + par2[1])

			elif expression[2] == 'sub':
				# TODO: переполнение
				return (expected_type, par1[1] - par2[1])

		elif expression[0] == 'LOGEXP':

			if expression[2] == 'smaller':
				par1 = self.__exps(expression[1], varDict, 'INT')
				par2 = self.__exps(expression[3], varDict, 'INT')

				if par1[1] < par2[1]:
					return ('BOOL', 'true')
				elif par1[1] == par2[1]:
					return ('BOOL', 'undefined')
				elif par1[1] > par2[1]:
					return ('BOOL', 'false')

			elif expression[2] == 'larger':
				par1 = self.__exps(expression[1], varDict, 'INT')
				par2 = self.__exps(expression[3], varDict, 'INT')

				if par1[0] == 'BOOL':
					par1 = logic_to_arithm(par1)
				if par2[0] == 'BOOL':
					par2 = logic_to_arithm(par2)

				if par1[1] > par2[1]:
					return ('BOOL', 'true')
				elif par1[1] == par2[1]:
					return ('BOOL', 'undefined')
				elif par1[1] < par2[1]:
					return ('BOOL', 'false')

			par1 = self.__exps(expression[1], varDict, expected_type)
			par2 = self.__exps(expression[3], varDict, expected_type)

			if expression[2] == 'and':
				return ternary_AND(par1, par2)

			elif expression[2] == 'nand':
				return ternary_NAND(par1, par2)

			elif expression[2] == 'or':
				return ternary_OR(par1, par2)

			elif expression[2] == 'nor':
				return ternary_NOR(par1, par2)

		elif expression[0] == 'ID':
			if expression in varDict:
				return varDict[expression]
			else:
				print(self.errorList[3])
				raise RuntimeError

		elif expression[0] == 'INT':
			if expected_type == 'BOOL':
				return arithm_to_logic(expression)
			elif expected_type == 'INT':
				return expression
			elif expected_type == 'SHORT':
				# TODO: переполнение
				return ('SHORT', expression[1])

		elif expression[0] == 'SHORT':
			if expected_type == 'BOOL':
				return logic_to_arithm(expression)
			elif expected_type == 'INT':
				# TODO: переполнение
				return ('INT', expression[1])
			elif expected_type == 'SHORT':
				return expression

		elif expression[0] == 'BOOL':
			if expected_type == 'BOOL':
				return expression
			elif expected_type == 'INT' or expected_type == 'SHORT':
				return logic_to_arithm(expression)

		# TODO:
		elif expression[0] == 'VECTEL':
			pass

		elif expression[0] == 'CALLFUNC':
			if expression[1] == 'sizeof':
				if expression[2] is str:
					if expression[2] == 'int':
						return ('SHORT', SO_INT)
					elif expression[2] == 'short':
						return ('SHORT', SO_SHORT)
					elif expression[2] == 'bool':
						return ('SHORT', SO_BOOL)
				elif expression[2] is tuple:
					if expression[2][0] == 'ID':
						return ('SHORT', varDict[expression[2][1]][0])
					elif expression[2][0] == 'VECTEL':
						pass
					elif expression[2][0] == 'INT':
						return ('SHORT', SO_INT)
					elif expression[2][0] == 'SHORT':
						return ('SHORT', SO_SHORT)
			else:
				# TODO:
				if expression[1][1] in self.prog:
					# сравнение
					pass
				else:
					print(self.errorList[6])
					raise RuntimeError


	# TODO: обращение к переменной по минимальному набору символов
	def __expression(self, sentence, varsDict):
		# ID
		if len(sentence[1]) < 3:
			if sentence[1] in varsDict:
				res = self.__exps(sentence[3], varsDict, varsDict[sentence[1]][0])
				# varsDict[sentence[1]] = res
				print(res[0])
				print(varsDict[sentence[1]][0])
				if res[0] == varsDict[sentence[1]][0]:
					varsDict[sentence[1]] = res
				else:
					print(self.errorList[2])
					raise RuntimeError
			else:
				print(self.errorList[3])
				raise RuntimeError

		# VECTEL
		else:
			if sentence[1] in varsDict:
				pass
			# expected_type = varsDict[var[1]][0]
			# varsDict[var[1]] = self.__exps(var[2], varsDict, expected_type)
			else:
				print(self.errorList[3])
				raise RuntimeError

	# TODO:
	def __do_while(self, sentence, varsDict):
		pass

	# TODO:
	def __ifcond(self, sentence, varsDict):
		pass

	def __std_func(self, sentence):
		if self.isLabyrinthInit:
			if sentence[1] == 'move':
				self.__lab_move()
			elif sentence[1] == 'left':
				self.__lab_left()
			elif sentence[1] == 'right':
				self.__lab_right()
			elif sentence[1] == 'lms':
				self.__lab_lms()
		else:
			print('Ошибка # 0:' + self.errorList[0][15:43])
			raise RuntimeError
