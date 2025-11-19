# aula4.0.py
from lark import Lark

grammar = """
start: sign? intervals

sign: PLUS
    | MINUS

intervals: intervals interval
        | interval


interval: "[" num ";" lista_num "]"

lista_num: num ";" lista_num
        | num

num: FLOAT 
    | INT

PLUS: "+"
MINUS: "-"

FLOAT: /[+-]?\d+\.\d+/
INT:   /[+-]?\d+/

%import common.WS
%ignore WS
"""

parser = Lark(grammar, start="start")

def run_parser(data):
  """
  Lark parser with doctests.

  >>> run_parser('+[-1.5 ; +2] [3 ; +4.7]')
  Tree(start, [Tree(plus, []), Tree(intervals, [Tree(interval, [Tree(lista_num, [Tree(numero, [Token(FLOAT, '-1.5')]), Tree(numero, [Token(INT, '+2')])])]), Tree(interval, [Tree(lista_num, [Tree(numero, [Token(INT, '3')]), Tree(numero, [Token(FLOAT, '+4.7')])])])])])

  >>> run_parser("-[3 ; 3.5; 4] [5 ; 12] [48 ; 73.2]")
  Tree(start, [Tree(minus, []), Tree(intervals, [Tree(interval, [Tree(lista_num, [Tree(numero, [Token(INT, '3')]), Tree(numero, [Token(FLOAT, '3.5')]), Tree(numero, [Token(INT, '4')])])]), Tree(interval, [Tree(lista_num, [Tree(numero, [Token(INT, '5')]), Tree(numero, [Token(INT, '12')])])]), Tree(interval, [Tree(lista_num, [Tree(numero, [Token(INT, '48')]), Tree(numero, [Token(FLOAT, '73.2')])])])])])

  >>> run_parser("[3 ; 3.5] [1 ; 10; 12] [48 ; 73.2]")
  Tree(start, [Tree(intervals, [Tree(interval, [Tree(lista_num, [Tree(numero, [Token(INT, '3')]), Tree(numero, [Token(FLOAT, '3.5')])])]), Tree(interval, [Tree(lista_num, [Tree(numero, [Token(INT, '1')]), Tree(numero, [Token(INT, '10')]), Tree(numero, [Token(INT, '12')])])]), Tree(interval, [Tree(lista_num, [Tree(numero, [Token(INT, '48')]), Tree(numero, [Token(FLOAT, '73.2')])])])])])

  >>> run_parser("+[3 ; 3.5] [2 ; 1] [0.5 ; -73.2]")
  Tree(start, [Tree(plus, []), Tree(intervals, [Tree(interval, [Tree(lista_num, [Tree(numero, [Token(INT, '3')]), Tree(numero, [Token(FLOAT, '3.5')])])]), Tree(interval, [Tree(lista_num, [Tree(numero, [Token(INT, '2')]), Tree(numero, [Token(INT, '1')])])]), Tree(interval, [Tree(lista_num, [Tree(numero, [Token(FLOAT, '0.5')]), Tree(numero, [Token(FLOAT, '-73.2')])])])])])
  """
  return print(parser.parse(data).pretty())

import doctest
doctest.run_docstring_examples(run_parser, globals())