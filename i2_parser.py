import ply.yacc as yacc
import i2_lexer as lexer

tokens = lexer.tokens

precedence = (
    ('left', 'ADD', 'SUB')
)

def p_program(p):
    '''program : prograam statement
               | statement'''
    pass


parser = yacc.yacc()
