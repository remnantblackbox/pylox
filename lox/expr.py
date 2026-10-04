from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from token_ import Token

class Expr:
    pass

# eq=False keeps identity-based equality and hashing. The interpreter uses
# these nodes as keys in Interpreter.locals, and two uses of the same
# variable name must stay separate entries. A plain @dataclass would make
# the class unhashable.
@dataclass(eq=False)
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

# see Assign comment.
@dataclass(eq=False)
class Variable(Expr):
    name: Token