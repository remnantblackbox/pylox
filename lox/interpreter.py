from expr import Expr, Literal, Grouping, Unary, Binary, Variable, Assign, Logical
from stmt import Stmt, Expression, Print, Var, Block, If
from environment import Environment
from token_type import TokenType
from runtime_error import LoxRuntimeError
import error

class Interpreter:
    def __init__(self):
        # global environment
        self.environment = Environment()

    def interpret(self, statements: list[Stmt]):
        try:
            for stmt in statements:
                self.execute(stmt, self.environment)
        except LoxRuntimeError as e:
            error.runtime_error(e)    

    def evaluate(self, expr, environment):
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
                return environment.get(name)
            case Assign(name, value):
                value = self.evaluate(value, environment)
                environment.assign(name, value)
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
                        return left / right
                    case TokenType.STAR:
                        self.check_number_operands(operator, left, right)
                        return left * right
                    case TokenType.BANG_EQUAL:
                        return left != right
                    case TokenType.EQUAL_EQUAL:
                        return left == right
                return None

    def execute(self, stmt, environment):
        match stmt:
            case Expression(expression):
                self.evaluate(expression, environment)
            case If(condition, then_branch, else_branch):
                if self.is_truthy(self.evaluate(condition, environment)):
                    self.execute(then_branch, environment)
                elif else_branch is not None:
                    self.execute(else_branch, environment)
            case Print(expression):
                value = self.evaluate(expression, environment)
                print(self.stringify(value))
            case Var(name, initializer):
                value = None
                if initializer is not None:
                    value = self.evaluate(initializer, environment)
                environment.define(name.lexeme, value)
            case Block(statements):
                block_env = Environment(environment)
                for statement in statements:
                    self.execute(statement, block_env)

    def is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def stringify(self, value):
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

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")