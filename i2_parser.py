import ply.yacc as yacc
import i2_lexer as lexer

tokens = lexer.tokens

precedence = (
    ('left', 'ADD', 'SUB')
)


def p_program(p):
    '''program : program statement
               | statement'''

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


def p_program_error(p):
    '''program : error'''
    p[0] = None
    p.parser.error = 1


def p_statement(p):
    '''statement : '''
    pass


parser = yacc.yacc()


def parse(data, debug=0):
	parser.error = 0
	p = parser.parse(data, debug=debug)
	if parser.error:
		return None
	return p
