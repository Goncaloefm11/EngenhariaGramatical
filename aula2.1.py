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

precedence = (
    ('right', 'IMPLI', 'EQUIV'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NEG'),
)

def p_var(p):
    "expression : VAR"
    p[0] = assignment[p[1]]

def p_neg(p):
    "expression : NEG expression"
    p[0] = not p[2]

def p_and(p):
    "expression : expression AND expression"
    p[0] = (p[1] and p[3])

def p_or(p):
    "expression : expression OR expression"
    p[0] = (p[1] or p[3])

def p_impli(p):
    "expression : expression IMPLI expression"
    p[0] = (not p[1]) or p[3]

def p_equiv(p):
    "expression : expression EQUIV expression"
    p[0] = p[1] == p[3]

def p_true(p):
    "expression : TRUE"
    p[0] = True

def p_false(p):
    "expression : FALSE"
    p[0] = False

def p_parens(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_error(p):
    raise SyntaxError("Erro de sintaxe")

def run_parser(data, asg):
  """
  PLY parser with doctests.

  >>> print(run_parser("Frio ∧ ¬Chove", {"Frio":True, "Chove": True}))
  False
  >>> print(run_parser("Noite ∨ ¬Noite", {"Noite":True, "Dia": False}))
  True
  >>> print(run_parser("A ∧ ¬B ∨ ⊤", {"A":True, "B": True}))
  True
  >>> print(run_parser("Reprovar → (¬Presenca ∨ Negativa)", {"Presenca":True, "Negativa": False, "Reprovar": False}))
  True
  >>> print(run_parser("A ∧ (X ∧ ¬Y)", {"A":True, "X": False, "Y": True}))
  False
  """
  global assignment # not good: hack to run inside notbook
  assignment = asg
  return yacc.yacc(write_tables=False, debug=True).parse(data)

import doctest
doctest.run_docstring_examples(run_parser, globals())

