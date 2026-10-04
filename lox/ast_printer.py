from expr import Expr, Binary, Grouping, Literal, Unary

class AstPrinter:
    def print(self, expr: Expr) -> str:
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
        
    def parenthesize(self, name: str, *exprs: Expr) -> str:
        output = [self.print(expr) for expr in exprs]
        return f"({name} {' '.join(output)})"