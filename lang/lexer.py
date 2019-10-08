"""
<expression> ::= <term> (INFIX <term>)* ;

<term> :: = PREFIX* <value> POSTFIX* ;

<value> ::= '(' <expression> ')'
         / INTEGER
         / IDENTIFIER '(' <arguments>? ')'
         / IDENTIFIER
         ;

<arguments> ::= <expression> (',' <expression>)* ;
"""

import re, typing

from dataclasses import dataclass
from enum import Enum

class LexerError(Exception):
    pass

class Category(Enum):
    INTEGER = 0
    INVOKE = 1
    VARIABLE = 2

    OPEN = 3
    CLOSE = 4
    COMMA = 5

    PREFIX = 6
    INFIX = 7
    POSTFIX = 8

@dataclass
class Token:
    offset: int
    category: Category
    value: typing.Any

class Lexer:
    def __init__(self, input_: str):
        self._input = input_
        self._cursor = 0
        self._output = []

    def _backup(self):
        return {'cursor': self._cursor, 'output': self._output}

    def _restore(self, backup):
        self._cursor = backup['cursor']
        self._output = backup['output']

    def _match(self, string: str, category: Category):
        token = Token(
            offset=self._cursor,
            category=category,
            value=string
        )

        if self._input[self._cursor:].startswith(string):
            self._cursor += len(string)
            self._output.append(token)
            return True
        return False

    def _regex(self, regex: re.Pattern, category: Category):
        match = regex.match(self._input[self._cursor:])
        if match:
            token = Token(
                offset=self._cursor,
                category=category,
                value=match.group(0)
            )

            self._cursor += len(match.group(0))
            self._output.append(token)
            return True
        return False

    _re_integer = re.compile('^[0-9]+')
    _re_identifier = re.compile('^[_a-z0-9]+')
    def _lex_value(self):
        # rule: '(' <expression> ')'
        if self._match('(', Category.OPEN):
            if not self._lex_expression():
                raise LexerError

            if self._match(')', Category.CLOSE):
                return True
            else:
                raise LexerError

        # rule: INTEGER
        if self._regex(self._re_integer, Category.INTEGER):
            return True

        # rule: IDENTIFIER '(' <arguments>? ')' / IDENTIFIER
        if self._regex(self._re_identifier, None):
            if self._match('(', Category.OPEN):
                self._output.pop()
                self._output[-1].category = Category.INVOKE

                self._lex_arguments()

                if self._match(')', Category.CLOSE):
                    return True
                else:
                    raise LexerError
            else:
                self._output[-1].category = Category.VARIABLE
                return True
        
        return False
    
    def _lex_term(self):
        backup = self._backup()

        while self._lex_prefix():
            pass

        if not self._lex_value():
            self._restore(backup)
            return False

        while self._lex_postfix():
            pass

        return True

    def _lex_prefix(self):
        for op in ['++', '--', '-']:
            if self._match(op, Category.PREFIX):
                return True
        return False

    def _lex_infix(self):
        for op in '+-*/':
            if self._match(op, Category.INFIX):
                return True
        return False

    def _lex_postfix(self):
        for op in ['++', '--']:
            if self._match(op, Category.POSTFIX):
                return True
        return False

    def _lex_arguments(self):
        if not self._lex_expression():
            return False

        while self._match(',', Category.COMMA):
            if not self._lex_expression():
                raise LexerError
        
        return True

    def _lex_expression(self):
        if not self._lex_term():
            return False

        while self._lex_infix():
            if not self._lex_term():
                raise LexerError
        
        return True

@dataclass
class Expr:
    offset: int

@dataclass
class ExprInteger(Expr):
    offset: int
    value: int

@dataclass
class ExprVariable(Expr):
    offset: int
    name: str

@dataclass
class ExprBinary(Expr):
    offset: int
    operator: str
    lhs: Expr
    rhs: Expr

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

def parse(input_: str):
    lexer = Lexer(input_)
    assert lexer._lex_expression()

    parser = Parser(lexer._output)

    while len(parser.tokens):
        token = parser.tokens.pop(0)

        if token.category == Category.INTEGER:
            parser.operands.append(ExprInteger(offset=token.offset, value=int(token.value)))
            continue

        if token.category == Category.VARIABLE:
            parser.operands.append(ExprVariable(offset=token.offset, name=token.value))
            continue

        if token.category == Category.OPEN:
            parser.operators.append(token)
            continue

        if token.category == Category.CLOSE:
            while parser.top.category != Category.OPEN:
                parser.apply(parser.operators.pop())

            parser.operators.pop()
            continue
    
        raise NotImplementedError
    
    while len(parser.operators) > 0:
        parser.apply(parser.operators.pop())

    assert len(parser.operands) == 1
    return parser.operands[0]
