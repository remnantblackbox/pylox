from stmt import Stmt, Block, Var, Function, Expression, If, Print, Return, While
from expr import Expr, Variable, Assign, Binary, Call, Grouping, Lambda, Logical, Unary
from token_ import Token
from error import parse_error
from enum import Enum, auto

class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()

class Resolver:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes: list[dict[str, bool]] = []
        self.current_function = FunctionType.NONE

    def resolve(self, statements: list[Stmt]) -> None:
        for statement in statements:
            self.resolve_stmt(statement)

    def resolve_function(self, function: Function | Lambda, function_type) -> None:
        enclosing_function = self.current_function
        self.current_function = function_type
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()
        self.current_function = enclosing_function

    def begin_scope(self) -> None:
        self.scopes.append({})

    def end_scope(self) -> None:
        self.scopes.pop()

    def declare(self, name: Token) -> None:
        if not self.scopes:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            parse_error(name, "Already a variable with this name in this scope.")
        scope[name.lexeme] = False

    def define(self, name: Token) -> None:
        if not self.scopes:
            return
        self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expr, name: Token) -> None:
        for distance, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, distance)
                return

    def resolve_stmt(self, stmt) -> None:
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
                self.resolve_function(stmt, FunctionType.FUNCTION)
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
                if self.current_function is FunctionType.NONE:
                    parse_error(keyword, "Can't return from top-level code.")
                if value is not None:
                    self.resolve_expr(value)
            case While(condition, body):
                self.resolve_expr(condition)
                self.resolve_stmt(body)

    def resolve_expr(self, expr) -> None:
        match expr:
            case Variable(name):
                if self.scopes and self.scopes[-1].get(name.lexeme) is False:
                    parse_error(name, "Can't read local variable in its own initializer.")
                self.resolve_local(expr, name)
            case Assign(name, value):
                self.resolve_expr(value)
                self.resolve_local(expr, name)
            case Binary(left, operator, right):
                self.resolve_expr(left)
                self.resolve_expr(right)
            case Call(callee, paren, arguments):
                self.resolve_expr(callee)
                for argument in arguments:
                    self.resolve_expr(argument)
            case Grouping(expression):
                self.resolve_expr(expression)
            case Lambda():
                self.resolve_function(expr, FunctionType.FUNCTION)
            case Logical(left, operator, right):
                self.resolve_expr(left)
                self.resolve_expr(right)
            case Unary(operator, right):
                self.resolve_expr(right)