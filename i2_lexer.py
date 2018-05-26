import ply.lex as lex
from re import sub

MAX_SHORT = 2 ** 8
MAX_INT = 2 ** 12

SO_INT = 2
SO_SINT = 1

states = [
	('SHORT', 'exclusive'),
	('MOVE', 'exclusive')
]

# кортеж зарезервированных слов
reserved = (
	'false',  # bconst
	'true',  # bconst
	'undefined'  # bconst
	'right',  # direction
	'left'  # direction
)

# словарь ключевых слов - токены
keywords = {
	'smaller': 'SMALLER',
	'larger': 'LARGER',

	'set': 'SET',
	'add': 'ADD',
	'sub': 'SUB',
	'not': 'NOT',
	'or': 'OR',
	'and': 'AND',

	'int': 'INT',
	'short': 'SHORT',
	'bool': 'BOOL',
	'vector': 'VECTOR',
	'of': 'OF',

	'function': 'FUNCTION',
	'return': 'RETURN',
	'if': 'IF',
	'then': 'THEN',
	'else': 'ELSE',
	'while': 'WHILE',
	'do': 'DO',
	'begin': 'BEGIN',
	'end': 'END',

	'lms': 'LMS',
	'move': 'MOVE',
	'sizeof': 'SIZEOF',
	'print': 'PRINT'
}

# кортеж токенов
tokens = tuple(keywords.values()) + (
	'ID', 'ICONST', 'SCONST', 'BCONST',  # 'DIRECTION',
	'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'COMMA',
	'ENDS', 'NEWLINE', 'COMMENT'
)


############################ State lexing

def t_SHORT(t):
	r'short'
	t.lexer.begin('SHORT')


def t_SHORT_smth(t):
	r'[a-zA-Z\,\;][0-9a-zA-Z]*'
	t.type = 'SHORT'
	t.value = '1'
	t.lexer.begin('INITIAL')
	return t


def t_SHORT_int(t):
	r'int'
	t.value = '2'
	t.type = 'SHORT'
	t.lexer.begin('INITIAL')
	return t


def t_MOVE(t):
	r'move'
	t.lexer.begin('MOVE')


def t_MOVE_left(t):
	r'left'
	t.type = 'MOVE'
	t.value = 'LEFT'
	t.lexer.begin('INITIAL')
	return t


def t_MOVE_right(t):
	r'right'
	t.type = 'MOVE'
	t.value = 'RIGHT'
	t.lexer.begin('INITIAL')
	return t


def t_MOVE_smth(t):
	r'[A-Za-z\;][A-Za-z0-9]*'
	t.type = 'MOVE'
	t.value = 'VERTICAL'
	t.lexer.begin('INITIAL')
	return t


###########################

def t_ANY_error(t):
	t.type = 'ERROR'
	t.value = 404
	# print("Illegal character %s" % t.value[0])
	# t.lexer.skip(1)
	return t


t_ANY_ignore = ' \t'
t_ignore_COMMENT = r'\/\/.*'

t_COMMA = r'\,'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ENDS = r';'


def t_ICONST(t):
	'((\-)?[1-9][0-9]*)|[0]'  # const int
	t.value = int(t.value)
	if abs(t.value) < MAX_INT:
		return t
	else:
		# переполнение - ошибка
		print('Illegal value - overflow')
		pass


def t_SCONST(t):
	r'(\-)?(?i)[S][1-9][0-9]*'
	t.value = sub(r'(?i)[S]', '', t.value)
	t.value = int(t.value)
	if abs(t.value) < MAX_SHORT:
		return t
	elif (MAX_SHORT <= abs(t.value) and abs(t.value) < MAX_INT):
		t.type = 'ICONST'
		return t
	elif (abs(t.value) >= MAX_INT):
		# переполнение - ошибка
		print('Illegal value - overflow')
		pass


def t_ID(t):
	r'[A-Za-z][A-Za-z0-9]*'
	if t.value in keywords:
		t.type = keywords[t.value]
		return t

	if t.value in reserved[0:2]:
		t.type = 'BCONST'
		return t

	if t.value in reserved[3:4]:
		# error
		print('Illegal ID %s' % t.value)

	if (str(t.value).lower() in keywords or str(t.value).lower() in reserved):
		print('Illegal ID %s' % t.value)
	else:
		return t


def t_NEWLINE(t):
	r'\n'
	t.lexer.lineno += 1
	return t


lexer = lex.lex()

if __name__ == '__main__':

	def test(lexer, data):
		lexer.input(data)
		while True:
			tok = lexer.token()
			if not tok:
				break
			print(tok)
			if tok.type == 'NEWLINE':
				print()


	print()
	filename = 'simple.txt'
	data = open(filename).read()
	test(lexer, data)
