import ply.lex as lex
import ply.lex as lex
import math

# Limpar tabelas antigas
try:
    os.remove("parsetab.py")
except FileNotFoundError:
    pass
# ------------- TOKENS -------------
tokens = ('NUM', 'PONTO', 'MENOS', 'PONTOVIRGULA', 'ESPACO', 'LPAREN', 'RPAREN')

t_ignore = ' \t\n'
t_PONTO = r'\.'
t_MENOS = r'-'
t_PONTOVIRGULA = r';'
t_ESPACO = r' '
t_LPAREN = r'\['
t_RPAREN = r'\]'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t 

def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

def run_lexer(data):
    """
    PLY lexer with doctests.

    >>> print([(tok.type, tok.value) for tok in run_lexer('[-1.5 ; +2] [3 ; +4.7]')])
    [('[', '['), ('NUM', -1.5), (';', ';'), ('NUM', 2.0), (']', ']'), ('[', '['), ('NUM', 3.0), (';', ';'), ('NUM', 4.7), (']', ']')]
    >>> print([(tok.type, tok.value) for tok in run_lexer("[3 ; 3.5] [5 ; 12] [48 ; 73.2]")])
    [('[', '['), ('NUM', 3.0), (';', ';'), ('NUM', 3.5), (']', ']'), ('[', '['), ('NUM', 5.0), (';', ';'), ('NUM', 12.0), (']', ']'), ('[', '['), ('NUM', 48.0), (';', ';'), ('NUM', 73.2), (']', ']')]
    >>> print([(tok.type, tok.value) for tok in run_lexer("[3 ; 3.5] [1 ; 12] [48 ; 73.2]")])
    [('[', '['), ('NUM', 3.0), (';', ';'), ('NUM', 3.5), (']', ']'), ('[', '['), ('NUM', 1.0), (';', ';'), ('NUM', 12.0), (']', ']'), ('[', '['), ('NUM', 48.0), (';', ';'), ('NUM', 73.2), (']', ']')]
    >>> print([(tok.type, tok.value) for tok in run_lexer("[3 ; 3.5] [2 ; 1] [0.5 ; -73.2]")])
    [('[', '['), ('NUM', 3.0), (';', ';'), ('NUM', 3.5), (']', ']'), ('[', '['), ('NUM', 2.0), (';', ';'), ('NUM', 1.0), (']', ']'), ('[', '['), ('NUM', 0.5), (';', ';'), ('NUM', -73.2), (']', ']')]
    """

    lexer.input(data)
    return lexer

import doctest
doctest.run_docstring_examples(run_lexer, globals())
