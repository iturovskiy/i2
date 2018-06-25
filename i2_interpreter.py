# -*- coding: utf-8 -*-

from numpy import array

from labyrinth import Labyrinth

MAX_SHORT = 2 ** 10
MAX_INT = 2 ** 13

SO_INT = 4
SO_SHORT = 2
SO_BOOL = 1

ERROR_LIST = (
	'Предупреждение: Лабиринт неинициализирован! Попытки вызова методов работы с лабиринтом вызовут ошибку.',
	'Ошибка # 1: Отсутствует точка входа в программу.',
	'Ошибка # 2: Несовпадение типов.',
	'Ошибка # 3: Необъявленная переменная.',
	'Ошибка # 4: Несовпадение размерностей vector.',
	'Ошибка # 5: Некорректные параметры вызова функции.',
	'Ошибка # 6: Вызов неизвестной функции.',
	'Ошибка # 7: По миниальной лексеме найдено несколько переменных.',
	'Ошибка # 8: Обращение к вектору как к переменной.',
	'Ошибка # 9: Обращение к неинициализированной переменной.',
	'Ошибка # 10: Переполнение.',
	'Ошибка # 11: Дистигнута максимальная глубина рекурсии.',
	'Ошибка # 12: Вызванная функция ничего не вернула.',
	'Ошибка # 13: Видимо бесконечный цикл.',
)

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


def check_vector_shape(vect):
	ar = array(vect, object)
	shapess = ar.shape
	for elm in ar.flat:
		if type(elm) is not tuple:
			shapess = tuple(shapess[0:-1])
			break
	return shapess


def make_size(tup):
	if tup is None:
		i = 0
	else:
		i = 1
		for el in tup:
			i *= el
	return i


def make_index(vecShape, elShape):
	if leng(elShape) != leng(vecShape):
		print(ERROR_LIST[4], 'При попытке обратиться к элементу вектора.')
		raise RuntimeError
	index = 0
	vecSize = make_size(vecShape)
	for i in range(len(vecShape)):
		if elShape[i] >= vecShape[i]:
			print(ERROR_LIST[4], 'Выход за границы вектора.')
			raise RuntimeError
		vecSize /= vecShape[i]
		index += elShape[i] * vecSize
	return int(index)


def leng(obj):
	try:
		q1 = len(obj)
	except:
		q1 = 0
	return q1


class Interpreter:

	def __init__(self, prog):
		self.prog = prog
		self.labyrinth = Labyrinth()
		self.isLabyrinthInit = self.labyrinth.inited
		self.syntErrors = 0

	def run(self):
		self._check_SyntaxError()
		if self.syntErrors:
			print()
			print('Total syntax errors have found: ' + str(self.syntErrors))
			raise RuntimeError

		if 'work' not in self.prog:
			print(ERROR_LIST[1])
			self.syntErrors = 1
			raise RuntimeError

		if not self.isLabyrinthInit:
			print(ERROR_LIST[0])

		return self._call_func('work', None)

	def _check_SyntaxError(self):
		if 0 in self.prog:
			print('-----WRONG FUNCS------')
			self.syntErrors += len(self.prog[0])
			for it in self.prog[0]:
				print(it[1])
			print('-----SYNTAX ERRORS----')

		for func in self.prog:
			if func != 0:
				for sent in self.prog[func][3][1]:
					if sent[1][0] == 'ERR':
						print(sent[1][1])
						self.syntErrors += 1

	def _call_func(self, funcID, funcParams):
		localVariables = {}
		if funcID != 'work':
			params = self.prog[funcID][2][1]
			q1 = leng(params)
			q2 = leng(funcParams)
			if q1 != q2:
				print(ERROR_LIST[5] + " (кол-во принятых != кол-во принмаемых) : " + funcID)
				raise RuntimeError
			else:
				if params is not None:
					for i in range(q1):
						if type(params[i][0]) is str:
							typ = params[i][0].upper()
						else:
							typ = params[i][0]
						if typ != funcParams[i][0]:
							# в принципе, сюда можно добавть преобразование типов и забить на ошибку
							print(ERROR_LIST[5] + funcID)
							raise RuntimeError
						localVariables[params[i][1]] = funcParams[i]

		val = self._sentencess(self.prog[funcID][3][1],
		                       localVariables)  # ('SENTGROUP', p[2]) -> sentencess = [ ('SENTENCE', p[1]), ... ]

		print('\nLocals of function "%s":' % funcID)
		for item in localVariables:
			print("%s : %s" % (item, localVariables[item]))

		return val

	def _sentencess(self, sentencess, varsDict):
		for sentence in sentencess:
			if sentence[1] is not None:
				sent = sentence[1]

				if sent[0] == 'INITVARS':
					self._init_variables(sent, varsDict)

				elif sent[0] == 'EXPRESSION':
					self._expression(sent, varsDict)

				elif sent[0] == 'DOWHILE':
					retval = self._do_while(sent, varsDict)
					if retval is not None:
						return retval

				elif sent[0] == 'IFCOND':
					retval = self._ifcond(sent, varsDict)
					if retval is not None:
						return retval

				elif sent[0] == 'CALLFUNC':
					if sent[1][1] != 'sizeof':
						paramz = []
						if sent[2] is not None:
							for it in sent[2]:
								paramz.append(self._exps(it, varsDict))
							try:
								self._call_func(sent[1][1], paramz.copy())
							except RecursionError:
								print(ERROR_LIST[11])
								raise RuntimeError
						else:
							try:
								self._call_func(sent[1][1], None)
							except RecursionError:
								print(ERROR_LIST[11])
								raise RuntimeError

				elif sent[0] == 'STD':
					if sent[1] == 'print':
						expected_type = None
						if sent[2][0] == 'INT' or sent[2][0] == 'ARMEXP':
							expected_type = 'INT'
						elif sent[2][0] == 'BOOL' or sent[2][0] == 'LOGEXP':
							expected_type = 'BOOL'
						elif sent[2][0] == 'SHORT':
							expected_type = 'SHORT'

						res = self._exps(sent[2], varsDict, expected_type)
						print("PRINTING: %s" % res[1])

					elif sent[1] == 'return':
						expected_type = None
						if sent[2][0] == 'INT' or sent[2][0] == 'ARMEXP':
							expected_type = 'INT'
						elif sent[2][0] == 'BOOL' or sent[2][0] == 'LOGEXP':
							expected_type = 'BOOL'
						elif sent[2][0] == 'SHORT':
							expected_type = 'SHORT'

						res = self._exps(sent[2], varsDict, expected_type)
						return res

				elif sent[0] == 'OPERATOR':
					if self.isLabyrinthInit:
						if sent[1] == 'move':
							self.labyrinth.move()
						elif sent[1] == 'left':
							self.labyrinth.left()
						elif sent[1] == 'right':
							self.labyrinth.right()
						elif sent[1] == 'lms':
							self.labyrinth.lms()
					else:
						print('Ошибка # 0:' + ERROR_LIST[0][15:43])
						raise RuntimeError

				elif sent[0] == 'EMPTY':
					pass

	def _init_variables(self, sentence, varsDict):
		dims = None
		shapess = None
		sizess = None
		# инициализация вектора
		if type(sentence[1]) is list:
			expected_type = sentence[1][2].upper()
			dims = sentence[1][1]
			for var in sentence[2]:
				if var[2] is None and var[3] is not None:
					shapess = check_vector_shape(var[3])
					sizess = make_size(shapess)
					if leng(shapess) != dims:
						print('q', ERROR_LIST[4])
						raise RuntimeError
					result_ar = self.___make_vector(var[3], shapess, varsDict, expected_type)
					result = ['VECTOR', shapess, expected_type, result_ar]

				elif var[2] is not None:
					if len(var[2]) != dims:
						print('z', ERROR_LIST[4])
						raise RuntimeError

					shapess = [self._exps(i, varsDict, 'INT')[1] for i in var[2]]

					shapess = tuple(shapess)
					sizess = make_size(shapess)
					if var[3] is None:
						a = [(expected_type, None) for ite in range(sizess)]
						result_ar = self.___make_vector(a, shapess, varsDict, expected_type)
						result = ['VECTOR', shapess, expected_type, result_ar]
					else:
						shapesv = check_vector_shape(var[3])
						sizesv = make_size(shapesv)
						if sizess != sizesv:
							print('x', ERROR_LIST[4])
							raise RuntimeError
						result_ar = self.___make_vector(var[3], shapess, varsDict, expected_type)
						result = ['VECTOR', shapess, expected_type, result_ar]

				varsDict[var[1]] = result

		# инициализация НЕ вектора
		else:
			expected_type = sentence[1].upper()
			for var in sentence[2]:
				if var[2] is None:
					varsDict[var[1]] = (expected_type, var[2])
				else:
					varsDict[var[1]] = self._exps(var[2], varsDict, expected_type)

	def _exps(self, expression, varsDict, expected_type=None):
		fl_None = False
		if expected_type is None:
			fl_None = True

		if expression[0] == 'ARMEXP':
			if fl_None:
				expected_type = 'INT'

			par1 = self._exps(expression[1], varsDict, expected_type)
			par2 = self._exps(expression[3], varsDict, expected_type)

			if expression[2] == 'add':
				# переполнение
				res = par1[1] + par2[1]
				if expected_type == 'SHORT' and abs(res) >= MAX_SHORT:
					print(ERROR_LIST[10], 'SHORT')
					raise RuntimeError
				elif expected_type == 'INT' and abs(res) >= MAX_INT:
					print(ERROR_LIST[10], 'INT')
					raise RuntimeError
				return (expected_type, res)

			elif expression[2] == 'sub':
				# переполнение
				res = par1[1] - par2[1]
				if expected_type == 'SHORT' and abs(res) >= MAX_SHORT:
					print(ERROR_LIST[10], 'SHORT')
					raise RuntimeError
				elif expected_type == 'INT' and abs(res) >= MAX_INT:
					print(ERROR_LIST[10], 'INT')
					raise RuntimeError
				return (expected_type, res)

		elif expression[0] == 'LOGEXP':
			if fl_None:
				expected_type = 'BOOL'

			if expression[1] == 'FSMALLER':
				par1 = self._exps(expression[2], varsDict, 'INT')
				par2 = self._exps(expression[3], varsDict, 'INT')

				if par1[0] == 'BOOL':
					par1 = logic_to_arithm(par1)
				if par2[0] == 'BOOL':
					par2 = logic_to_arithm(par2)

				if par1[1] < par2[1]:
					return self._exps(('BOOL', 'true'), varsDict, expected_type)
				elif par1[1] == par2[1]:
					return self._exps(('BOOL', 'undefined'), varsDict, expected_type)
				elif par1[1] > par2[1]:
					return self._exps(('BOOL', 'false'), varsDict, expected_type)

			if expression[1] == 'FLARGER':
				par1 = self._exps(expression[2], varsDict, 'INT')
				par2 = self._exps(expression[3], varsDict, 'INT')

				if par1[0] == 'BOOL':
					par1 = logic_to_arithm(par1)
				if par2[0] == 'BOOL':
					par2 = logic_to_arithm(par2)

				if par1[1] > par2[1]:
					return self._exps(('BOOL', 'true'), varsDict, expected_type)
				elif par1[1] == par2[1]:
					return self._exps(('BOOL', 'undefined'), varsDict, expected_type)
				elif par1[1] < par2[1]:
					return self._exps(('BOOL', 'false'), varsDict, expected_type)

			if expression[1] == 'SSMALLER':
				par1 = self._exps(expression[2], varsDict, 'INT')
				par2 = self._exps(expression[3], varsDict, 'INT')

				if par1[0] == 'BOOL':
					par1 = logic_to_arithm(par1)
				if par2[0] == 'BOOL':
					par2 = logic_to_arithm(par2)

				if par2[1] < par1[1]:
					return self._exps(('BOOL', 'true'), varsDict, expected_type)
				elif par2[1] == par1[1]:
					return self._exps(('BOOL', 'undefined'), varsDict, expected_type)
				elif par2[1] > par1[1]:
					return self._exps(('BOOL', 'false'), varsDict, expected_type)

			if expression[1] == 'SLARGER':
				par1 = self._exps(expression[2], varsDict, 'INT')
				par2 = self._exps(expression[3], varsDict, 'INT')

				if par1[0] == 'BOOL':
					par1 = logic_to_arithm(par1)
				if par2[0] == 'BOOL':
					par2 = logic_to_arithm(par2)

				if par2[1] > par1[1]:
					return self._exps(('BOOL', 'true'), varsDict, expected_type)
				elif par2[1] == par1[1]:
					return self._exps(('BOOL', 'undefined'), varsDict, expected_type)
				elif par2[1] < par1[1]:
					return self._exps(('BOOL', 'false'), varsDict, expected_type)

			#############################################################################

			# if expression[2] == 'smaller':
			# 	par1 = self._exps(expression[1], varsDict, 'INT')
			# 	par2 = self._exps(expression[3], varsDict, 'INT')
			#
			# 	if par1[0] == 'BOOL':
			# 		par1 = logic_to_arithm(par1)
			# 	if par2[0] == 'BOOL':
			# 		par2 = logic_to_arithm(par2)
			#
			# 	if par1[1] < par2[1]:
			# 		return self._exps(('BOOL', 'true'), varsDict, expected_type)
			# 	elif par1[1] == par2[1]:
			# 		return self._exps(('BOOL', 'undefined'), varsDict, expected_type)
			# 	elif par1[1] > par2[1]:
			# 		return self._exps(('BOOL', 'false'), varsDict, expected_type)
			#
			# elif expression[2] == 'larger':
			# 	par1 = self._exps(expression[1], varsDict, 'INT')
			# 	par2 = self._exps(expression[3], varsDict, 'INT')
			#
			# 	if par1[0] == 'BOOL':
			# 		par1 = logic_to_arithm(par1)
			# 	if par2[0] == 'BOOL':
			# 		par2 = logic_to_arithm(par2)
			#
			# 	if par1[1] > par2[1]:
			# 		return self._exps(('BOOL', 'true'), varsDict, expected_type)
			# 	elif par1[1] == par2[1]:
			# 		return self._exps(('BOOL', 'undefined'), varsDict, expected_type)
			# 	elif par1[1] < par2[1]:
			# 		return self._exps(('BOOL', 'false'), varsDict, expected_type)

			#############################################################################

			par1 = self._exps(expression[1], varsDict, expected_type)
			par2 = self._exps(expression[3], varsDict, expected_type)

			if expression[2] == 'and':
				return ternary_AND(par1, par2)

			elif expression[2] == 'nand':
				return ternary_NAND(par1, par2)

			elif expression[2] == 'or':
				return ternary_OR(par1, par2)

			elif expression[2] == 'nor':
				return ternary_NOR(par1, par2)

		elif expression[0] == 'ID':
			ID = self.___min_lexem(expression, varsDict)
			if varsDict[ID][0] == 'VECTOR':
				print(ERROR_LIST[8])
				raise RuntimeError
			ret = self._exps(varsDict[ID], varsDict, expected_type)
			if ret[1] is None:
				print(ERROR_LIST[9], expression[1])
				raise RuntimeError
			return ret

		elif expression[0] == 'INT':
			if expected_type == 'BOOL':
				return arithm_to_logic(expression)
			elif expected_type == 'INT' or fl_None:
				if abs(expression[1]) >= MAX_INT:
					print(ERROR_LIST[10], 'INT')
					raise RuntimeError
				return expression
			elif expected_type == 'SHORT':
				if abs(expression[1]) >= MAX_SHORT:
					print(ERROR_LIST[10], 'SHORT')
					raise RuntimeError
				return ('SHORT', expression[1])

		elif expression[0] == 'SHORT':
			if expected_type == 'BOOL':
				return logic_to_arithm(expression)
			elif expected_type == 'INT':
				if abs(expression[1]) >= MAX_INT:
					print(ERROR_LIST[10], 'INT')
					raise RuntimeError
				return ('INT', expression[1])
			elif expected_type == 'SHORT' or fl_None:
				if abs(expression[1]) >= MAX_SHORT:
					print(ERROR_LIST[10], 'SHORT')
					raise RuntimeError
				return expression

		elif expression[0] == 'BOOL':
			if expected_type == 'BOOL' or fl_None:
				return expression
			elif expected_type == 'INT' or expected_type == 'SHORT':
				return logic_to_arithm(expression)

		elif expression[0] == 'VECTEL':
			ID = self.___min_lexem(expression[1], varsDict)
			if varsDict[ID][0] != 'VECTOR':
				print(ERROR_LIST[2], 'Обращение как к вектору для не вектора.')
				raise RuntimeError
			shapess = [self._exps(i, varsDict, 'INT')[1] for i in expression[2]]

			shapess = tuple(shapess)
			index = make_index(varsDict[ID][1], shapess)
			ret = self._exps(varsDict[ID][3].flat[index], varsDict, expected_type)
			if ret[1] is None:
				print(ERROR_LIST[9], expression[1][1], list(shapess))
				raise RuntimeError
			return ret

		elif expression[0] == 'CALLFUNC':
			if expression[1] == 'sizeof':
				if type(expression[2]) is str:
					if expression[2] == 'int':
						return self._exps(('SHORT', SO_INT), varsDict, expected_type)
					elif expression[2] == 'short':
						return self._exps(('SHORT', SO_SHORT), varsDict, expected_type)
					elif expression[2] == 'bool':
						return self._exps(('SHORT', SO_BOOL), varsDict, expected_type)

				elif type(expression[2]) is tuple:
					if expression[2][0] == 'ID':
						return ('SHORT', varsDict[expression[2][1]][0])
					elif expression[2][0] == 'VECTEL':
						vectv = self._exps(expression[2], varsDict)
						if vectv[0] == 'BOOL':
							return self._exps(('SHORT', SO_BOOL), varsDict, expected_type)

						elif vectv[0] == 'INT':
							return self._exps(('SHORT', SO_INT), varsDict, expected_type)

						elif vectv[0] == 'SHORT':
							return self._exps(('SHORT', SO_SHORT), varsDict, expected_type)

					elif expression[2][0] == 'INT':
						return self._exps(('SHORT', SO_INT), varsDict, expected_type)

					elif expression[2][0] == 'SHORT':
						return self._exps(('SHORT', SO_SHORT), varsDict, expected_type)

					elif expression[2][0] == 'BOOL':
						return self._exps(('SHORT', SO_BOOL), varsDict, expected_type)

					elif expression[2][0] == 'VECTOR':
						size = make_size(expression[2][1])
						if vectv[0] == 'BOOL':
							size *= SO_BOOL

						elif vectv[0] == 'INT':
							size *= SO_INT

						elif vectv[0] == 'SHORT':
							size *= SO_SHORT

						return self._exps(('SHORT', size), varsDict, expected_type)
			else:
				if expression[1][1] in self.prog:
					paramz = []
					if expression[2] is not None:
						for it in expression[2]:
							paramz.append(self._exps(it, varsDict))
						try:
							ret = self._call_func(expression[1][1], paramz.copy())
						except RecursionError:
							print(ERROR_LIST[11])
							raise RuntimeError
					else:
						try:
							ret = self._call_func(expression[1][1], None)
						except RecursionError:
							print(ERROR_LIST[11])
							raise RuntimeError

					if ret is None:
						print(ERROR_LIST[12])
						raise RuntimeError
					return ret;
				else:
					print(ERROR_LIST[6], expression[1][1])
					raise RuntimeError

		elif expression[0] == 'OPERATOR':
			if self.isLabyrinthInit:
				if expression[1] == 'move':
					val = self.labyrinth.move()
					return self._exps(('BOOL', val), varsDict, expected_type)

				elif expression[1] == 'left':
					val = self.labyrinth.left()
					return self._exps(('BOOL', val), varsDict, expected_type)

				elif expression[1] == 'right':
					val = self.labyrinth.right()
					return self._exps(('BOOL', val), varsDict, expected_type)

				elif expression[1] == 'lms':
					val = self.labyrinth.lms()
					return self._exps(('SHORT', val), varsDict, expected_type)

			else:
				print('Ошибка # 0:' + ERROR_LIST[0][15:43])
				raise RuntimeError

	def _expression(self, sentence, varsDict):
		# ID
		if len(sentence[1]) < 3:
			ID = self.___min_lexem(sentence[1], varsDict)
			if varsDict[ID][0] == 'VECTOR':
				print(ERROR_LIST[8])
				raise RuntimeError
			res = self._exps(sentence[3], varsDict, varsDict[ID][0])
			if res[0] == varsDict[ID][0]:
				varsDict[ID] = res
			else:
				print(ERROR_LIST[2])
				raise RuntimeError
		# VECTEL
		else:
			ID = self.___min_lexem(sentence[1][1], varsDict)
			expected_type = varsDict[ID][2]
			exps = self._exps(sentence[3], varsDict, expected_type)
			shapeEl = [self._exps(i, varsDict, 'INT')[1] for i in sentence[1][2]]
			shapeEl = tuple(shapeEl)
			vecShape = varsDict[ID][1]
			index = make_index(vecShape, shapeEl)
			vec = varsDict[ID][3]
			vec.flat[index] = exps

	def _do_while(self, sentence, varsDict):
		flag = 1
		good = False
		while flag < MAX_INT:
			if sentence[1][0] == 'SENTGROUP':
				retval = self._sentencess(sentence[1][1], varsDict)
			else:
				retval = self._sentencess([sentence[1]], varsDict)
			if retval is not None:
				return retval
			cond = self._exps(sentence[2], varsDict, 'BOOL')
			if cond[1] != 'true':
				good = True
				break
			flag += 1

		if not good:
			print(ERROR_LIST[13])
			raise RuntimeError

	def _ifcond(self, sentence, varsDict):
		cond = self._exps(sentence[1], varsDict, 'BOOL')
		retval = None
		if cond[1] == 'true':
			if sentence[2][0] == 'SENTGROUP':
				retval = self._sentencess(sentence[2][1], varsDict)
			else:
				retval = self._sentencess([sentence[2]], varsDict)
		elif cond[1] == 'false':
			if sentence[3] is not None:
				if sentence[3][0] == 'SENTGROUP':
					retval = self._sentencess(sentence[3][1], varsDict)
				else:
					retval = self._sentencess([sentence[3]], varsDict)
		if retval is not None:
			return retval

	def ___make_vector(self, vec, expected_shape, varsDict, expected_type):
		sizess = make_size(expected_shape)
		if sizess != array(vec, tuple).size:
			a = [0 for ite in range(sizess)]
			result_ar = array(a, tuple)
			ad = array(vec, tuple)
			ad.shape = ad.size
			i = 0
			t = 0
			if sizess == ad.size / 2:
				while (t < ad.size / 2):
					val = ad[i + 1]
					try:
						val = int(val)
					except:
						pass
					result_ar[t] = tuple([ad[i], val])
					i += 2
					t = int(i / 2)

			elif sizess == ad.size / 3:
				i = 0
				while (t < ad.size / 3):
					llist = [ad[i], ad[i + 1], ad[i + 2]]
					result_ar[t] = tuple(llist)
					i += 3
					t = int(i / 3)

			elif sizess == ad.size / 4:
				i = 0
				while (t < ad.size / 4):
					llist = [ad[i], ad[i + 1], ad[i + 2], ad[i + 3]]
					result_ar[t] = tuple(llist)
					i += 4
					t = int(i / 4)
			result_ar.shape = expected_shape
		else:
			result_ar = array(vec, tuple)

		for t in range(result_ar.size):
			result_ar.flat[t] = self._exps(result_ar.flat[t], varsDict, expected_type)
		return result_ar

	def ___min_lexem(self, tup, varsDict):
		realID = ['ID', None]
		minlex = tup[1]
		ID = ''
		inns = 0
		for key in varsDict:
			if key[1].startswith(minlex):
				ID = key[1]
				if ID == minlex:
					inns = 1
					break
				inns += 1
		if inns == 0:
			print(ERROR_LIST[3])
			raise RuntimeError
		elif inns > 1:
			print(ERROR_LIST[7])
			raise RuntimeError

		realID[1] = ID
		realID = tuple(realID)
		return realID
