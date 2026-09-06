from expr import ExprVisitor, Expr, Binary, Grouping, Literal, Unary

class AstPrinter(ExprVisitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def visit_binary(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visit_literal(self, expr: Literal):
        if expr.value == None:
            return "nil"
        return str(expr.value)

    def visit_unary(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr):
        output = [expr.accept(self) for expr in exprs]
        return f"({name} {' '.join(output)})"