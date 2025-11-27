from lark import Visitor, Token

class SymbolTable:
    def __init__(self):
        self.scopes = [{}] 
    def enter_scope(self): self.scopes.append({})
    def exit_scope(self): self.scopes.pop()
    def declare(self, name): self.scopes[-1][name] = "var"
    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope: return True
        return False

class ScopeAnalyser(Visitor):
    def __init__(self):
        self.table = SymbolTable()
        self.errors = [] # Agora guarda dicionários: {'line': 1, 'message': '...'}

    def block(self, tree): self.table.enter_scope()
    
    def assign_expr(self, tree):
        var_token = tree.children[0]
        if isinstance(var_token, Token): self.table.declare(var_token.value)

    def var_access(self, tree):
        var_token = tree.children[0]
        name = var_token.value

        if not self.table.lookup(name):
            line = getattr(tree.meta, 'line', '?')
            self.errors.append({
                'line': line,
                'message': f"Variável '{name}' não declarada.",
                'severity': 'SCOPE'
            })

        # IMPORTANTE: não retornar nada, não mexer no tree.
        return tree   # ← ADICIONA ISTO


    def try_catch_stmt(self, tree):
        if len(tree.children) == 4:
            var_token = tree.children[2]
            if isinstance(var_token, Token): self.table.declare(var_token.value)