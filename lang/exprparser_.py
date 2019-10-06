from lexer import Lexer # from .lexer import Lexer

class Parser:
    def __init__(self, input_):
        self.input = input_
        self._lexer = Lexer(input_)
        self._ahead = None

    def _has_more(self):
        try:
            self._peek()
            return True
        except StopIteration:
            return False

    def _peek(self):
        if self._ahead is None:
            self._ahead = next(self._lexer)

        return self._ahead

    def parse_expr(self):
        pass

parser = Parser('(20 + 1) * 2')
