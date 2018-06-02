import ply.lex as lex
from re import sub

MAX_SHORT = 2 ** 8
MAX_INT = 2 ** 12

SO_INT = 4
SO_SHORT = 2
SO_BOOL = 1

states = [
	('MOVE', 'exclusive')
]

# кортеж зарезервированных слов
reserved = (
	'false',
	'true',
	'undefined'
)

# словарь ключевых слов - токены
keywords = {
	'smaller': 'SMALLER',
	'larger': 'LARGER',

	'right' : 'RIGHT',
	'left' : 'LEFT',

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
	'sizeof': 'SIZEOF'
}

# кортеж токенов
tokens = tuple(keywords.values()) + (
	'ID', 'ICONST', 'SCONST', 'BCONST',
	'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'COMMA',
	'ENDS', 'NEWLINE'
)



def t_MOVE(t):
	r'move'
	t.lexer.begin('MOVE')


def t_MOVE_left(t):
	r'left'
	t.type = 'LEFT'
	t.lexer.begin('INITIAL')
	return t


def t_MOVE_right(t):
	r'right'
	t.type = 'RIGHT'
	t.lexer.begin('INITIAL')
	return t


def t_MOVE_ends(t):
	r';'
	t.type = 'MOVE'
	t.value = 'move'
	t.lexer.begin('INITIAL')
	return t



t_COMMA = r'\,'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ENDS = r';'
t_ANY_ignore = ' \t'

def t_ANY_error(t):
	t.type = 'ERROR'
	t.value = 404
	return t



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
	r'((\-)?(?i)[S][1-9][0-9]*)|((?i)[S][0])'
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
	r'[_A-Za-z][_A-Za-z0-9]*'
	if t.value in keywords:
		t.type = keywords[t.value]
		return t
	elif t.value in reserved:
		t.type = 'BCONST'
		return t
	elif (str(t.value).lower() in keywords or str(t.value).lower() in reserved):
		print('Illegal ID %s' % t.value)
	else:
		return t


def t_NEWLINE(t):
	r'\n'
	t.lexer.lineno += 1
	#t.lexer.lexposition = t.lexer.lexpos


lexer = lex.lex()

if __name__ == '__main__':

	def test(lexer, data):
		lexer.input(data)
		while True:
			tok = lexer.token()
			if not tok:
				break
			print(tok)
			if tok.type == 'ENDS':
				print()


	print()
	filename = 'simple.i2'
	data = open(filename).read()
	test(lexer, data)
