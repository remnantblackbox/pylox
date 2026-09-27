from stmt import Block, Var, Function, Expression, If, Print, Return, While
from expr import Variable, Assign, Binary, Call
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
        self.resolve(function.body)
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
            case Expression(expression):
                self.resolve_expr(expression)
            case If(condition, then_branch, else_branch):
                self.resolve_expr(condition)
                self.resolve_stmt(then_branch)
                if else_branch is not None:
                    self.resolve_stmt(else_branch)
            case Print(expression):
                self.resolve_expr(expression)
            case Return(keyword, value):
                if value is not None:
                    self.resolve_expr(value)
            case While(condition, body):
                self.resolve_expr(condition)
                self.resolve_stmt(body)

    def resolve_expr(self, expr):
        match expr:
            case Variable(name):
                if self.scopes and self.scopes[-1].get(name.lexeme) is False:
                    error(name, "Can't read local variable in its own initializer.")
                self.resolve_local(expr, name)
            case Assign(name, value):
                self.resolve_expr(value)
                self.resolve_local(expr, name)
            case Binary(left, operator, right):
                self.resolve_expr(left)
                self.resolve_expr(right)