from dataclasses import dataclass
from typing import Any
from token_ import Token

class Expr():
    pass

@dataclass
class Assign(Expr):
    name: Token
    value: Expr
@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass
class Grouping(Expr):
    expression: Expr

@dataclass
class Literal(Expr):
    value: Any

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

@dataclass
class Variable(Expr):
    name: Token