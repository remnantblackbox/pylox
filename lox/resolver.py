from stmt import Block, Var

class Resolver:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes: list[dict[str, bool]] = []

    def resolve(self, statements):
        for statement in statements:
            self.resolve_stmt(statement)

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name):
        if not self.scopes:
            return
        scope = self.scopes[-1]
        scope[name.lexeme] = False

    def define(self, name):
        if not self.scopes:
            return
        self.scopes[-1][name.lexeme] = True

    def resolve_stmt(self, stmt):
        match stmt:
            case Block(statements):
                self.begin_scope()
                self.resolve(statements)
                self.end_scope()
            case Var(name, initializer):
                self.declare(name)
                if initializer is not None:
                    self.resolve_expr(initializer)
                self.define(name)

    def resolve_expr(self, expr):
        pass