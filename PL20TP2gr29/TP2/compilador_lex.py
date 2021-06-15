import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'print': 'PRINT',
    'int': 'INT',
    'read': 'READ',
    'true': 'TRUE',
    'false': 'FALSE',
    'for': 'FOR',
}

tokens = ['CONJ', 'DISJ', 'LOWEREQUAL', 'GREATEQUAL', 'NOTEQUAL', 'EQUALS', 'ID', 'NUM'] + list(reserved.values())
literals = ['!', '{', '}', '>', '<', '(', ')', ',', '+', '-', '*', '/', '=', ';', '[', ']', '%']

t_NUM = r'\d+'
t_EQUALS = r'=='
t_LOWEREQUAL = r'<='
t_GREATEQUAL = r'>='
t_NOTEQUAL = r'!='
t_CONJ = r'&&'
t_DISJ = r'\|\|'

def t_ID(t):
    r'[a-z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

t_ignore = " \n\t"

def t_error(t):
    print('Carater ilegal: ', t.value[0])
    t.lexer.skip(1)

# Controi o lexer
lexer = lex.lex()

