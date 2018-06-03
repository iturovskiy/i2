import ply.lex as lex
import ply.yacc as yacc


MAX_INT = 2 ** 12

keywords = {
	'vector' : 'VECTOR',
	'of' : 'OF',
	'int' : 'INT',
	'set' : 'SET'
}

tokens = tuple(keywords.values()) + (
	'ID', 'NUM',
	'COMMA', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
	'ENDS', 'NEWLINE'
)


def t_ANY_error(t):
	t.type = 'ERROR'
	t.value = 404
	return t

t_ANY_ignore = ' \t'

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_ENDS = r';'
t_COMMA = r','


def t_NUM(t):
	'((\-)?[1-9][0-9]*)|[0]'  # const int
	t.value = int(t.value)
	if abs(t.value) < MAX_INT:
		return t
	else:
		# переполнение - ошибка
		print('Illegal value - overflow')
		pass

def t_ID(t):
	r'[A-Za-z][A-Za-z0-9]*'
	if t.value in keywords:
		t.type = keywords[t.value]
		return t
	else:
		return t


def t_NEWLINE(t):
	r'\n'
	t.lexer.lineno += 1
	t.lexer.lexposition = t.lexer.lexpos


lexer = lex.lex()

def p_program(p):
	'''program : program initvars
			   | initvars'''
	if len(p) == 2 and p[1]:
		p.counter = 1
		p[0] = {}
		p[0][p.counter] = p[1]
		p.counter += 1
	elif len(p) == 3:
		p[0] = p[1]
		if not p[0]:
			p[0] = {}
		if p[2]:
			stat = p[2]
			p[0][p.counter] = stat
			p.counter += 1


def p_vect_v(p):
	'''vect : VECTOR OF
	        | vect VECTOR OF'''
	if (len(p) == 4):
		p[0] = ('VECT', p[1], p[2])
	else:
		p[0] = ('VECT', p[1])


def p_vect_int(p):
	'''vect : vect INT'''
	p[0] = ('VECT', p[1], p[2])



def p_initvars(p):
	'''initvars : vect initvects ENDS''' #NEWLINE'''
	p[0] = ('VARS', p[1], p[2])


def p_initvects(p):
	'''initvects : initvect
				 | initvects COMMA initvect'''
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1]
		p[0].append(p[3])


def p_initvect(p):
	'''initvect : ID dimensions
				| ID SET vectvalues
				| ID dimensions SET vectvalues'''
	if (len(p) == 3):
		p[0] = ('INIVECT', p[1], p[2], None)
	elif (len(p) == 4):
		p[0] = ('INIVECT', p[1], None, p[3])
	else:
		p[0] = ('INIVECT', p[1], p[2], p[4])

#
# def p_initvect_s(p):
# 	'''inivect : ID dimensions COMMA
# 			   | ID SET vectvalues COMMA
# 			   | ID dimensions SET vectvalues COMMA'''
# 	if (len(p) == 4):
# 		p[0] = ('INIVECT', p[1], p[2], None)
# 	elif (len(p) == 5):
# 		p[0] = ('INIVECT', p[1], None, p[3])
# 	else:
# 		p[0] = ('INIVECT', p[1], p[2], p[4])


def p_dimensions(p):
	'''dimensions : dimension
				  | dimensions dimension'''
	if (len(p) == 2):
		p[0] = [p[1]]
	else:
		p[0] = p[1]
		p[0].append(p[2])


def p_dimension(p):
	'''dimension : LBRACKET NUM RBRACKET'''
	p[0] = p[2]


def p_vectvalues_coma(p):
	'''vectvalues : vectvalues COMMA vectvalues'''
	p[0] = [p[1]]
	p[0].append(p[3])


def p_vectvalues_vect(p):
	'''vectvalues : LBRACE vectvalue RBRACE
				  | LBRACE vectvalues RBRACE'''
	p[0] = p[2]


def p_vectvalue(p):
	'''vectvalue : NUM
				 | vectvalue COMMA NUM'''
	if (len(p) == 2):
		p[0] = [p[1]]
	else:
		p[0] = p[1]
		p[0].append(p[3])


def p_error(t):
	print("Syntax error at line '%s', token = '%s', value = '%s'" % (t.lexer.lineno, t.type, t.value))


parser = yacc.yacc()

if __name__ == '__main__':
# vector of vector of vector of int FFF set { { {1,2}, {2,3}, {3, 4} }, { {6,7}, {7,8}, {8,9} } };
# vector of int A[5] set {6, 7, 8, 9, 10};

	def lexx(lexer, data):
		lexer.input(data)
		while True:
			tok = lexer.token()
			if not tok:
				break
			#print(tok)
			#if tok.type == 'ENDS':
			#	print()


	def parse(data, debug=0):
		parser.error = 0
		p = parser.parse(data, debug=1)
		if parser.error:
			return None
		return p


	print()
	filename = 'testvec.i2'
	data = open(filename).read()
	lexx(lexer, data)
	print()

	prog = parse(data)
	if not prog:
	 	print('not prog')
	else:
		#print(prog)
		#print()
		print('--- parse ---')
		for key in prog:
			print(str(key) + ' : '+ str(prog[key]))
