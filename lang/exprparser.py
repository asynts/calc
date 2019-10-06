#!/usr/bin/env python

from enum import Enum
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

class Associativity(Enum):
    LEFT = 0
    RIGHT = 1

_ASSOCIATIVITY = {
    '+': Associativity.LEFT,
    '-': Associativity.LEFT,
    '*': Associativity.LEFT,
    '/': Associativity.LEFT,
}

_PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    # The shunting yard algorithm checks whether the top token has a greater
    # precedence. A left parentheses isn't an operator but can appear on the
    # operator stack and must therefor be compareable with operators.
    '(': 0,
}

class Parser:
    def __init__(self, lexer):
        self._lexer = lexer
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

    def parse_operator(self):
        node = self._lexer.next_special()
        if node is None: return False

        if node.value == '(':
            self.operators.append(node)
        elif node.value == ')':
            while len(self.operators) > 0 and self.operators[-1].value != '(':
                self.apply()
            self.operators.pop()
        elif _ASSOCIATIVITY[node.value] == Associativity.LEFT:
            if len(self.operators) > 0 and _PRECEDENCE[self.operators[-1].value] >= _PRECEDENCE[node.value]:
                self.apply()
            self.operators.append(node)
        else:
            if len(self.operators) > 0 and _PRECEDENCE[self.operators[-1].value] > _PRECEDENCE[node.value]:
                self.apply()
            self.operators.append(node)

        return True

def parse(input_):
    lexer = Lexer(input_)
    parser = Parser(lexer)

    while lexer.has_more_input:
        if not (lexer.skip_whitespace() or parser.parse_integer() or parser.parse_operator()):
            raise SyntaxError

    while len(parser.operators) > 0:
        parser.apply()

    assert len(parser.operands) == 1
    return parser.operands[0]
