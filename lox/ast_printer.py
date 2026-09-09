from expr import Expr, Binary, Grouping, Literal, Unary

class AstPrinter:
    def print(self, expr: Expr):
        match expr:
            case Binary(left, operator, right):
                return self.parenthesize(operator.lexeme, left, right)
            case Grouping(expression):
                return self.parenthesize("group", expression)
            case Literal(value):
                if value is None:
                    return "nil"
                return str(value)
            case Unary(operator, right):
                return self.parenthesize(operator.lexeme, right)
            case _:
                raise NotImplementedError(f"Unhandled expression: {type(expr).__name__}")
        
    def parenthesize(self, name: str, *exprs: Expr):
        output = [self.print(expr) for expr in exprs]
        return f"({name} {' '.join(output)})"