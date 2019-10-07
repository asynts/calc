from dataclasses import dataclass
from enum import Enum

class Tokens(Enum):
    EOF = 0
    INTEGER = 1
    INFIX = 2
    PREFIX = 3
    POSTFIX = 4

@dataclass
class Token:
    offset: int
    type: Tokens
    value: str

class Reader:
    def __init__(self, input_: str):
        self._input = input_
        self._cursor = 0

    @property
    def has_more(self):
        return self._cursor < len(self._input)

    def peek(self):
        return self._input[self._cursor]

    def consume(self):
        if not self.has_more:
            raise ValueError('no more input to consume')

        self._cursor += 1

    @property
    def offset(self):
        return self._cursor

    # TODO this is a really bad function name
    def close(self, marker):
        if marker < _cursor:
            raise ValueError('invalid marker')

        return self._input[marker:_cursor]

class Lexer:
    def __init__(self, reader):
        self._reader = reader

    def integer(self):
        begin = self._reader.offset
        while self._reader.peek() in '0123456789':
            self._reader.consume()

        if begin != self._reader.offset:
            return Token(begin, Tokens.INTEGER, self._reader.close(begin))
        return None

def lex_expression(reader: Reader):
    lexer = Lexer(reader)

    # TODO
