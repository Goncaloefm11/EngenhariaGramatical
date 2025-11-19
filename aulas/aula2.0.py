import ply.lex as lex
import ply.yacc as yacc
import os

# Limpar tabelas antigas
try:
    os.remove("parsetab.py")
except FileNotFoundError:
    pass

# ------------- TOKENS -------------
tokens = ('VAR','NEG','AND','OR','IMPLI','EQUIV','TRUE','FALSE')
literals = ('(',')')

t_ignore = ' \t\n'
t_NEG = r'¬'
t_OR = r'∨'
t_AND = r'∧'
t_IMPLI = r'→'
t_EQUIV = r'↔'
t_TRUE = r'⊤'
t_FALSE = r'⊥'

def t_VAR(t):
    r'\w+'
    return t

def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# ------------- PARSER -------------

def p_var(p):
    "expression : VAR"
    p[0] = {p[1]}

def p_neg(p):
    "expression : NEG expression"
    p[0] = p[2]

def p_and(p):
    "expression : expression AND expression"
    p[0] = p[1] | p[3]

def p_or(p):
    "expression : expression OR expression"
    if(p[1] == p[3]):
        p[0] = p[1]
    else:
        p[0] = p[1] | p[3]

def p_impli(p):
    "expression : expression IMPLI expression"
    p[0] = p[1] | p[3]

def p_equiv(p):
    "expression : expression EQUIV expression"
    p[0] = p[1] | p[3]

def p_true(p):
    "expression : TRUE"
    p[0] = set()

def p_false(p):
    "expression : FALSE"
    p[0] = set()

def p_parens(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_error(p):
    raise SyntaxError("Erro de sintaxe")

def run_parser(data):
  """
  PLY parser with doctests.

  >>> print(run_parser("Chove ∧ ¬Frio"))
  {'Chove', 'Frio'}
  >>> print(run_parser("Dia ∨ ¬Dia"))
  {'Dia'}
  >>> print(run_parser("A ∧ ¬B ∨ ⊤"))
  {'A', 'B'}
  >>> print(run_parser("Reprovar → (¬Presenca ∨ Negativa)"))
  {'Presenca', 'Reprovar', 'Negativa'}
  >>> print(run_parser("A ∧ (X ∧ ¬Y) ∨ ⊤"))
  {'A', 'X', 'Y'}
  """
  return yacc.yacc(write_tables=False, debug=True).parse(data)

import doctest
doctest.run_docstring_examples(run_parser, globals())
