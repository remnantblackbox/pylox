class ReturnException(Exception):
    """Carries a return value from a Lox 'return' statement up the Python
    call stack to LoxFunction.call. Used for control flow, not as an error."""

    def __init__(self, value):
        super().__init__()
        self.value = value