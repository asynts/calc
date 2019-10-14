import typing

from dataclasses import dataclass

from . import Error
from .lexer import Category, Token

class ParserError(Error):
    pass

@dataclass
class Expr:
    offset: int

@dataclass
class ExprInteger(Expr):
    value: int

@dataclass
class ExprBinding(Expr):
    name: str

@dataclass
class ExprInvoke(Expr):
    name: str
    arguments: typing.List[Expr]

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

ASSOCIATIVITY = {
    '=': 'right',
    '+': 'left',
    '-': 'left',
    '*': 'left',
    '/': 'left',
}

class Parser:
    def __init__(self, tokens: typing.List[Token]):
        self._tokens = tokens
        self._cursor = 0
        self._operands: typing.List[Expr] = []
        self._operators: typing.List[Token] = []
        self._scope = 0

    @property
    def _has_more(self):
        return self._cursor < len(self._tokens)

    @property
    def _ahead(self) -> Token:
        return self._tokens[self._cursor]
    
    def _backup(self):
        return { 'cursor': self._cursor, 'operands': self._operands[:], 'operators': self._operators[:] }
    
    def _restore(self, backup):
        self._cursor = backup['cursor']
        self._operands = backup['operands']
        self._operators = backup['operators']

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
        if not self._has_more:
            return False

        backup = self._backup()

        if self._ahead.category == Category.INTEGER:
            self._operands.append(ExprInteger(
                offset=self._ahead.offset,
                value=int(self._ahead.value)
            ))
            self._cursor += 1
            return True
        
        if self._ahead.category == Category.INVOKE:
            node = ExprInvoke(
                offset=self._ahead.offset,
                name=self._ahead.value,
                arguments=[]
            )
            self._cursor += 1

            if self._has_more and self._ahead.category == Category.OPEN:
                self._cursor += 1

                if self._ahead.category == Category.CLOSE:
                    self._cursor += 1
                    self._operands.append(node)
                    return True
                
                while True:
                    subparser = Parser(self._tokens[self._cursor:])
                    subparser._parse_expression()
                    self._cursor += subparser._cursor

                    node.arguments.append(subparser._operands.pop())

                    if self._ahead.category == Category.CLOSE:
                        self._cursor += 1
                        self._operands.append(node)
                        return True
                    
                    assert self._ahead.category == Category.COMMA
                    self._cursor += 1

            else:
                self._restore(backup)

        if self._ahead.category == Category.VARIABLE:
            self._operands.append(ExprBinding(
                offset=self._ahead.offset,
                name=self._ahead.value
            ))
            self._cursor += 1
            return True

        return False

    def _parse_operator(self):
        if not self._has_more:
            return False

        if self._ahead.category == Category.INFIX:
            if ASSOCIATIVITY[self._ahead.value] == 'left':
                while len(self._operators) > 0 and PRECEDENCE[self._operators[-1].value] >= PRECEDENCE[self._ahead.value]:
                    self._apply(self._operators.pop())
            else:
                assert ASSOCIATIVITY[self._ahead.value] == 'right'

                while len(self._operators) > 0 and PRECEDENCE[self._operators[-1].value] > PRECEDENCE[self._ahead.value]:
                    self._apply(self._operators.pop())

            self._operators.append(self._ahead)
            self._cursor += 1
            return True
       
        return False

    def _parse_parentheses(self):
        if not self._has_more:
            return False

        if self._ahead.category == Category.OPEN:
            self._scope += 1

            self._operators.append(self._ahead)
            self._cursor += 1
            return True
        
        if self._ahead.category == Category.CLOSE and self._scope > 0:
            self._cursor += 1

            while len(self._operators) > 0 and self._operators[-1].category != Category.OPEN:
                self._apply(self._operators.pop())

            assert self._operators[-1].category == Category.OPEN
            self._operators.pop()
            
            self._scope -= 1

            return True
           
        return False

    def _parse_expression(self):
        has_matched = False
        while self._parse_value() or self._parse_parentheses() or self._parse_operator():
            has_matched = True

        if not has_matched:
            return False

        while len(self._operators) > 0:
            self._apply(self._operators.pop())
    
        assert len(self._operands) == 1
        return True

def parse(tokens: typing.List[Token]):
    parser = Parser(tokens)

    if not parser._parse_expression():
        return None
    
    return parser._operands.pop()
