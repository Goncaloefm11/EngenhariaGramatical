import lark_ag

grammar = r"""
SA(start) { output : str }
SA(lista) { output : str , depth : int , header : str }
SA(elems) { output : str , depth : int , header : str }
SA(elem)  { output : str , depth : int , header : str }

start : lista
    lista.depth = 0
    lista.header = ""
ER {
    start.output = lista.output;
}
TR {
    print(start.output)
}

lista : "(" elems ")"
ER {
    lista.output = elems.output;
}

elems : elems "," elem
ER {
    elems[1].output = elems[2].output + "\n" + elem.output;
}
      | elem
ER {
    elems.output = elem.output;
}

elem : STR
ER {
    elem.output = STR;
}
     | STR lista
ER {
    elem.output = STR + "\n" + lista.output;
}

STR : /"[^"]+"/
%ignore " "
"""

text = '("Introduction", "Background" ("Formalism", "Tools"), "Approach" ("Overview", "Implementation" ("Architecture", "Evaluation"), "Discussion"), "Conclusion")'

parser = lark_ag.Lark_AG(grammar)
result = parser.process(text)
