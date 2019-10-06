from dataclasses import dataclass

@dataclass
class Expr:
    pass

@dataclass
class ExprInteger(Expr):
    offset: int
    value: int

@dataclass
class ExprBinary(Expr):
    offset: int
    op: str
    lhs: Expr
    rhs: Expr
