import ply.lex as lex

MAX_SHORT = 2**8
MAX_INT = 2**12

# кортеж зарезервированных слов
reserved = (
    'smaller',          # cmpare
    'larger',           # cmpare
    'false',            # bool
    'true',             # bool
    'undefined',        # bool
    'right',            # direction
    'left'              # direction
)

# словарь ключевых слов - токены
keywords = {
    'bool' : 'BOOL',
    'int' : 'INT',
    'short' : 'SHORT',
    'vector' : 'VECTOR',

    'set' : 'SET',
    'add' : 'ADD',
    'sub' : 'SUB',
    'not' : 'NOT',
    'or' : 'OR',
    'and' : 'AND',

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
    'ID', 'NUM', 'CMPARE', 'DIRECTION',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'PIPE',
    'ENDL', 'NEWLINE', 'COMMENT'
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
#t_STRING = r'\".*?\"'
t_ENDL = r';'


def t_NUM(t):
    r'\d+'
    t.value = int(t.value)

    if abs(t.value) < MAX_INT:
        if abs(t.value) > MAX_SHORT:
            t.type = 'INT'
        else:
            t.type = 'SHORT'
        return t
    else:
        # error - как обработать?
        pass


def t_ID(t):
    r'[A-Za-z][A-Za-z0-9]*'
    if t.value in keywords:
        t.type = keywords[t.value]
        return t
    elif str(t.value).lower() in reserved:
        if (str(t.value).lower() == reserved[2] or str(t.value).lower() == reserved[3]
            or str(t.value).lower() == reserved[4]):
            t.type = 'BOOL'
        if (str(t.value).lower() == reserved[0] or str(t.value).lower() == reserved[1]):
            t.type = 'CMPARE'
        if (str(t.value).lower() == reserved[5] or str(t.value).lower() == reserved[6]):
            t.type = 'DIRECTION'
        return t
    elif str(t.value).lower() in keywords:
        # error
        print('Illegal ID %s' %t.value)


def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


# тестер
def test(lexer, data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


if __name__ == '__main__':
	lexer = lex.lex() # (module=tokrules)
	test(lexer, '''AD set 1300 add 4; // good\n
		        move right;''')
	print('')
	test(lexer, "short A set 4;")
	print('')
	test(lexer, "short SHORT;")
