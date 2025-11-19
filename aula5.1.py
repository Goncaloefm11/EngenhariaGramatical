import lark_ag

grammar = r'''

SA(lista) { max : float }
SA(elems) { max : float, sinal: int }



start :
"(" elems ")"

elems :
    elems "," elem
  | elem

elem :
    NUM
  | P
  | N
  | TXT

NUM : /-?\d+/
P : "p"
N : "n"
TXT : /[a-zA-Z_][a-zA-Z0-9_]*/

'''

def mixed_lists(lst):
    """
    >>> mixed_lists("( 1, 2, 3, 2, 1 )")
    3
    >>> mixed_lists("( um, 1, a, dois, b, c, -1, dd, -4, erro, 12, 4 )")
    12
    >>> mixed_lists("( um , 1, a, dois, b, c, -100, dd, -4, erro, 12, 4 )")
    Traceback (most recent call last):
        ...
    Exception: Non-positive sum
    >>> mixed_lists("( um , 1, a, dois, b, c, -100, dd, -4, erro, 12, 4, 200 )")
    200
    """
    parser = lark_ag.Lark_AG(grammar)
    res = parser.process(lst)
    return res.sum


import doctest
doctest.run_docstring_examples(mixed_lists, globals())