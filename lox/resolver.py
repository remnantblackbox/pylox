class Resolver:
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def resolve(self, statements):
        for statement in statements:
            self.resolve_stmt(statement)

    def resolve_stmt(self, statement):
        pass

    def resolve_expr(self, statement):
        pass