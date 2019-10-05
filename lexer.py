class Lexer:
    def __init__(self, input_):
        self._input = input_

    @property
    def has_more_input(self):
        return len(self._input) > 0

    def peek(self):
        if self.has_more_input:
            return self._input[0]
        raise IndexError

    def next(self):
        if self.has_more_input:
            self._input, value = self._input[1:], self._input[0]
            return value
        raise IndexError

    def next_integer(self):
        if self.has_more_input and self.peek() in '123456789':
            matched = self.next()

            while self.has_more_input and self.peek() in '0123456789':
                matched += self.next()

            return int(matched)
        return None

    def next_special(self):
        if self.has_more_input and self.peek() in '+-*/()':
            return self.next()
        return None
