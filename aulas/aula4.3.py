from lark import Lark

grammar = r"""
?start: decls expr

decls: decl*

decl: "let" ID "=" expr ";"
    | "let" funcao "=" expr ";"

?funcao: ID "(" params ")"
?params: (ID ("," ID)*)?

?expr: arithexpr
    | "let" ID "=" expr ";" expr

?arithexpr: term
    | arithexpr "*" term   -> multiplicacao

term: INT
    | ID


INT: /0|[1-9][0-9]*/
ID: /[a-zA-Z_][a-zA-Z0-9_]*/
%ignore /[ \t\f\n]+/
"""


def run_parser(data):
    """
    Lark parser with doctests.

    >>> run_parser('x : int \\n if 2 > x or 4 < 9 then 10 else -1*10')
    Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'decl'), [Token('ID', 'x'), Tree(Token('RULE', 'int'), [])]), Tree(Token('RULE', 'ifthenelse'), [Tree(Token('RULE', 'disj'), [Tree(Token('RULE', 'comp'), [Token('INT', '2'), Token('GT', '>'), Tree(Token('RULE', 'var'), [Token('ID', 'x')])]), Token('OR', 'or'), Tree(Token('RULE', 'comp'), [Token('INT', '4'), Token('LT', '<'), Token('INT', '9')])]), Token('INT', '10'), Tree(Token('RULE', 'arithterm'), [Token('INT', '-1'), Token('MUL', '*'), Token('INT', '10')])])])

    >>> run_parser('x : int \\n if 2*2 > x or 4 < 9 then 10 else -1*10')
    Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'decl'), [Token('ID', 'x'), Tree(Token('RULE', 'int'), [])]), Tree(Token('RULE', 'ifthenelse'), [Tree(Token('RULE', 'disj'), [Tree(Token('RULE', 'comp'), [Tree(Token('RULE', 'arithterm'), [Token('INT', '2'), Token('MUL', '*'), Token('INT', '2')]), Token('GT', '>'), Tree(Token('RULE', 'var'), [Token('ID', 'x')])]), Token('OR', 'or'), Tree(Token('RULE', 'comp'), [Token('INT', '4'), Token('LT', '<'), Token('INT', '9')])]), Token('INT', '10'), Tree(Token('RULE', 'arithterm'), [Token('INT', '-1'), Token('MUL', '*'), Token('INT', '10')])])])

    >>> run_parser('x : int \\n p : bool \\n if 2 > 3 or p then 10 else -x*10')
    Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'decls'), [Tree(Token('RULE', 'decl'), [Token('ID', 'x'), Tree(Token('RULE', 'int'), [])]), Tree(Token('RULE', 'decl'), [Token('ID', 'p'), Tree(Token('RULE', 'bool'), [])])]), Tree(Token('RULE', 'ifthenelse'), [Tree(Token('RULE', 'disj'), [Tree(Token('RULE', 'comp'), [Token('INT', '2'), Token('GT', '>'), Token('INT', '3')]), Token('OR', 'or'), Tree(Token('RULE', 'var'), [Token('ID', 'p')])]), Token('INT', '10'), Tree(Token('RULE', 'arithterm'), [Tree(Token('RULE', 'literal'), [Token('SUB', '-'), Tree(Token('RULE', 'var'), [Token('ID', 'x')])]), Token('MUL', '*'), Token('INT', '10')])])])

    >>> run_parser('x : int \\n p : bool \\n if True or x and 10 < 20 then 10 else -1*10*30')
    Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'decls'), [Tree(Token('RULE', 'decl'), [Token('ID', 'x'), Tree(Token('RULE', 'int'), [])]), Tree(Token('RULE', 'decl'), [Token('ID', 'p'), Tree(Token('RULE', 'bool'), [])])]), Tree(Token('RULE', 'ifthenelse'), [Tree(Token('RULE', 'disj'), [Token('BOOL', 'True'), Token('OR', 'or'), Tree(Token('RULE', 'conj'), [Tree(Token('RULE', 'var'), [Token('ID', 'x')]), Token('AND', 'and'), Tree(Token('RULE', 'comp'), [Token('INT', '10'), Token('LT', '<'), Token('INT', '20')])])]), Token('INT', '10'), Tree(Token('RULE', 'arithterm'), [Token('INT', '-1'), Token('MUL', '*'), Token('INT', '10'), Token('MUL', '*'), Token('INT', '30')])])])

    >>> run_parser('x : int \\n p : bool \\n if p then if not p then 10 else x+20 else if p and 20 > 23 then x*x else 50')
    Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'decls'), [Tree(Token('RULE', 'decl'), [Token('ID', 'x'), Tree(Token('RULE', 'int'), [])]), Tree(Token('RULE', 'decl'), [Token('ID', 'p'), Tree(Token('RULE', 'bool'), [])])]), Tree(Token('RULE', 'ifthenelse'), [Tree(Token('RULE', 'var'), [Token('ID', 'p')]), Tree(Token('RULE', 'ifthenelse'), [Tree(Token('RULE', 'neg'), [Token('NOT', 'not'), Tree(Token('RULE', 'var'), [Token('ID', 'p')])]), Token('INT', '10'), Tree(Token('RULE', 'arithexpr'), [Tree(Token('RULE', 'var'), [Token('ID', 'x')]), Token('SUM', '+'), Token('INT', '20')])]), Tree(Token('RULE', 'ifthenelse'), [Tree(Token('RULE', 'conj'), [Tree(Token('RULE', 'var'), [Token('ID', 'p')]), Token('AND', 'and'), Tree(Token('RULE', 'comp'), [Token('INT', '20'), Token('GT', '>'), Token('INT', '23')])]), Tree(Token('RULE', 'arithterm'), [Tree(Token('RULE', 'var'), [Token('ID', 'x')]), Token('MUL', '*'), Tree(Token('RULE', 'var'), [Token('ID', 'x')])]), Token('INT', '50')])])])

    >>> run_parser('20')
    Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'decls'), []), Token('INT', '20')])
    """
    parser = Lark(grammar)
    return parser.parse(data)

import doctest
doctest.run_docstring_examples(run_parser, globals())
