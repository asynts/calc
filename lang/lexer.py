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
    VARIABLE = 3

    OPEN = 7
    CLOSE = 2
    COMMA = 8

    PREFIX = 4
    INFIX = 5
    POSTFIX = 6

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
            return token
        return None

    def _regex(self, regex: re.Pattern, category: Category):
        match = regex.match(self._input[self._cursor:])
        if match:
            token = Token(
                offset=self._cursor,
                category=category,
                value=match.group(0)
            )

            self._cursor += len(match.group(0))
            return token
        return None

    _re_integer = re.compile('^[0-9]+')
    _re_identifier = re.compile('^[_a-z0-9]+')
    def _lex_value(self):
        # rule: '(' <expression> ')'
        token = self._match('(', Category.OPEN)
        if token:
            self._output.append(token)

            if not self._lex_expression():
                raise LexerError

            token = self._match(')', Category.CLOSE)
            if token:
                self._output.append(token)
                return True
            else:
                raise LexerError

        # rule: INTEGER
        token = self._regex(self._re_integer, Category.INTEGER)
        if token:
            self._output.append(token)
            return True

        # rule: IDENTIFIER '(' <arguments>? ')' / IDENTIFIER
        token = self._regex(self._re_identifier, None)
        if token:
            if self._match('(', None):
                token.category = Category.INVOKE
                self._output.append(token)

                self._lex_arguments()

                token = self._match(')', Category.CLOSE)
                if token:
                    self._output.append(token)
                else:
                    raise LexerError

                return True
            else:                
                token.category = Category.VARIABLE
                self._output.append(token)
                return True
            raise LexerError

        
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
            token = self._match(op, Category.PREFIX)
            if token:
                self._output.append(token)
                return True
        return False

    def _lex_infix(self):
        for op in '+-*/':
            token = self._match(op, Category.INFIX)
            if token:
                self._output.append(token)
                return True
        return False

    def _lex_postfix(self):
        for op in ['++', '--']:
            token = self._match(op, Category.POSTFIX)
            if token:
                self._output.append(token)
                return True
        return False

    def _lex_arguments(self):
        if not self._lex_expression():
            return False

        token = self._match(',', Category.COMMA)
        while token:
            self._output.append(token)

            if not self._lex_expression():
                raise LexerError

            token = self._match(',', Category.COMMA)
        
        return True

    def _lex_expression(self):
        if not self._lex_term():
            return False

        while self._lex_infix():
            if not self._lex_term():
                raise LexerError
        
        return True
