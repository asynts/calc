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
class ExprBinding(Expr):
    value: str

@dataclass
class ExprBinary(Expr):
    operator: str
    lhs: Expr
    rhs: Expr

PRECEDENCE = {
    '(': -1,
    '=': 0,
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
}

class Parser:
    def __init__(self, tokens: typing.List[Token]):
        self._tokens = tokens
        self._cursor = 0
        self._operands: typing.List[Expr] = []
        self._operators: typing.List[Token] = []

    @property
    def _has_more(self):
        return self._cursor < len(self._tokens)

    @property
    def _ahead(self) -> Token:
        return self._tokens[self._cursor]

    def _apply(self, operator: Token):
        if operator.category == Category.INFIX:
            self._operands.append(ExprBinary(
                offset=operator.offset,
                operator=operator.value,
                rhs=self._operands.pop(),
                lhs=self._operands.pop()
            ))
            return

        if operator.category in [Category.PREFIX, Category.POSTFIX]:
            raise NotImplementedError

        raise AssertionError

    def _parse_value(self):
        if self._ahead.category == Category.INTEGER:
            self._operands.append(ExprInteger(
                offset=self._ahead.offset,
                value=int(self._ahead.value)
            ))
            self._cursor += 1
            return True

        if self._ahead.category == Category.VARIABLE:
            self._operands.append(ExprBinding(
                offset=self._ahead.offset,
                value=self._ahead.value
            ))
            self._cursor += 1
            return True

        return False

    def _parse_operator(self):
        if self._ahead.category == Category.INFIX:
            while len(self._operators) > 0 and PRECEDENCE[self._operators[-1].value] >= PRECEDENCE[self._ahead.value]:
                self._apply(self._operators.pop())
            self._operators.append(self._ahead)
            self._cursor += 1
            return True
        
        return False

    def _parse_parentheses(self):
        if self._ahead.category == Category.OPEN:
            self._operators.append(self._ahead)
            self._cursor += 1
            return True
        
        if self._ahead.category == Category.CLOSE:
            self._cursor += 1

            while len(self._operators) > 0 and self._operators[-1].category != Category.OPEN:
                self._apply(self._operators.pop())

            assert self._operators[-1].category == Category.OPEN
            self._operators.pop()
            
            return True
           
        return False
