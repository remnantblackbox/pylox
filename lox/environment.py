from __future__ import annotations
from typing import Any
from token_ import Token
from runtime_error import LoxRuntimeError

class Environment:
    """Maps variable names to their values for one scope.

    Each environment links to the one it was created inside, so a name not
    found here is looked up in the enclosing scopes.

    Variables are reached in two ways. Lookups by name search this scope,
    then the enclosing ones, and raise if the name is undefined. Lookups
    by distance (the *_at methods) go straight to the scope the Resolver
    identified and assume the variable is there.
    """
    
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