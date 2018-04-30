import ply.lex as lex

MAX_SHORT = 1024

class testLexer:

    # словарь зарезервированных слов
    keywords = {
        'false' : 'FALSE',
        'true' : 'TRUE',
        'undefined' : 'UNDEFINED',
        'bool' : 'BOOL',
        'int' : 'INT',
        'short' : 'SHORT',
        'vector' : 'VECTOR',
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'while': 'WHILE',
        'set' : 'SET',
        'add' : 'ADD',
        'sub' : 'SUB',
        'not' : 'NOT',
        'or' : 'OR',
        'and' : 'AND',
        'function' : 'FUNCTION',
        'return' : 'RETURN',
        'do' : 'DO',
        'begin' : 'BEGIN',
        'end' : 'END',
        'vector' : 'VECTOR',
        'lms':'LMS',
        'move':'MOVE',
        'right' : 'RIGHT',
        'left' : 'LEFT',

        'sizeof': 'SIZEOF'
    }

    # токены
    tokens = list(keywords.values()) + [
        'ID', 'NUM', 'LT', 'GT', 'LE', 'GE',
        'LPAREN', 'RPAREN', 'LSBRACKET', 'RSBRACKET',
        'ENDL', 'NEWLINE', 'COMMENT'
    ]

    t_ignore = ' \t'
    t_ignore_COMMENT = r'\/\/.*'

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LSBRACKET = r'\['
    t_RSBRACKET = r'\]'
    t_LT = r'<'
    t_LE = r'<='
    t_GT = r'>'
    t_GE = r'>='
    t_ENDL = r';'

    def t_NUM(self, t):
        r'\d+'
        t.value = int(t.value)
        if t.value > MAX_SHORT:
            t.type = 'INT'
        else:
            t.type = 'SHORT'
        return t

    def t_ID(self, t):
        r'[A-Za-z][A-Za-z0-9]*'
        if t.value in self.keywords:
            if (t.value == 'true' or t.value =='false' or t.value == 'undefined'):
                t.type = 'BOOL'
                return t
            t.type = self.keywords[t.value]
            return t
        elif str(t.value).lower() in self.keywords:
            print('Illegal ID %s' %t.value)


    def t_NEWLINE(self, t):
        r'\n'
        t.lexer.lineno += 1
        return t

    def t_error(self, t):
        print("Illegal character %s" % t.value[0])
        t.lexer.skip(1)

    # для тестирования
    # Построение лексера
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # тестирование
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


if __name__ == '__main__':

    m = testLexer()
    m.build()

    m.test("AD set 1300 add 4; // good")
    print('')
    m.test("short A set 4;")
    print('')
    m.test("short SHORT;")
