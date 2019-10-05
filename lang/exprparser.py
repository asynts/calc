#!/usr/bin/env python

from dataclasses import dataclass

from .lexer import Lexer

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

_PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '(': 0,
}

class Parser:
    def __init__(self, lexer_):
        self._lexer = lexer_
        self.operands = []
        self.operators = []

    def apply(self):
        rhs = self.operands.pop()
        lhs = self.operands.pop()
        op = self.operators.pop()

        self.operands.append(ExprBinary(lhs, rhs, op.value, op.offset))

    def parse_integer(self):
        node = self._lexer.next_integer()
        if node is None: return False

        self.operands.append(ExprInteger(node.value, node.offset))
        return True

    def parse_special(self):
        node = self._lexer.next_special()
        if node is None: return False

        if node.value == '(':
            self.operators.append(node)
        elif node.value == ')':
            while len(self.operators) > 0 and self.operators[-1].value != '(':
                self.apply()
            self.operators.pop()
        else:
            if len(self.operators) > 0 \
           and _PRECEDENCE[self.operators[-1].value] > _PRECEDENCE[node.value]:
                self.apply()
            self.operators.append(node)

        return True

def parse(input_):
    lexer_ = Lexer(input_)
    parser = Parser(lexer_)

    while lexer_.has_more_input:
        if not (parser.parse_integer() or parser.parse_special()):
            raise SyntaxError

    while len(parser.operators) > 0:
        parser.apply()

    assert len(parser.operands) == 1
    return parser.operands[0]
