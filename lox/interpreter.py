from expr import Expr, Literal, Grouping, Unary, Binary
from token_type import TokenType

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
                        return -right
                return None
            case Binary(left, operator, right):
                left = self.evaluate(left)
                right = self.evaluate(right)
                match operator.type:
                    case TokenType.GREATER:
                        return left > right
                    case TokenType.GREATER_EQUAL:
                        return left >= right
                    case TokenType.LESS:
                        return left < right
                    case TokenType.LESS_EQUAL:
                        return left <= right
                    case TokenType.MINUS:
                        return left - right
                    case TokenType.PLUS:
                        if isinstance(left, float) and isinstance(right, float):
                            return left + right
                        if isinstance(left, str) and isinstance(right, str):
                            return left + right
                    case TokenType.SLASH:
                        return left / right
                    case TokenType.STAR:
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