import ply.yacc as yacc
import i2_lexer as toks

parser = yacc.yacc(module=toks)
