from lark import Lark

def run_parser(data):
    """
    Lark parser with doctests.

    >>> run_parser("A ∧ ¬B")
    Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'expr'), [Token('ID', 'A')]), Token('AND', '∧'), Tree(Token('RULE', 'expr'), [Token('NOT', '¬'), Tree(Token('RULE', 'expr'), [Token('ID', 'B')])])])])

    >>> run_parser("A ∧ ¬B")
    Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'expr'), [Token('ID', 'A')]), Token('AND', '∧'), Tree(Token('RULE', 'expr'), [Token('NOT', '¬'), Tree(Token('RULE', 'expr'), [Token('ID', 'B')])])])])

    >>> run_parser("A ∧ ¬B ∨ ⊤")
    Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'expr'), [Token('ID', 'A')]), Token('AND', '∧'), Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'expr'), [Token('NOT', '¬'), Tree(Token('RULE', 'expr'), [Token('ID', 'B')])]), Token('OR', '∨'), Tree(Token('RULE', 'expr'), [Token('FALSE', '⊤')])])])])

    >>> run_parser("A ∧ ¬B ∨ ⊤")
    Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'expr'), [Token('ID', 'A')]), Token('AND', '∧'), Tree(Token('RULE', 'expr'), [Tree(Token('RULE', 'expr'), [Token('NOT', '¬'), Tree(Token('RULE', 'expr'), [Token('ID', 'B')])]), Token('OR', '∨'), Tree(Token('RULE', 'expr'), [Token('FALSE', '⊤')])])])])

    """
    grammar = """
    start: expr

    expr: expr OR expr
        | expr AND expr
        | NOT expr
        | ID
        | TRUE
        | FALSE

    ID: /[A-Za-z]+/
    FALSE: "⊤"
    TRUE: "⊥"

    AND: "∧"
    OR: "∨"
    NOT: "¬"

    %ignore /[ \\t\\f]+/
    """

    parser = Lark(grammar, start="start")
    return parser.parse(data)
import doctest
doctest.run_docstring_examples(run_parser, globals())