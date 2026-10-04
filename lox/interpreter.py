from expr import Expr, Literal, Grouping, Unary, Binary, Variable, Assign, Logical, Call, Lambda
from stmt import Stmt, Expression, Print, Var, Block, If, While, Function, Return
from environment import Environment
from lox_callable import LoxCallable, Clock, LoxFunction
from token_ import Token
from token_type import TokenType
from runtime_error import LoxRuntimeError
from return_exc import ReturnException
from typing import Any
import error

class Interpreter:
    """Tree-walking interpreter: executes a resolved syntax tree.
    
    Lox values are represented directly by Python values:
    
        nil       None
        Boolean   bool
        number    float (every Lox number, including integers)
        string    str
        function  LoxCallable (LoxFunction or a native such as Clock)
    
    Variables live in a chain of Environment objects, one per scope.
    Before execution, the Resolver stores in self.locals how many
    scopes away each local variable use is. A variable use that is not
    in self.locals is looked up by name in self.globals.
    
    The current environment is passed to evaluate() and execute() 
    as a parameter instead of being stored in a field, 
    so a block never has to restore the previous environment.
    """
    
    def __init__(self):
        self.globals = Environment()
        self.globals.define("clock", Clock())
        # Scope distance for each local variable use, filled in by the Resolver
        # before execution. An expression missing from this dict is a global one.
        self.locals: dict[Expr, int] = {}

    def interpret(self, statements: list[Stmt]) -> None:
        try:
            for stmt in statements:
                self.execute(stmt, self.globals)
        except LoxRuntimeError as e:
            error.runtime_error(e)

    def evaluate(self, expr, environment) -> Any:
        """Evaluate an expression in the given environment and return its Lox value.

        Literal   the value itself
        Logical   left operand first; the right one only if needed.
                  Returns the operand's own value, not true/false.
        Lambda    a new function closing over the environment
        Grouping  the value of the inner expression
        Unary     "-" requires a number; "!" negates truthiness
        Variable  the variable's value, at its resolved distance or global
        Assign    stores the value and returns it, so "a = b = 1" works
        Binary    both operands, left to right, then the operator.
                  Arithmetic and comparison require numbers; "+" also
                  joins two strings; "==" never converts between types.
        Call      callee, then arguments left to right. The callee must
                  be callable and the argument count must match its arity.

        Raises LoxRuntimeError when an operand or callee has the wrong type.
        """

        match expr:
            case Literal(value):
                return value
            case Logical(left, operator, right):
                left = self.evaluate(left, environment)
                if operator.type == TokenType.OR:
                    if self.is_truthy(left):
                        return left
                else:
                    if not self.is_truthy(left):
                        return left
                return self.evaluate(right, environment)
            case Lambda():
                return LoxFunction(expr, environment)
            case Grouping(expression):
                return self.evaluate(expression, environment)
            case Unary(operator, right):
                right = self.evaluate(right, environment)
                match operator.type:
                    case TokenType.BANG:
                        return not self.is_truthy(right)
                    case TokenType.MINUS:
                        self.check_number_operand(operator, right)
                        return -right
                return None
            case Variable(name):
                return self.look_up_variable(name, expr, environment)
            case Assign(name, value):
                value = self.evaluate(value, environment)
                distance = self.locals.get(expr)
                if distance is not None:
                    environment.assign_at(distance, name, value)
                else:
                    self.globals.assign(name, value)
                return value
            case Binary(left, operator, right):
                left = self.evaluate(left, environment)
                right = self.evaluate(right, environment)
                match operator.type:
                    case TokenType.GREATER:
                        self.check_number_operands(operator, left, right)
                        return left > right
                    case TokenType.GREATER_EQUAL:
                        self.check_number_operands(operator, left, right)
                        return left >= right
                    case TokenType.LESS:
                        self.check_number_operands(operator, left, right)
                        return left < right
                    case TokenType.LESS_EQUAL:
                        self.check_number_operands(operator, left, right)
                        return left <= right
                    case TokenType.MINUS:
                        self.check_number_operands(operator, left, right)
                        return left - right
                    case TokenType.PLUS:
                        if isinstance(left, float) and isinstance(right, float):
                            return left + right
                        if isinstance(left, str) and isinstance(right, str):
                            return left + right
                        raise LoxRuntimeError(operator, "Operands must be two numbers or two strings.")
                    case TokenType.SLASH:
                        self.check_number_operands(operator, left, right)
                        if right == 0:
                            raise LoxRuntimeError(operator, "Division by zero.")
                        return left / right
                    case TokenType.STAR:
                        self.check_number_operands(operator, left, right)
                        return left * right
                    case TokenType.BANG_EQUAL:
                        # Compare types first because in Python True == 1.0, but in Lox 1 == true is false.
                        return type(left) is not type(right) or left != right
                    case TokenType.EQUAL_EQUAL:
                        return type(left) is type(right) and left == right
                return None
            case Call(callee, paren, arguments):
                callee = self.evaluate(callee, environment)
                arguments = [self.evaluate(arg, environment) for arg in arguments]
                if not isinstance(callee, LoxCallable):
                    raise LoxRuntimeError(paren, "Can only call functions and classes.")
                if len(arguments) != callee.arity():
                    raise LoxRuntimeError(paren, f"Expected {callee.arity()} arguments but got {len(arguments)}.")
                return callee.call(self, arguments)

    def execute(self, stmt, environment) -> None:
        """Execute a statement in the given environment.

        Expression  evaluates and discards the value
        Function    defines the name, capturing environment as closure
        If          runs one branch, by the truthiness of the condition
        Print       writes the value's printed form and a newline
        Return      raises ReturnException to unwind to the function call
        Var         defines the name; nil when there is no initializer
        While       repeats the body while the condition is truthy
        Block       runs the statements in a new nested environment
        """

        match stmt:
            case Expression(expression):
                self.evaluate(expression, environment)
            case Function(name):
                function = LoxFunction(stmt, environment)
                environment.define(name.lexeme, function)
            case If(condition, then_branch, else_branch):
                if self.is_truthy(self.evaluate(condition, environment)):
                    self.execute(then_branch, environment)
                elif else_branch is not None:
                    self.execute(else_branch, environment)
            case Print(expression):
                value = self.evaluate(expression, environment)
                print(self.stringify(value))
            case Return(keyword, value):
                ret_val = None
                if value is not None:
                    ret_val = self.evaluate(value, environment)
                raise ReturnException(ret_val)
            case Var(name, initializer):
                value = None
                if initializer is not None:
                    value = self.evaluate(initializer, environment)
                environment.define(name.lexeme, value)
            case While(condition, body):
                while self.is_truthy(self.evaluate(condition, environment)):
                    self.execute(body, environment)
            case Block(statements):
                block_env = Environment(environment)
                self.execute_block(statements, block_env)

    def resolve(self, expr, depth) -> None:
        self.locals[expr] = depth

    def look_up_variable(self, name: Token, expr: Expr, environment) -> Any:
        """Read a variable at its resolved distance, or from self.globals if unresolved."""

        distance = self.locals.get(expr)
        if distance is not None:
            return environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)

    def execute_block(self, statements: list[Stmt], environment) -> None:
        """Run statements in an environment the caller has already created.

        Used by blocks and by function calls, which need different parents.
        """
        for statement in statements:
            self.execute(statement, environment)

    def is_truthy(self, obj) -> bool:
        """Lox truthiness: nil and false are falsey, everything else is truthy."""
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def stringify(self, value) -> str:
        """Format a Lox value for printing: nil, true/false, 3 instead of 3.0."""
        if value is None:
            return "nil"
        
        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text

        if isinstance(value, bool):
            return "true" if value else "false"
        
        return str(value)

    def check_number_operand(self, operator, operand) -> None:
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")