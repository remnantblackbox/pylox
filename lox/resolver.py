from stmt import Block, Var, Function
from expr import Variable, Assign
from error import error

class Resolver:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes: list[dict[str, bool]] = []

    def resolve(self, statements):
        for statement in statements:
            self.resolve_stmt(statement)

    def resolve_function(self, function):
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve_stmt(function.body)
        self.end_scope()

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

    def resolve_local(self, expr, name):
        for distance, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, distance)
                return

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
            case Function(name):
                self.declare(name)
                self.define(name)
                self.resolve_function(stmt)

    def resolve_expr(self, expr):
        match expr:
            case Variable(name):
                if self.scopes and self.scopes[-1][name.lexeme] == False:
                    error(name, "Can't read local variable in its own initializer.")
                self.resolve_local(expr, name)
            case Assign(name, value):
                self.resolve(value)
                self.resolve_local(expr, name)