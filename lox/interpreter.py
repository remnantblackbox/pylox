from expr import Expr, Literal, Grouping, Unary, Binary
from token_type import TokenType
from runtime_error import LoxRuntimeError

class Interpreter:
    def evaluate(self, expr: Expr):
        match expr:
            case Literal(value):
                return value
            case Grouping(expression):
                return self.evaluate(expression)
            case Unary(operator, right):
                right = self.evaluate(right)
                match operator.type:
                    case TokenType.BANG:
                        return not self.is_truthy(right)
                    case TokenType.MINUS:
                        self.check_number_operand(operator, right)
                        return -right
                return None
            case Binary(left, operator, right):
                left = self.evaluate(left)
                right = self.evaluate(right)
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

    def is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")