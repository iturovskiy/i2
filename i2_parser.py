import ply.yacc as yacc
import i2_lexer as lexer

tokens = lexer.tokens

precedence = (
	('left', 'ADD', 'SUB')
)


# declaration of variable ?

def p_program(p):
	'''program : program func
			   | func'''

	if len(p) == 2 and p[1]:
		p[0] = {}
		line, stat = p[1]
		p[0][line] = stat
	elif len(p) == 3:
		p[0] = p[1]
		if not p[0]:
			p[0] = {}
		if p[2]:
			line, stat = p[2]
			p[0][line] = stat


def p_func(p):
	'''func : FUNCTION ID paramlist sentgroup ENDS'''
	p[0] = ('FUNC', p[2], p[3], p[4])


# что с error'ами делать то?

def p_func_error(p):
	'''func : FUNCTION ID error sentgroup
			| FUNCTION ID paramlist error'''
	p[0] = None
	p.parser.error = 1


def p_paramlist(p):
	'''paramlist : LPAREN params RPAREN
				 | LPAREN RPAREN'''
	if (len(p) == 4):
		p[0] = ('PARAMLIST', p[2])
	else:
		p[0] = ('PARAMLIST', '')


def p_params(p):
	'''params : params COMMA param
			  | var'''
	if (len(p) == 2):
		p[0] = ('PARAMS', p[1])
	else:
		p[0] = ('PARAMS', p[1], p[3])


def p_param(p):
	'''param : INT ID
		     | SHORT ID
		     | vect ID'''
	p[0] = ('PARAM', p[1], p[2])


def p_vect(p):
	'''vect : VECTOR OF
			| vect SHORT
			| vect INT
	        | vect VECTOR OF'''
	if (len(p) == 4):
		p[0] = ('VECT', p[2], p[3])
	else:
		p[0] = ('VECT', p[1], p[2])


def p_sentgroup(p):
	'''sentgroup : BEGIN sentencess END'''
	p[0] = ('SENTGROUP', p[2])


def p_sentencess(p):
	'''sentencess : sentencess sentence
				  | sentence'''
	if (len(p) == 3):
		p[0] = ('SENTENCES', p[1], p[2])
	else:
		p[0] = ('SENTENCES', p[1])


def p_sentence(p):
	'''sentence : initvars ENDS
				| cycle ENDS
				| expr ENDS
				| call ENDS
				| ifcond'''
	p[0] = ('SENTENCE', p[1])


# do while

def p_cycle(t):
	'''cycle : DO sentgroup WHILE boolexp ENDS
			 | DO sentence WHILE boolexp ENDS'''
	p[0] = ('DOWHILE', p[2], p[4])


def p_initvars(p):
	'''initvars : BOOL initbools
				| INT initints
				| SHORT initshorts
				| vect initvect'''
	p[0] = ('', p[1], p[2])


def p_initbools(p):
	'''inibools : ID
	            | fullboolexp
	            | initbools COMMA ID
	            | initbools COMMA fullboolexp'''
	if (len(p) == 2):
		p[0] = ('BOOLEANS', p[1])
	else:
		p[0] = ('BOOLEANS', p[1], p[3])


def p_initints(p):
	'''initints : ID
	            | fullintexp
	            | initints COMMA ID
	            | initints COMMA fullarithmexp'''
	if (len(p) == 2):
		p[0] = ('INTS', p[1])
	else:
		p[0] = ('INTS', p[1], p[3])


def p_initshorts(p):
	'''initshorts : ID
	              | fullshortexp
	              | initshorts COMMA ID
	              | initshorts COMMA fullarithmexp'''
	if (len(p) == 2):
		p[0] = ('SHORTS', p[1])
	else:
		p[0] = ('SHORTS', p[1], p[3])


def p_initvect(p):
	'''initvect : ID dimensions
				| ID dimensions SET vectvalues
				| initvect COMMA ID dimensions
				| initvect COMMA ID dimensions SET vectvalues'''
	pass


def p_dimensions(p):
	'''dimensions : LBRACKET arithmexp RBRACKET
				  | dimensions LBRACKET arithmexp RBRACKET'''
	pass


# vector of int A[5] set { 1, 2, 3, 4, 5};

def p_vectvalues(p):
	'''vectvalues : LBRACE
				  | vectvalues RBRACE
				  ...
				  | '''
	pass


def p_ifcond(p):
	'''cond : IF boolexp sentence
			| IF boolexp sentgroup ENDS
			| IF boolexp sentence ELSE sentence
			| IF boolexp sentence ELSE sentgroup ENDS
			| IF boolexp sentgroup ELSE sentence
			| IF boolexp sentgroup ELSE sentgroup ENDS '''
	pass


def p_error(t):
	print("Syntax error at '%s' at line '%s' at pos '%s'" % (
		t.value, t.lexer.lineno, t.lexer.lexpos - t.lexer.lexposition))


parser = yacc.yacc()


# добавить NEWLINE ???

# fullboolexp -> boolexp
# fullarithmexp -> arithmexp
# expr -> fullboolexp | fullarithmexp
# calls
# stdfunc: move, lbs, print

def parse(data, debug=0):
	parser.error = 0
	p = parser.parse(data, debug=debug)
	if parser.error:
		return None
	return p
