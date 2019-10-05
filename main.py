#!/usr/bin/env python

from dataclasses import dataclass

from lexer import Lexer

lx = Lexer('(20+1)*2')

PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '(': 0,
}

@dataclass
class Expr:
    pass

@dataclass
class ExprInteger(Expr):
    value: int
    offset: int

@dataclass
class ExprBinary(Expr):
    lhs: Expr
    rhs: Expr
    op: str
    offset: int

operands = []
operations = []

def apply_():
    rhs = operands.pop()
    lhs = operands.pop()
    op = operations.pop()

    operands.append(ExprBinary(lhs, rhs, op.value, op.offset))

while lx.has_more_input:
    node = lx.next_integer()
    if node is not None:
        operands.append(ExprInteger(node.value, node.offset))
        continue

    node = lx.next_special()
    if node is not None:
        if node.value == '(':
            operations.append(node)
        elif node.value == ')':
            while len(operations) > 0 and operations[-1].value != '(':
                apply_()
            operations.pop()
        else:
            if len(operations) > 0 and PRECEDENCE[operations[-1].value] > PRECEDENCE[node.value]:
                apply_()
            operations.append(node)
        continue

    raise SyntaxError

while len(operations) > 0:
    apply_()

print(operands)
