# -*- coding: utf-8 -*-

import ply.lex  as lex
import ply.yacc as yacc

import i2_lexer

tokens = i2_lexer.tokens


def p_program(p):
	'''program : program func
			   | func'''
	if len(p) == 2 and p[1]:
		p[0] = {}
		if p[1][0] == 'FUNCERROR':
			p[0][0] = [p[1]]
		else:
			p[0][p[1][1]] = p[1]

	elif len(p) == 3:
		p[0] = p[1]
		if p[2][0] == 'FUNCERROR':
			if 0 not in p[0]:
				p[0][0] = [p[2]]
			else:
				p[0][0].append(p[2])

		elif p[2][1] not in p[1]:
			p[0][p[2][1]] = p[2]

		else:
			# error
			if 0 in p[0]:
				p[0][0].append(
					('FUNCERROR', 'FUNCTION WITH THAT ID "%s" ALREADY EXIST at line %s' % (p[2][1], p.lineno(2))))
			else:
				p[0][0] = [('FUNCERROR', 'FUNCTION WITH THAT ID "%s" ALREADY EXIST at line %s'
				            % (p[2][1], p.lineno(2)))]
			p.parser.error += 1


def p_program_error(p):
	'''program : program error
			   | error'''
	if len(p) == 2:
		p[0] = {}
	else:
		p[0] = p[1]
	p[0][0].append(('FUNCERROR', 'NOT FUNC at line %s' % p.lineno(1)))
	print('NOT FUNC SENTENCE at line %s' % p.lineno(1))
	p.parser.error += 1


def p_func(p):
	'''func : FUNCTION ids paramlist sentgroup ENDS'''
	p[0] = ('FUNC', p[2][1], p[3], p[4])


def p_func_error1(p):
	'''func : FUNCTION error paramlist sentgroup ENDS'''
	p[0] = ('FUNCERROR', 'BAD FUNC ID at line %s' % p.lineno(1))
	p.parser.error += 1


def p_func_error2(p):
	'''func : FUNCTION ids error sentgroup ENDS'''
	p[0] = ('FUNCERROR', 'BAD FUNC PARAMS at line %s' % p.lineno(1))
	p.parser.error += 1


def p_func_error3(p):
	'''func : FUNCTION ids paramlist error ENDS'''
	p[0] = ('FUNCERROR', 'BAD FUNC SENTGROUP at line %s' % p.lineno(1))
	p.parser.error += 1


def p_func_error4(p):
	'''func : FUNCTION error'''
	p[0] = ('FUNCERROR', 'TERRIBLE FUNC ERRORS at line %s' % p.lineno(1))


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


def p_vect_type(p):
	'''vect : vect INT
			| vect BOOL
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
				| operator ENDS
				| callfunc ENDS
				| cycle
				| ifcond'''
	p[0] = ('SENTENCE', p[1])


def p_sentence_empty(p):
	'''sentence : ENDS'''
	p[0] = ('SENTENCE', 'EMPTY')


def p_sentence_error(p):
	'''sentence : error'''
	p.parser.error += 1
	p[0] = ('SENTENCE', ('ERR', 'SYNT: SOME TERRIBLE SENTENCE ERROR at line %s' % p.lineno(1)))



def p_cycle(p):
	'''cycle : DO sentgroup WHILE expr ENDS
			 | DO sentence WHILE expr ENDS'''
	p[0] = ('DOWHILE', p[2], p[4])


def p_cycle_error(p):
	'''cycle : DO sentgroup WHILE error
			 | DO sentence WHILE error'''
	p.parser.error += 1
	p[0] = ('ERR', 'SYNT: CYCLE CONDITIONS ERROR at line %s' % p.lineno(1))


def p_cycle_error1(p):
	'''cycle : DO error'''
	p.parser.error += 1
	p[0] = ('ERR', 'SYNT: CYCLE TERRIBLE ERROR at line %s' % p.lineno(1))


def p_initvars(p):
	'''initvars : BOOL initbools
				| INT initints
				| shrt initints
				| vect initvects'''
	p[0] = ('INITVARS', p[1], p[2])


def p_initvars_error(p):
	'''initvars : BOOL error
				| INT error
				| shrt error
				| vect error'''
	p.parser.error += 1
	p[0] = ('ERR', 'SYNT: INIT VARS ERROR at line %s' % p.lineno(1))


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
	'''initvects : initvects COMMA initvect'''
	if type(p[1]) is not list:
	 	p[0] = [p[1]]
	else:
		p[0] = p[1]
	p[0].append(p[3])


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


def p_vectvalues(p):
	'''vectvalues : LBRACE vectels RBRACE'''
	p[0] = p[2]


def p_vectels(p):
	'''vectels : vectel
			   | vectels COMMA vectel'''
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		if p[1] is None:
			p[0] = None
		elif type(p[1][-1]) is not type(p[3]):
			p.parser.error += 1
			p[0] = None
		else:
			p[0] = p[1]
			p[0].append(p[3])


def p_vectel(p):
	'''vectel : expr
			  | vectvalues'''
	p[0] = p[1]


#
def p_operator_move(p):
	'''operator : MOVE
			    | rightm
			    | leftm'''
	p[0] = ('OPERATOR', p[1])


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


#
def p_operator_lms(p):
	'''operator : LMS'''
	p[0] = ('OPERATOR', p[1])


def p_callstd_return(p):
	'''callstd : RETURN expr'''
	p[0] = ('STD', p[1], p[2])


def p_callstd_return_error(p):
	'''callstd : RETURN error'''
	p.parser.error += 1
	p[0] = ('ERR', 'SYNT: BAD RETURN at line %s' % p.lineno(1))


def p_callstd_print(p):
	'''callstd : PRINT expr'''
	p[0] = ('STD', p[1], p[2])


def p_callstd_print_error(p):
	'''callstd : PRINT error'''
	p.parser.error += 1
	p[0] = ('ERR', 'SYNT: BAD PRINT at line %s' % p.lineno(1))


def p_ifcond_simple(p):
	'''ifcond : IF expr THEN sentence
			  | IF expr THEN sentgroup ENDS'''
	p[0] = ('IFCOND', p[2], p[4], None)


def p_ifcond_complex(p):
	'''ifcond : IF expr THEN sentence ELSE sentence
			  | IF expr THEN sentence ELSE sentgroup ENDS
			  | IF expr THEN sentgroup ELSE sentence
			  | IF expr THEN sentgroup ELSE sentgroup ENDS'''
	p[0] = ('IFCOND', p[2], p[4], p[6])


def p_ifcond_error(p):
	'''ifcond : IF error THEN sentence
			  | IF error THEN sentgroup ENDS
			  | IF error THEN sentence ELSE sentence
			  | IF error THEN sentence ELSE sentgroup ENDS
			  | IF error THEN sentgroup ELSE sentence
			  | IF error THEN sentgroup ELSE sentgroup ENDS'''
	p.parser.error += 1
	p[0] = ('ERR', 'SYNT: BAD LOGIC CONDITIONS IN "IF SENTENCE" at line %s' % p.lineno(1))


def p_ifcond_error1(p):
	'''ifcond : IF error'''
	p.parser.error += 1
	p[0] = ('ERR', 'SYNT: TERRIBLE ERROR IN "IF SENTENCE" at line %s' % p.lineno(1))


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


def p_expression_error(p):
	'''expression : ids SET error
				  | vectelem SET error'''
	p.parser.error += 1
	p[0] = ('ERR', 'SYNT: BAD ASSIGNMENT VALUE at line %s' % p.lineno(2))


def p_ids(p):
	'''ids : ID'''
	p[0] = ('ID', p[1])


def p_expr_simple(p):
	'''expr : num
			| operator
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


def p_callfunc_error(p):
	'''callfunc : ids LPAREN error RPAREN'''
	p.parser.error += 1
	p[0] = ('ERR', 'SYNT: BAD FUNC "%s" CALL PARAMS at line %s' % (p[1][1], p.lineno(2)))


def p_callfunc_sizeof_1(p):
	'''callfunc : SIZEOF LPAREN INT RPAREN
				| SIZEOF LPAREN shrt RPAREN
				| SIZEOF LPAREN BOOL RPAREN'''
	p[0] = ('CALLFUNC', p[1], p[3])


def p_callfunc_sizeof_2(p):
	'''callfunc : SIZEOF expr'''
	p[0] = ('CALLFUNC', p[1], p[2])


def p_callfunc_sizeof_error(p):
	'''callfunc : SIZEOF LPAREN error RPAREN'''
	p.parser.error += 1
	p[0] = ('ERR', 'SYNT: BAD FUNC "sizeof" CALL PARAMS at line %s' % p.lineno(1))


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


def p_error(p):
	pass


parser = yacc.yacc()


def parse(data, debug=0):
	parser.error = 0
	try:
		p = parser.parse(data, debug=debug)
	except lex.LexError:
		p = None
	return p


if __name__ == '__main__':

	def lexx(lexer, data):
		lexer.input(data)
		while True:
			tok = lexer.token()
			if not tok:
				break


	lexer = lex.lex(module=i2_lexer)
	print()
	filename1 = 'simple_test.i2'
	filename5 = 'simple_factorial.i2'
	data = open(filename1).read()
	lexx(lexer, data)
	print()
	prog = parse(data, 1)
	if not prog:
	 	print('not prog')
	else:
		f = open('parseresult.out', 'w')
		for key in prog:
			print('%s : %s' % (key, prog[key]))
			if key == 0:
				f.write('FUNC ERRORS:::' + str(prog[key]) + '\n')
			else:
				f.write("('" + str(prog[key][0]) + "', '" + str(prog[key][1]) + "', " + str(prog[key][2]) + ", [\n")
				for sentence in prog[key][3][1]:
					f.write(str(sentence) + '\n')
				f.write('])\n\n')
		f.close()
