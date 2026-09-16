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
class Print(Stmt):
    expression: Expr

@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr

@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt

@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt