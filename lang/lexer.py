"""
<expr> ::= <term> (INFIX <term>)* ;

<term> :: = PREFIX* <value> POSTFIX* ;

<value> ::= '(' <expr> ')'
         / INTEGER
         / IDENTIFIER '(' <args>? ')'
         / IDENTIFIER
         ;

<args> ::= <expr> (',' <expr>)* ;
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

    def _match(self, string: str):
        if self._input[self._cursor:].startswith(string):
            self._cursor += len(string)
            return string
        return None

    def _regex(self, regex: re.Pattern):
        match = regex.match(self._input[self._cursor:])
        if match:
            self._cursor += len(match.group(0))
            return match.group(0)
        return None

    _re_integer = re.compile('^[0-9]+')
    _re_identifier = re.compile('^[_a-z0-9]+')
    def _lex_value(self):
        # rule: '(' <expression> ')'
        token = Token(
            offset=self._cursor,
            category=Category.OPEN,
            value=self._match('(')
        )
        if token.value:
            self._output.append(token)

            if not self._lex_expression():
                raise LexerError

            token = Token(
                offset=self._cursor,
                category=Category.CLOSE,
                value=self._match(')')
            )
            if token.value:
                self._output.append(token)
                return True
            else:
                raise LexerError

        # rule: INTEGER
        token = Token(
            offset=self._cursor,
            category=Category.INTEGER,
            value=self._regex(self._re_integer)
        )
        if token.value:
            self._output.append(token)
            return True

        # rule: IDENTIFIER '(' <arguments> ')' / IDENTIFIER
        token = Token(
            offset=self._cursor,
            value=self._regex(self._re_identifier),
            category=None
        )
        if token.value:
            if self._match('('):
                token.category = Category.INVOKE
                self._output.append(token)

                self._lex_arguments()

                token = Token(
                    offset=self._cursor,
                    category=Category.CLOSE,
                    value=self._match(')'),
                )
                if token.value:
                    self._output.append(token)
                else:
                    raise LexerError

                return True
            else:                
                token.category = Category.VARIABLE
                self._output.append(token)
                return True

        
        return False

    def _lex_arguments(self):
        pass

    def _lex_expression(self):
        pass
