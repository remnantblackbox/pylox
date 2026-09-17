from abc import ABC, abstractmethod
from time import time

class LoxCallable(ABC):
    @abstractmethod
    def call(self, interpreter, arguments):
        pass

    @abstractmethod
    def arity(self):
        pass

class Clock(LoxCallable):
    def call(self, interpreter, arguments):
        return time.time()

    def arity(self):
        return 0

    def __repr__(self):
        return "<native fn>"