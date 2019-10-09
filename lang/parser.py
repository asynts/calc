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

class ExprInvoke(Expr):
    name: str
    args: typing.List[Expr]

PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '(': 0,
}

class Parser_:
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
                return True

            if token.category == Category.VARIABLE:
                self._operands.append(ExprVariable(
                    offset=token.offset,
                    name=token.value
                ))
                return True

            if token.category == Category.INVOKE:
                # When the parser encounters a `Category.CLOSE` token it backtracks and searches for a
                # `Category.INVOKE` operator. When this operator is found, a `ExprInvoke` node will be constructed.
                self._operators.append(token)

                while self._parse_expression():
                    self._operators.append(self._tokens.pop(0))
                    assert self._operators[-1].category == Category.COMMA
                return True
            
            # TODO
