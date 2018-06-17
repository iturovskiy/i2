import ply.lex  as lex
import ply.yacc as yacc

import i2_lexer

tokens = i2_lexer.tokens


def p_program(p):
	'''program : program func
			   | func'''
	if len(p) == 2 and p[1]:
		p[0] = {}
		p[0][p[1][1]] = p[1]
	elif len(p) == 3:
		if p[2][1] not in p[1]:
			p[0] = p[1]
			p[0][p[2][1]] = p[2]
		else:
			# error
			p[0] = None
			p.parser.error = 1


def p_func(p):
	'''func : FUNCTION ids paramlist sentgroup ENDS'''
	p[0] = ('FUNC', p[2][1], p[3], p[4])


def p_func_error(p):
	'''func : FUNCTION error paramlist sentgroup
			| FUNCTION ids error sentgroup
			| FUNCTION ids paramlist error'''
	p[0] = None
	p.parser.error = 1


def p_paramlist(p):
	'''paramlist : LPAREN params RPAREN
				 | LPAREN RPAREN'''
	if len(p) == 4:
		p[0] = ('PARAMLIST', p[2])
	else:
		p[0] = ('PARAMLIST', None)


def p_params(p):
	'''params : params COMMA param
			  | param'''
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1]
		p[0].append(p[3])


def p_param(p):
	'''param : INT ids
		     | shrt ids
		     | BOOL ids
		     | vect ids'''
	p[0] = (p[1], p[2])


def p_vect_v(p):
	'''vect : VECTOR OF
	        | vect VECTOR OF'''
	if len(p) == 4:
		p[0] = p[1]
		p[0][1] += 1
	else:
		p[0] = ['VECT', 1]


def p_vect_int(p):
	'''vect : vect INT
			| vect shrt'''
	p[0] = p[1]
	p[0].append(p[2])


def p_sentgroup(p):
	'''sentgroup : BEGIN sentencess END'''
	p[0] = ('SENTGROUP', p[2])


def p_sentencess(p):
	'''sentencess : sentencess sentence
				  | sentence'''
	if len(p) == 3:
		p[0] = p[1]
		p[0].append(p[2])
	else:
		p[0] = [p[1]]


def p_sentence(p):
	'''sentence : initvars ENDS
				| expression ENDS
				| callstd ENDS
				| callfunc ENDS
				| cycle
				| ifcond'''
	p[0] = ('SENTENCE', p[1])


def p_sentence_empty(p):
	'''sentence : ENDS'''
	p[0] = ('SENTENCE', 'EMPTY')


def p_cycle(p):
	'''cycle : DO sentgroup WHILE expr ENDS
			 | DO sentence WHILE expr ENDS'''
	p[0] = ('DOWHILE', p[2], p[4])


def p_initvars(p):
	'''initvars : BOOL initbools
				| INT initints
				| shrt initints
				| vect initvects'''
	p[0] = ('INITVARS', p[1], p[2])


def p_shrt(p):
	'''shrt : SHORT INT
			| SHORT'''
	p[0] = p[1]


def p_initbools(p):
	'''initbools : initbool
	             | initbools COMMA initbool'''
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1]
		p[0].append(p[3])


def p_initbool(p):
	'''initbool : ids
	            | ids SET expr'''
	if len(p) == 2:
		p[0] = ('BOOLEAN', p[1], None)
	else:
		p[0] = ('BOOLEAN', p[1], p[3])


def p_initints(p):
	'''initints : initint
	            | initints COMMA initint'''
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1]
		p[0].append(p[3])


def p_initint(p):
	'''initint : ids
	           | ids SET expr'''
	if len(p) == 2:
		p[0] = ('INTS', p[1], None)
	else:
		p[0] = ('INTS', p[1], p[3])


def p_initvects(p):
	'''initvects : initvect'''
	p[0] = [p[1]]


def p_initvects_more(p):
	'''initvects : initvects initvect'''
	if type(p[1]) is not list:
	 	p[0] = [p[1]]
	else:
		p[0] = p[1]
	p[0].append(p[2])


def p_initvect_a(p):
	'''initvect : ids dimensions COMMA'''
	p[0] = ('VECTOR', p[1], p[2], None)


def p_initvect_b(p):
	'''initvect : ids SET vectvaluescomma
				 | ids dimensions SET vectvaluescomma'''
	if len(p) == 4:
		p[0] = ('VECTOR', p[1], None, p[3])
	else:
		p[0] = ('VECTOR', p[1], p[2], p[4])


def p_initvect(p):
	'''initvect : ids dimensions
				| ids SET vectvalues
				| ids dimensions SET vectvalues'''
	if len(p) == 3:
		p[0] = ('VECTOR', p[1], p[2], None)
	elif len(p) == 4:
		p[0] = ('VECTOR', p[1], None, p[3])
	else:
		p[0] = ('VECTOR', p[1], p[2], p[4])


def p_dimensions(p):
	'''dimensions : dimension
				  | dimensions dimension'''
	if (len(p) == 2):
		p[0] = [p[1]]
	else:
		p[0] = p[1]
		p[0].append(p[2])


def p_dimension(p):
	'''dimension : LBRACKET expr RBRACKET'''
	p[0] = p[2]


def p_vectvaluescomma(p):
	'''vectvaluescomma : vectvalues COMMA'''
	p[0] = p[1]


def p_vectvalues_coma(p):
	'''vectvalues : vectvalues COMMA vectvalues'''
	p[0] = [p[1]]
	p[0].append(p[3])


def p_vectvalues_vect(p):
	'''vectvalues : LBRACE vectvalue RBRACE
				  | LBRACE vectvalues RBRACE'''
	p[0] = p[2]


def p_vectvalue(p):
	'''vectvalue : expr
				 | vectvalue COMMA expr'''
	if (len(p) == 2):
		p[0] = [p[1]]
	else:
		p[0] = p[1]
		p[0].append(p[3])


def p_callstd_move(p):
	'''callstd : MOVE
			   | rightm
			   | leftm'''
	p[0] = ('STD', p[1])


def p_rightm(p):
	'''rightm : MOVE RIGHT
			  | RIGHT'''
	if len(p) == 3:
		p[0] = p[2]
	else:
		p[0] = p[1]


def p_leftm(p):
	'''leftm : MOVE LEFT
			 | LEFT'''
	if len(p) == 3:
		p[0] = p[2]
	else:
		p[0] = p[1]


def p_callstd_lbs(p):
	'''callstd : LMS'''
	p[0] = ('STD', p[1])


def p_callstd_return(p):
	'''callstd : RETURN expr'''
	p[0] = ('STD', p[1], p[2])


def p_callstd_print(p):
	'''callstd : PRINT expr'''
	p[0] = ('STD', p[1], p[2])


def p_ifcond_simple(p):
	'''ifcond : IF expr THEN sentence
			  | IF expr THEN sentgroup ENDS '''
	p[0] = ('IFCOND', p[2], p[4], None)


def p_ifcond_complex(p):
	'''ifcond : IF expr THEN sentence ELSE sentence
			  | IF expr THEN sentence ELSE sentgroup ENDS
			  | IF expr THEN sentgroup ELSE sentence
			  | IF expr THEN sentgroup ELSE sentgroup ENDS'''
	p[0] = ('IFCOND', p[2], p[4], p[6])


def p_vectelem(p):
	'''vectelem : ids dimensions'''
	p[0] = ('VECTEL', p[1], p[2])


def p_num_int(p):
	'''num : ICONST'''
	p[0] = ('INT', p[1])

def p_num_sh(p):
	'''num : SCONST'''
	p[0] = ('SHORT', p[1])


def p_bool(p):
	'''bool : TRUE
			| FALSE
			| UNDEFINED'''
	p[0] = ('BOOL', p[1])


def p_expression(p):
	'''expression : ids SET expr
				  | vectelem SET expr'''
	p[0] = ('EXPRESSION', p[1], p[2], p[3])


def p_ids(p):
	'''ids : ID'''
	p[0] = ('ID', p[1])


def p_expr_simple(p):
	'''expr : num
			| bool
			| ids
			| callfunc
			| vectelem
			| LPAREN expr RPAREN'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = p[2]


def p_expr_arithm(p):
	'''expr : expr ADD expr
			| expr SUB expr'''
	p[0] = ('ARMEXP', p[1], p[2], p[3])


def p_expr_logic(p):
	'''expr : expr SMALLER expr
			| expr LARGER expr
			| expr AND expr
			| expr OR expr
			| expr nand expr
			| expr nor expr'''
	p[0] = ('LOGEXP', p[1], p[2], p[3])


def p_nand(p):
	'''nand : NOT AND'''
	p[0] = 'nand'


def p_nor(p):
	'''nor : NOT OR'''
	p[0] = 'nor'


def p_callfunc(p):
	'''callfunc : ids callfuncparams'''
	p[0] = ('CALLFUNC', p[1], p[2])


def p_callfunc_sizeof(p):
	'''callfunc : SIZEOF LPAREN INT RPAREN
				| SIZEOF LPAREN shrt RPAREN
				| SIZEOF LPAREN BOOL RPAREN
				| SIZEOF LPAREN num RPAREN
				| SIZEOF LPAREN vectelem RPAREN
				| SIZEOF LPAREN ids RPAREN'''
	p[0] = ('CALLFUNC', p[1], p[3])


def p_callfuncparams(p):
	'''callfuncparams : LPAREN RPAREN
				      | LPAREN callfuncparam RPAREN'''
	if len(p) == 4:
		p[0] = p[2]
	else:
		p[0] = None


def p_callfuncparam(p):
	'''callfuncparam : expr
				     | callfuncparam expr'''
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1]
		p[0].append(p[2])


def p_error(t):
	print("Syntax error at line '%s', token = '%s', value = '%s'" % (t.lexer.lineno, t.type, t.value))


parser = yacc.yacc()


def parse(data, debug=0):
	parser.error = 0
	p = parser.parse(data, debug=debug)#True)
	if parser.error:
		return None
	return p


if __name__ == '__main__':

	def lexx(lexer, data):
		lexer.input(data)
		while True:
			tok = lexer.token()
			if not tok:
				break


	lexer = lex.lex(module=i2_lexer)
	lexer.lineno = 1
	print()
	filename = 'simple.i2'
	data = open(filename).read()
	lexx(lexer, data)
	print()
	prog = parse(data)
	if not prog:
	 	print('not prog')
	else:
		f = open('parseresult.out', 'w')
		for key in prog:
			print('%s : %s' % (key, prog[key]))
			f.write("('" + str(prog[key][0]) + "', '" + str(prog[key][1]) + "', " + str(prog[key][2]) + ", [\n")
			for sentence in prog[key][3][1]:
				f.write(str(sentence) + '\n')
			f.write('])\n\n')
		f.close()
