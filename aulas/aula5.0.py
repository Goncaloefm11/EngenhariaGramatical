import lark_ag

grammar = r'''
SA(lista) { max: float, sum: float }
SA(elems) { max: float, sum: float }
SA(elem)  { val: float }

lista: "(" elems ")"
ER {
    lista.max = elems.max;
    lista.sum = elems.sum;
}

CC {
    lista.sum > 0 : "Non-positive sum";
}

elems: elems "," elem
ER {
    elems[1].max = max(elems[2].max, elem.val);
    elems[1].sum = elems[2].sum + elem.val;
}
  | elem
ER {
    elems[1].max = elem.val;
    elems[1].sum = elem.val;
}

elem: NUM
ER {
    elem.val = float(NUM);
}
  | TXT
ER {
    elem.val = 0;
}

NUM: /-?\d+/
TXT: /[a-zA-Z_][a-zA-Z0-9_]*/

WS: /[ \t\f\n]+/
%ignore WS
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