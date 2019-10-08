import re, typing

from dataclasses import dataclass
from enum import Enum

class Tokens(Enum):
    INTEGER = 0
    IDENTIFIER = 1
    INVOKE = 2
    COMMA = 3

    UNARY = 4
    BINARY = 5

@dataclass
class Token:
    offset: int
    type_: Tokens
    value: typing.Any

class Lexer:
    def __init__(self, input_):
        self._input = input_
        self._cursor = 0
        self._tokens = []
    
    def _emit(self, offset, type_, value):
        self._tokens.append(Token(offset, type_, value))

    def _backup(self):
        return {'cursor': self._cursor, 'tokens': self._tokens}

    def _restore(self, backup):
        self._cursor = backup['cursor']
        self._tokens = backup['tokens']

    @property
    def _ahead(self):
        return self._input[self._cursor:]

    def _must(self, condition):
        if not condition:
            raise AssertionError('assertion failed')

    def _match(self, string):
        if self._ahead.startswith(string):
            self._cursor += len(string)
            return True
        return False

    _re_integer = re.compile('^[0-9]+')
    def _lex_integer(self) -> bool:
        match = self._re_integer.match(self._ahead)
        if match:
            self._emit(
                offset=self._cursor,
                type_=Tokens.INTEGER,
                value=match.group(0)
            )
            self._cursor += len(match.group(0))
        return bool(match)

    _re_identifier = re.compile('^[_a-z0-9]+')
    def _lex_identifier(self) -> bool:
        match = self._re_identifier.match(self._ahead)
        if match:
            self._emit(
                offset=self._cursor,
                type_=Tokens.IDENTIFIER,
                value=match.group(0)
            )
            self._cursor += len(match.group(0))
        return bool(match)

    def _lex_arguments(self) -> bool:
        if self._lex_expression():
            while self._match(','):
                self._emit(
                    offset=self._cursor-1,
                    type_=Tokens.COMMA,
                    value=','
                )
                self._must(self._lex_expression)
            return True
        return False

    def _lex_operand(self) -> bool:
        if self._match('('):
            self._must(self._lex_expression())
            self._must(self._match(')'))
            return True

        if self._lex_integer():
            return True

        if self._lex_identifier():
            if self._match('('):
                begin = self._cursor
                self._lex_arguments()
                self._must(self._match(')'))

                token = Token(
                    offset=begin,
                    type_=Tokens.INVOKE,
                    value=[self._tokens[begin:]]
                )
                self._tokens = self._tokens[:begin]
                self._tokens.append(token)                

            return True

        return False

    def _lex_prefix(self):
        for op in ['++', '--', '-']:
            if self._match(op):
                self._emit(
                    offset=self._cursor,
                    type_=Tokens.UNARY,
                    value=op
                )
                return True
        return False

    def _lex_infix(self):
        for op in ['+', '-', '*', '/']:
            if self._match(op):
                self._emit(
                    offset=self._cursor,
                    type_=Tokens.BINARY,
                    value=op
                )
                return True
        return False

    def _lex_postfix(self):
        for op in ['++', '--']:
            if self._match(op):
                self._emit(
                    offset=self._cursor,
                    type_=Tokens.UNARY,
                    value=op
                )
                return True
        return False

    def _lex_term(self) -> bool:
        backup = self._backup()

        while self._lex_prefix():
            pass

        if not self._lex_operand():
            self._restore(backup)
            return False

        while self._lex_postfix():
            pass

        return True

    def _lex_expression(self) -> bool:
        if self._lex_term():
            while self._lex_infix():
                self._must(self._lex_term())

            return True
        return False

lexer = Lexer('(20+1)*2')
if lexer._lex_expression():
    print(lexer._tokens)
else:
    print('<no match>')
