from typing import Any
from token_ import Token
from runtime_error import LoxRuntimeError

class Environment:
    def __init__(self):
        self.values: dict[str, Any] = {}

    def define(self, name: str, value: Any):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")