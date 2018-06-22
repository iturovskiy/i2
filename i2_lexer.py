# -*- coding: utf-8 -*-

from re import sub

import ply.lex as lex

keywords = {
	'smaller': 'SMALLER',
	'larger': 'LARGER',
	'not': 'NOT',
	'or': 'OR',
	'and': 'AND',

	'set': 'SET',
	'add': 'ADD',
	'sub': 'SUB',

	'int': 'INT',
	'short': 'SHORT',
	'bool': 'BOOL',
	'false': 'FALSE',
	'true': 'TRUE',
	'undefined': 'UNDEFINED',

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
	'right': 'RIGHT',
	'left': 'LEFT',
	'sizeof': 'SIZEOF',
	'print' : 'PRINT'
}

tokens = tuple(keywords.values()) + (
	'ID', 'ICONST', 'SCONST',
	'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'COMMA',
	'ENDS', 'NEWLINE'
)

t_COMMA = r'\,'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ENDS = r';'
t_ANY_ignore = ' \t'


def t_error(t):
	print("Illegal character '%s' at line '%s'" % (t.value[0], t.lexer.lineno))



def t_ICONST(t):
	'((\-)?[1-9][0-9]*)|[0]'
	t.value = int(t.value)
	return t;


def t_SCONST(t):
	r'((\-)?(?i)[S][1-9][0-9]*)|((?i)[S][0])'
	t.value = sub(r'(?i)[S]', '', t.value)
	t.value = int(t.value)
	return t;


def t_ID(t):
	r'[_A-Za-z][_A-Za-z0-9]*'
	t.value = t.value.lower()
	if t.value in keywords:
		t.type = keywords[t.value]
	return t


def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)


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
	filename = 'simple_test.i2'
	data = open(filename).read()
	test(lexer, data)
