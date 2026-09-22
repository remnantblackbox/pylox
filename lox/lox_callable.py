from abc import ABC, abstractmethod
from time import time
from stmt import Function
from environment import Environment

class LoxCallable(ABC):
    @abstractmethod
    def call(self, interpreter, arguments):
        pass

    @abstractmethod
    def arity(self):
        pass

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function):
        self.declaration = declaration

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        interpreter.execute(self.declaration.body, environment)

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