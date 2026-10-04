from __future__ import annotations
from typing import Any
from token_ import Token
from runtime_error import LoxRuntimeError

class Environment:
    def __init__(self, enclosing=None):
        self.values: dict[str, Any] = {}
        self.enclosing: Environment | None = enclosing

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def ancestor(self, distance: int) -> Environment:
        environment = self
        for i in range(distance):
            environment = environment.enclosing
        return environment

    def get_at(self, distance: int, name: str) -> Any:
        return self.ancestor(distance).values.get(name)

    def assign_at(self, distance: int, name: Token, value: Any) -> None:
        self.ancestor(distance).values[name.lexeme] = value

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")