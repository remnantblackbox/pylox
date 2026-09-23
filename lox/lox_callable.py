from abc import ABC, abstractmethod
from stmt import Function
from environment import Environment
from return_exc import ReturnException
import time

class LoxCallable(ABC):
    @abstractmethod
    def call(self, interpreter, arguments):
        pass

    @abstractmethod
    def arity(self):
        pass

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as e:
            return e.value

    def arity(self):
        return len(self.declaration.params)

    def __repr__(self):
        return f"<fn {self.declaration.name.lexeme}>"

# native functions
class Clock(LoxCallable):
    def call(self, interpreter, arguments):
        return time.time()

    def arity(self):
        return 0

    def __repr__(self):
        return "<native fn>"