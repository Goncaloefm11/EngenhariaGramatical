from lark import Lark, Transformer

grammar = """
start: decls
decls: decl*                           // zero ou mais 'decl'

decl: LETRA simbolo INT decl              // A : 1 ...
    | LETRA simbolo  decl                 // A :
    | simbolo                          // só um símbolo isolado
    | simbolo decl simbolo            // coisas dentro do parentesis

// 'simbolo' é uma regra que aceita QUALQUER um dos terminais abaixo
simbolo: IMPLY | EQUIV | CONJ | DISJ | NEG | ALL | SOME
       | DOT | TRUE | FALSE | COLON | COMMA | LPAR | RPAR

       
// ---- Terminais ----
LETRA: /[A-Za-z][A-Za-z0-9_]*/
INT: /0|[1-9][0-9]*/

IMPLY: "→"
EQUIV: "↔"
CONJ:  "∧"
DISJ:  "∨"
NEG:   "¬"
ALL:   "∀"
SOME:  "∃"
DOT:   "."
TRUE:  "⊤"
FALSE: "⊥"
COLON: ":"
COMMA: ","
LPAR:  "("
RPAR:  ")"

%import common.WS
%ignore WS
"""
def run_parser(data):
  """
  Lark parser with doctests.

  >>> run_parser("A : 0 B: 0 A() ∧ ¬B()")
  Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'decls'), [Tree(Token('RULE', 'decl'), [Token('PRD', 'A'), Token('INT', '0')]), Tree(Token('RULE', 'decl'), [Token('PRD', 'B'), Token('INT', '0')])]), Tree(Token('RULE', 'conj'), [Tree(Token('RULE', 'application'), [Token('PRD', 'A'), Tree(Token('RULE', 'vars'), [])]), Token('CONJ', '∧'), Tree(Token('RULE', 'neg'), [Token('NEG', '¬'), Tree(Token('RULE', 'application'), [Token('PRD', 'B'), Tree(Token('RULE', 'vars'), [])])])])])

  >>> run_parser("A : 1 ∃ b . A(b)")
  Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'decls'), [Tree(Token('RULE', 'decl'), [Token('PRD', 'A'), Token('INT', '1')])]), Tree(Token('RULE', 'formula'), [Token('SOME', '∃'), Tree(Token('RULE', 'bnd'), [Token('ID', 'b')]), Tree(Token('RULE', 'application'), [Token('PRD', 'A'), Tree(Token('RULE', 'vars'), [Token('ID', 'b')])])])])

  >>> run_parser("A : 1 R : 2 ∀ a . (A(a) → ∃ b . R(a,b))")
  Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'decls'), [Tree(Token('RULE', 'decl'), [Token('PRD', 'A'), Token('INT', '1')]), Tree(Token('RULE', 'decl'), [Token('PRD', 'R'), Token('INT', '2')])]), Tree(Token('RULE', 'formula'), [Token('ALL', '∀'), Tree(Token('RULE', 'bnd'), [Token('ID', 'a')]), Tree(Token('RULE', 'implies'), [Tree(Token('RULE', 'application'), [Token('PRD', 'A'), Tree(Token('RULE', 'vars'), [Token('ID', 'a')])]), Token('IMPLY', '→'), Tree(Token('RULE', 'formula'), [Token('SOME', '∃'), Tree(Token('RULE', 'bnd'), [Token('ID', 'b')]), Tree(Token('RULE', 'application'), [Token('PRD', 'R'), Tree(Token('RULE', 'vars'), [Token('ID', 'a'), Token('ID', 'b')])])])])])])

  >>> run_parser("⊤")
  Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'decls'), []), Tree(Token('RULE', 'constant'), [Token('TRUE', '⊤')])])
  """

  parser = Lark(grammar)
  return parser.parse(data)

import doctest
doctest.run_docstring_examples(run_parser, globals())