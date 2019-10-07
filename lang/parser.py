from . import nodes, lexer

class ParserError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message

    @property
    def offset(self):
        return self.token.offset

    def __str__(self):
        return f"{self.message} at offset {self.offset}"

class Parser:
    def __init__(self, input_):
        self.input = input_
        self._lexer = lexer.Lexer(input_)
        self._ahead = None

    @property
    def _has_more(self) -> bool:
        try:
            return self.peek().type != lexer.Tokens.EOF
        except StopIteration:
            return False

    def peek(self) -> lexer.Token:
        if self._ahead is None:
            self._ahead = next(self._lexer)

        return self._ahead

    def _consume(self) -> lexer.Token:
        if self._ahead is None:
            return next(self._lexer)

        token = self._ahead
        self._ahead = None
        return token

    def parse_expr(self) -> nodes.Expr:
        if not self._has_more:
            return None

        exprparser = ExprParser(self)

        while self._has_more:
            if exprparser.process(self.peek()):
                self._consume()

        return exprparser.finalize()

PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    # The shunting yard algorithm checks whether the top token has a greater
    # precedence. A left parentheses isn't an operator but can appear on the
    # operator stack and must therefor be compareable with operators.
    '(': 0,
}

class ExprParser:
    def __init__(self, parser):
        self._parser = parser
        self._operands = []
        self._operators = []

    def _apply(self):
        operator = self._operators.pop()

        if len(self._operands) < 2:
            raise ParserError(operator, 'not enough operands')

        rhs = self._operands.pop()
        lhs = self._operands.pop()

        self._operands.append(nodes.ExprBinary(operator.offset, operator.value, lhs, rhs))

    @property
    def _top(self):
        return self._operators[-1]

    def _process_arithmetic(self, token):
        # Notice: `>=` causes all operators to be left associative.
        while len(self._operators) > 0 and PRECEDENCE[self._top.value] >= PRECEDENCE[token.value]:
            self._apply()

        self._operators.append(token)

    def process(self, token) -> bool:
        if token.type == lexer.Tokens.INTEGER:
            self._operands.append(nodes.ExprInteger(token.offset, int(token.value)))
            return True
        elif token.type == lexer.Tokens.SPECIAL and token.value in list('+-*/()'):
            if token.value == '(':
                self._operators.append(token)
            elif token.value == ')':
                while len(self._operators) > 0 and self._top.value != '(':
                    self._apply()

                if len(self._operators) > 0 and self._top.value == '(':
                    self._operators.pop()
                else:
                    raise ParserError(token, 'mismatched parentheses')
            else:
                self._process_arithmetic(token)
            return True

        return False

    def finalize(self) -> nodes.Expr:
        while len(self._operators) > 0:
            if self._top.value == '(':
                raise ParserError(self._top, 'mismatched parentheses')
            self._apply()

        if len(self._operands) == 0:
            return None

        if len(self._operands) == 1:
            return self._operands[0]

        raise ParserError(self._parser.peek(), 'invalid expression')
