"""
<expression> ::= WS? <term> WS? (INFIX <term> WS?)* ;

<term> :: = PREFIX* WS? <value> WS? POSTFIX* ;

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
    VARIABLE = 2
    INVOKE = 9

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
    value: str

class Lexer:
    def __init__(self, input_: str):
        self._input = input_
        self._cursor = 0
        self._output = []

    @property
    def has_more(self):
        return self._cursor < len(self._input)

    def _backup(self):
        return { 'cursor': self._cursor, 'output': self._output[:] }

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
    
    def _lex_arguments(self):
        if not self._lex_expression():
            return False
        
        while self._match(',', Category.COMMA):
            if not self._lex_expression():
                raise LexerError
        
        return True

    _re_integer = re.compile('^[0-9]+')
    _re_identifier = re.compile('^[_a-z0-9]+')
    def _lex_value(self):
        backup = self._backup()

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

        # rule: IDENTIFIER '(' <arguments>? ')'
        if self._regex(self._re_identifier, Category.INVOKE):
            if self._match('(', Category.OPEN):
                self._lex_arguments()

                if not self._match(')', Category.CLOSE):
                    raise LexerError

                return True
            
            self._restore(backup)

        # rule: IDENTIFIER
        if self._regex(self._re_identifier, Category.VARIABLE):
            return True
        
        return False
    
    def _lex_term(self):
        backup = self._backup()

        while self._lex_prefix():
            pass

        self._lex_whitespace()

        if not self._lex_value():
            self._restore(backup)
            return False

        self._lex_whitespace()

        while self._lex_postfix():
            pass

        return True

    def _lex_prefix(self):
        for op in ['++', '--', '-']:
            if self._match(op, Category.PREFIX):
                return True
        return False

    def _lex_infix(self):
        for op in '+-*/=':
            if self._match(op, Category.INFIX):
                return True
        return False

    def _lex_postfix(self):
        for op in ['++', '--']:
            if self._match(op, Category.POSTFIX):
                return True
        return False
    
    _re_whitespace = re.compile('^[ \t]+')
    def _lex_whitespace(self):
        if self._regex(self._re_whitespace, None):
            self._output.pop()
            return True
        return False

    def _lex_expression(self):
        self._lex_whitespace()

        if not self._lex_term():
            return False

        self._lex_whitespace()

        while self._lex_infix():
            if not self._lex_term():
                raise LexerError
            self._lex_whitespace()
        
        return True

    def lex(self):
        return self._lex_expression()
    
    def finalize(self):
        if self.has_more:
            raise LexerError

        return self._output

def lex(input_: str) -> typing.List[Token]:
    lexer = Lexer(input_)
    if not lexer.lex():
        return None

    return lexer.finalize()
