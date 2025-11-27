from lark import Visitor, Token, Tree

class StaticAnalyser(Visitor):
    def __init__(self):
        self.issues = []
        self.var_values = {}

    def add_issue(self, tree, message, severity):
        line = getattr(tree.meta, 'line', '?')
        self.issues.append({
            'line': line,
            'message': message,
            'severity': severity
        })

    def exec_stmt(self, tree):
        expr = tree.children[0]

        # Caso 1 — exec("literal")
        if isinstance(expr, Tree) and expr.data == "string":
            lit = expr.children[0].value
            self.add_issue(tree, f"Execução de sistema: {lit}", "WARNING")
            return

        # Caso 2 — exec(abc)
        if isinstance(expr, Tree) and expr.data == "var_access":
            var_name = expr.children[0].value
            stored = self.var_values.get(var_name)

            if isinstance(stored, Token) and stored.type == "STRING":
                self.add_issue(tree, f"Execução de sistema: {stored.value}", "WARNING")
                return
            else:
                self.add_issue(tree, "Possível Command Injection (exec dinâmico)", "CRITICAL")
                return

        # Caso geral
        self.add_issue(tree, "Possível Command Injection (exec dinâmico)", "CRITICAL")

    def assign_expr(self, tree):
        var_name = tree.children[0].value
        expr = tree.children[1]

        # Guardar valores estáticos
        if isinstance(expr, Tree) and expr.data == "string":
            self.var_values[var_name] = expr.children[0]
        else:
            self.var_values.pop(var_name, None)

        # Segredos hardcoded
        atom = expr.children[0] if isinstance(expr, Tree) else None
        if isinstance(atom, Token) and atom.type == "STRING":
            suspicious = ['pass', 'key', 'secret']
            if any(s in var_name.lower() for s in suspicious):
                self.add_issue(tree, f"Segredo Hardcoded em '{var_name}'", "CRITICAL")

        # Nome curto
        if len(var_name) < 2 and var_name not in ('i','j','x','y'):
            self.add_issue(tree, f"Nome curto '{var_name}'", "STYLE")

    def throw_stmt(self, tree):
        expr = tree.children[0]
        if isinstance(expr, Tree) and expr.data == "string":
            self.add_issue(tree, "Throw de string crua (Use Objetos)", "WARNING")
