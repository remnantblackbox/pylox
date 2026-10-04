from dataclasses import dataclass
from expr import Expr
from token_ import Token

class Stmt:
    pass

@dataclass
class Block(Stmt):
    statements: list[Stmt]

@dataclass
class Expression(Stmt):
    expression: Expr

@dataclass
class Function(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]

@dataclass
class Print(Stmt):
    expression: Expr

@dataclass
class Return(Stmt):
    keyword: Token
    value: Expr | None

@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr | None

@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt

@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt | None