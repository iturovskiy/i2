import ply.lex as lex
from re import sub

MAX_SHORT = 2**8
MAX_INT = 2**12

# кортеж зарезервированных слов
reserved = (
    'false',            # bconst
    'true',             # bconst
    'undefined',        # bconst
    'right',            # direction
    'left'              # direction
)

# словарь ключевых слов - токены
keywords = {
    'smaller' : 'SMALLER',
    'larger' : 'LARGER',

    'set' : 'SET',
    'add' : 'ADD',
    'sub' : 'SUB',
    'not' : 'NOT',
    'or'  : 'OR',
    'and' : 'AND',

    'int' : 'INT',
    'short' : 'SHORT',
    'bool' : 'BOOL',
    'vector' : 'VECTOR',
    'of' : 'OF',

    'function' : 'FUNCTION',
    'return' : 'RETURN',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do' : 'DO',
    'begin' : 'BEGIN',
    'end' : 'END',

    'lms':'LMS',
    'move':'MOVE',
    'sizeof': 'SIZEOF',
    'print' : 'PRINT'
}

# кортеж токенов
tokens = tuple(keywords.values()) + (
    'ID', 'ICONST', 'SCONST', 'BCONST', 'DIRECTION',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'PIPE',
    'ENDS', 'NEWLINE', 'COMMENT'
)


t_ignore = ' \t'
t_ignore_COMMENT = r'\/\/.*'

t_PIPE = r'\|'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ENDS = r';'


def t_ICONST(t):
    '(\-)?[1-9][0-9]*' # const int
    t.value = int(t.value)
    if abs(t.value) < MAX_INT:
        return t
    else:
        # переполнение - ошибка
        pass


def t_SCONST(t):
    r'(\-)?[S][1-9][0-9]*'
    t.value = sub(r'S', '', t.value)
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
    r'[A-Za-z][A-Za-z0-9]*'
    if t.value in keywords:
        t.type = keywords[t.value]
        return t

    elif t.value in reserved:
        if (t.value == reserved[0] or t.value == reserved[1] or t.value == reserved[2]):
            t.type = 'BCONST'
        if (t.value == reserved[3] or t.value == reserved[4]):
            t.type = 'DIRECTION'
        return t
    elif (str(t.value).lower() in keywords or str(t.value).lower() in reserved):
        # error
        print('Illegal ID %s' %t.value)
    else:
        return t


def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


######################################################################################################


def test(lexer, data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
        if tok.type == 'NEWLINE':
            print()


lexer = lex.lex()

if __name__ == '__main__':
	print()
	test(lexer, '''
	            int A set 1300 add 4; // good
		        move right;
		        bool DD set true;
		        if (pp|5 smaller) then 
		            A set S5;
		        else
		            A set 30;''')
