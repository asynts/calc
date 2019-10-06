import typing

from enum import Enum
from dataclasses import dataclass

class Tokens(Enum):
    INTEGER = 0
    SPECIAL = 1

@dataclass
class Token:
    offset: int
    type: Tokens
    value: typing.Any

class Lexer:
    def __init__(self, input_):
        self._input = input_
        self._cursor = 0

    def __iter__(self):
        return self

    def __next__(self):
        # In Python 3.8 this could be an assignment expression.
        node = self._next_integer()
        if node is not None:
            return node

        # In Python 3.8 this could be an assignment expression.
        node = self._next_special()
        if node is not None:
            return node

        if self._skip_whitespace():
            return self.__next__()

        if self._has_more:
            raise Exception("syntax error")

        raise StopIteration

    @property
    def _has_more(self):
        return self._cursor < len(self._input)

    @property
    def _ahead(self):
        return self._input[self._cursor]

    def _consume(self):
        char = self._ahead
        self._cursor += 1

        return char

    def _next_integer(self):
        token = Token(self._cursor, Tokens.INTEGER, None)

        if self._has_more and self._ahead in '123456789':
            matched = self._consume()

            while self._has_more and self._ahead in '0123456789':
                matched += self._consume()

            token.value = int(matched)
            return token
        return None

    def _next_special(self):
        token = Token(self._cursor, Tokens.SPECIAL, None)

        if self._has_more and self._ahead in '+-*/()':
            token.value = self._consume()
            return token
        return None

    def _skip_whitespace(self):
        begin = self._cursor
        while self._has_more and self._ahead in ' \t\n':
            self._cursor += 1

        return begin != self._cursor
