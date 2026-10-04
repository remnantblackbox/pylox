from stmt import Stmt, Block, Var, Function, Expression, If, Print, Return, While
from expr import Expr, Variable, Assign, Binary, Call, Grouping, Lambda, Logical, Unary
from token_ import Token
from error import parse_error
from enum import Enum, auto

class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()

class Resolver:
    """Static pass that works out which declaration each variable use refers to.

    Runs once between parsing and execution. It walks the syntax tree
    without running it, keeping a stack of scopes that mirrors the
    environments the interpreter will create. For each use of a local
    variable it tells the interpreter how many scopes away the
    declaration is. A closure therefore always reads the variable it
    captured, even if the same name is declared again later.

    Unlike the interpreter, it visits every part of the tree exactly
    once: both branches of an if, and a loop body a single time.

    It also reports errors that can be found without running the code:
    a variable read in its own initializer, a variable declared twice in
    the same local scope, and a return outside a function.

    Globals are not tracked. A name found in no local scope is assumed
    to be global and is looked up by name at runtime.
    """

    def __init__(self, interpreter):
        self.interpreter = interpreter
        # Stack of local scopes, innermost last. Each maps a variable name to
        # whether its initializer has been resolved: False = declared only,
        # True = defined. An empty stack means we are at global scope.
        self.scopes: list[dict[str, bool]] = []
        self.current_function = FunctionType.NONE

    def resolve(self, statements: list[Stmt]) -> None:
        """Resolve a list of statements in the current scope."""

        for statement in statements:
            self.resolve_stmt(statement)

    def resolve_function(self, function: Function | Lambda, function_type) -> None:
        """Resolve a function's parameters and body in a new scope.

        Records that we are inside a function, so a return is allowed, and
        restores the previous state afterwards because functions can nest.
        """

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
        """Add a name to the innermost scope, marked as not yet usable.

        Reports an error if the scope already has that name. Does nothing at
        global scope, where redeclaring a variable is allowed.
        """

        if not self.scopes:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            parse_error(name, "Already a variable with this name in this scope.")
        scope[name.lexeme] = False

    def define(self, name: Token) -> None:
        """Mark a declared name as initialized and usable.

        Declaring and defining are separate steps so that "var a = a;" can
        be detected: the initializer is resolved between the two.
        """

        if not self.scopes:
            return
        self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expr, name: Token) -> None:
        """Tell the interpreter how many scopes separate this use from its
        declaration. If the name is in no local scope, record nothing: it is
        treated as a global and looked up by name at runtime."""
        for distance, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, distance)
                return

    def resolve_stmt(self, stmt) -> None:
        """Resolve one statement.

        Block     opens a new scope for its statements
        Var       declares the name, resolves the initializer, then
                  defines the name
        Function  defines the name before resolving the body, so the
                  function can call itself
        Return    is an error outside a function

        Every other statement only resolves the expressions and statements
        it contains.
        """
        
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
        """Resolve one expression.

        Variable  is an error if read inside its own initializer;
                  otherwise its scope distance is recorded
        Assign    resolves the value, then records the distance of the
                  variable being assigned
        Lambda    is resolved like a function declaration, without a name

        Every other expression only resolves its sub-expressions.
        """

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