from dataclasses import dataclass
from expr import Expr

class Stmt:
    pass

@dataclass
class Expression(Stmt):
    expression: Expr

@dataclass
class Print(Stmt):
    expression: Expr