from dataclasses import dataclass
from typing import Any
from token_ import Token
from stmt import Stmt

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
class Call(Expr):
    callee: Expr
    paren: Token
    arguments: list[Expr]

@dataclass
class Grouping(Expr):
    expression: Expr

@dataclass
class Lambda(Expr):
    keyword: Token
    params: list[Token]
    body: list[Stmt]

@dataclass
class Literal(Expr):
    value: Any

@dataclass
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

@dataclass
class Variable(Expr):
    name: Token