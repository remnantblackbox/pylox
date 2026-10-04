from abc import ABC, abstractmethod
from typing import Any
from stmt import Function
from expr import Lambda
from environment import Environment
from return_exc import ReturnException
import time

class LoxCallable(ABC):
    @abstractmethod
    def call(self, interpreter, arguments) -> Any:
        pass

    @abstractmethod
    def arity(self) -> int:
        pass

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function | Lambda, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments: list[Any]) -> Any:
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as e:
            return e.value

    def arity(self) -> int:
        return len(self.declaration.params)

    def __repr__(self):
        if isinstance(self.declaration, Lambda):
            return "<fn>"
        return f"<fn {self.declaration.name.lexeme}>"

# native functions
class Clock(LoxCallable):
    def call(self, interpreter, arguments) -> Any:
        return time.time()

    def arity(self) -> int:
        return 0

    def __repr__(self):
        return "<native fn>"