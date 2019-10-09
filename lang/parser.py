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
    lhs: typing.Any # TODO
    rhs: typing.Any # TODO

@dataclass
class ExprInvoke(Expr):
    name: str
    arguments: typing.List[typing.Any] # TODO

PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '(': 0, # TODO
}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens[:]
        self.operands = []
        self.operators = []
    
    @property
    def top(self) -> Token:
        return self.operators[-1]
    
    def apply(self, token: Token):
        assert token.category == Category.INFIX # TODO

        self.operands.append(ExprBinary(
            offset=token.offset,
            operator=token.value,
            rhs=self.operands.pop(),
            lhs=self.operands.pop()
        ))
    
    def parse_arguments(self):
        pass # TODO

    def parse_expression(self):
        while len(self.tokens):
            token = self.tokens.pop(0)

            if token.category == Category.INTEGER:
                self.operands.append(ExprInteger(offset=token.offset, value=int(token.value)))
                continue

            if token.category == Category.VARIABLE:
                self.operands.append(ExprVariable(offset=token.offset, name=token.value))
                continue
        
            if token.category == Category.INVOKE:
                self.operands.append(ExprInvoke(
                    offset=token.offset,
                    name=token.value,
                    arguments=self.parse_arguments()
                ))
                continue

            if token.category == Category.OPEN:
                self.operators.append(token)
                continue

            if token.category == Category.CLOSE:
                while self.top.category != Category.OPEN:
                    self.apply(self.operators.pop())

                self.operators.pop()
                continue

            if token.category == Category.INFIX:
                while len(self.operators) > 0 and PRECEDENCE[self.top.value] >= PRECEDENCE[token.value]:
                    self.apply(self.operators.pop())
                
                self.operators.append(token)
                continue
        
            raise NotImplementedError
        
        while len(self.operators) > 0:
            self.apply(self.operators.pop())

        assert len(self.operands) == 1
        return self.operands[0]
