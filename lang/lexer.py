from enum import Enum
from dataclasses import dataclass

class LexerError(Exception):
    def __init__(self, offset, message):
        self.offset = offset
        self.message = message

    def __str__(self):
        return f"{self.message} at offset {self.offset}"

class Tokens(Enum):
    INTEGER = 0
    SPECIAL = 1

@dataclass
class Token:
    offset: int
    type: Tokens
    value: str

class Lexer:
    def __init__(self, input_):
        self._input = input_
        self._cursor = 0

    def __iter__(self):
        return self

    def __next__(self) -> Token:
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
            raise LexerError(self._cursor, 'syntax error')

        raise StopIteration

    @property
    def _has_more(self) -> bool:
        return self._cursor < len(self._input)

    @property
    def _ahead(self) -> str:
        return self._input[self._cursor]

    def _consume(self) -> str:
        char = self._ahead
        self._cursor += 1

        return char

    def _next_integer(self) -> Token:
        token = Token(self._cursor, Tokens.INTEGER, None)

        if self._has_more and self._ahead in '123456789':
            token.value = self._consume()

            while self._has_more and self._ahead in '0123456789':
                token.value += self._consume()

            return token
        return None

    def _next_special(self) -> Token:
        token = Token(self._cursor, Tokens.SPECIAL, None)

        if self._has_more and self._ahead in '+-*/()':
            token.value = self._consume()
            return token
        return None

    def _skip_whitespace(self) -> bool:
        begin = self._cursor
        while self._has_more and self._ahead in ' \t\n':
            self._cursor += 1

        return begin != self._cursor
