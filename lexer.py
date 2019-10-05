import typing

from dataclasses import dataclass

@dataclass
class Token:
    value: typing.Any
    offset: int

class Lexer:
    def __init__(self, input_):
        self.input = input_
        self._cursor = 0

    @property
    def has_more_input(self):
        return self._cursor < len(self.input)

    def peek(self):
        return self.input[self._cursor]

    def next(self):
        value = self.peek()
        self._cursor += 1

        return value

    def next_integer(self):
        token = Token(None, self._cursor)

        if self.has_more_input and self.peek() in '123456789':
            matched = self.next()

            while self.has_more_input and self.peek() in '0123456789':
                matched += self.next()

            token.value = int(matched)
            return token
        return None

    def next_special(self):
        if self.has_more_input and self.peek() in '+-*/()':
            # Notice: Python evaluates function arguments from left to right.
            return Token(offset=self._cursor, value=self.next())
        return None
