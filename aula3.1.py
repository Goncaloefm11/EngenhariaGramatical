from lark import Lark, Transformer, v_args

grammar = """
start: expr

expr: expr ADD term
    | expr SUB term
    | term

term: term MUL factor
    | term DIV factor
    | factor

factor: NUMBER
      | SUB factor
      | "(" expr ")"

ADD: "+"
SUB: "-"
MUL: "*"
DIV: "/"

NUMBER: /[0-9]+(\\.[0-9]+)?/

%ignore /[ \t\f]+/
"""

parser = Lark(grammar)
print(parser.parse("(-3.4 * 30) + 20 + -30 * 100").pretty())
print(parser.parse("(10 + 30 + 100) * (1 - 1)").pretty())