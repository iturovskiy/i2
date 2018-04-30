import ply.yacc as yacc
import i2_lexer as lexer

tokens = lexer.tokens

precedence = (
    ('left', 'ADD', 'SUB')
)

parser = yacc.yacc()
