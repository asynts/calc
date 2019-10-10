import typing

from dataclasses import dataclass

from .lexer import Category, Token

@dataclass
class Expr:
    offset: int

@dataclass
class ExprInteger(Expr):
    value: int

@dataclass
class ExprVariable(Expr):
    name: str

@dataclass
class ExprBinary(Expr):
    operator: str
    lhs: Expr
    rhs: Expr

PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '(': 0,
}

class Parser:
    def __init__(self, tokens):
        self._tokens = tokens
        self._operands = []
        self._operators = []

    def _apply(self, operator):
        if operator.category == Category.PREFIX:
            raise NotImplementedError
        elif operator.category == Category.INFIX:
            self._operands.append(ExprBinary(
                offset=operator.offset,
                operator=operator.value,
                rhs=self._operands.pop(),
                lhs=self._operands.pop()
            ))
        else:
            assert operator.category == Category.POSTFIX
            raise NotImplementedError

    def _parse_expression(self) -> Expr:
        while len(self._tokens > 0):
            token = self._tokens.pop(0)

            if token.category == Category.INTEGER:
                self._operands.append(ExprInteger(
                    offset=token.offset,
                    value=int(token.value)
                ))
                continue

            if token.category == Category.VARIABLE:
                self._operands.append(ExprVariable(
                    offset=token.offset,
                    name=token.value
                ))
                continue
            
            if token.category == Category.OPEN:
                self._operators.append(token)
                continue

            if token.category == Category.CLOSE:
                while self._operators[-1].category != Category.OPEN:
                    self._apply(self._operators.pop())

                self._operators.pop()
                continue

            if token.category == Category.INFIX:
                while PRECEDENCE[self._operators[-1].value] >= PRECEDENCE[token.value]:
                    self._apply(self._operators.pop())
                
                self._operators.append(token)
                continue

            if token.category in [Category.PREFIX, Category.POSTFIX]:
                raise NotImplementedError

            raise AssertionError
