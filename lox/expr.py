from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from token_ import Token

class ExprVisitor(ABC):
    @abstractmethod
    def visit_binary(self, expr: "Binary") -> Any:
        pass

    @abstractmethod
    def visit_grouping(self, expr: "Grouping") -> Any:
        pass

    @abstractmethod
    def visit_literal(self, expr: "Literal") -> Any:
        pass

    @abstractmethod
    def visit_unary(self, expr: "Unary") -> Any:
        pass

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor):
        pass

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit_binary(self)

@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor):
        return visitor.visit_grouping(self)

@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor):
        return visitor.visit_literal(self)

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit_unary(self)