class Error(Exception):
    def __init__(self, offset, message):
        self.offset = offset
        self.message = message

from . import lexer, parser, runtime
