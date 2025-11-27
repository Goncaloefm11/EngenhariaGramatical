import networkx as nx
import matplotlib.pyplot as plt
from lark import Visitor, Token, Tree

class CFGBuilder(Visitor):
    def __init__(self, var_values=None):
        self.graph = nx.DiGraph()
        self.counter = 0
        self.last_node_id = "START"
        self.graph.add_node("START", label="Start", shape="oval")

        # Valores literais recebidos do StaticAnalyser
        self.var_values = var_values or {}

    # -----------------------------------
    # Criar Nó
    # -----------------------------------
    def _add_node(self, label, shape="box"):
        node_id = f"node_{self.counter}"
        self.counter += 1

        self.graph.add_node(node_id, label=label, shape=shape)
        self.graph.add_edge(self.last_node_id, node_id)

        self.last_node_id = node_id
        return node_id

    # -----------------------------------
    # Extrair o atom real
    # -----------------------------------
    def _unwrap_expr(self, node):
        if isinstance(node, Token):
            return node

        if not isinstance(node, Tree):
            return node

        if node.data in (
            "string", "var_access", "comparison",
            "logical_or", "logical_and",
            "sum", "product", "atom"
        ):
            return node

        if len(node.children) == 1:
            return self._unwrap_expr(node.children[0])

        return node

    # -----------------------------------
    # Converter AST -> Texto
    # -----------------------------------
    def _expr_to_text(self, node):
        node = self._unwrap_expr(node)

        if isinstance(node, Token):
            return node.value

        if isinstance(node, Tree):

            # String literal
            if node.data == "string":
                return node.children[0].value

            # Acesso a variável
            if node.data == "var_access":
                return node.children[0].value

            # Qualquer outro tipo (comparison, sum, etc)
            parts = [self._expr_to_text(ch) for ch in node.children]
            return " ".join(parts)

        return "?"

    # -----------------------------------
    # Atribuições
    # -----------------------------------
    def assign_expr(self, tree):
        var = tree.children[0].value
        expr_raw = tree.children[1]
        expr = self._unwrap_expr(expr_raw)

        # Caso literal
        if isinstance(expr, Tree) and expr.data == "string":
            literal = expr.children[0].value
            label = f"{var} = {literal}"

        # Caso var = outra_var
        elif isinstance(expr, Tree) and expr.data == "var_access":
            src = expr.children[0].valu
