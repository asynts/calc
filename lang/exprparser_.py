import ast
import lexer

class ParserError:
    def __init__(self, token, message):
        self.token = token
        self.message = message

    def __str__(self):
        return f"{self.message} while parsing {self.token}"

class Parser:
    def __init__(self, input_):
        self.input = input_
        self._lexer = lexer.Lexer(input_)
        self._ahead = None

    def _has_more(self) -> bool:
        try:
            self._peek()
            return True
        except StopIteration:
            return False

    def _peek(self) -> lexer.Token:
        if self._ahead is None:
            self._ahead = next(self._lexer)

        return self._ahead

    def _consume(self) -> lexer.Token:
        if self._ahead is None:
            return next(self._lexer)

        token = self._ahead
        self._ahead = None
        return token

    def parse_expr(self) -> ast.Expr:
        exprparser = ExprParser()

        while self._has_more:
            if exprparser.process(self._peek()):
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
    def __init__(self):
        self._operands = []
        self._operators = []
        self._last_processed_token = None

    def _apply(self):
        operator = self._operators.pop()

        if len(self._operands) < 2:
            raise ParserError(operator, 'not enough operands')

        rhs = self._operands.pop()
        lhs = self._operands.pop()

        self._operands.append(ast.ExprBinary(operator.offset, operator.value, lhs, rhs))

    @property
    def _top(self):
        return self._operators[-1].value

    def _process_arithmetic(self, token):
        while len(self._operators) > 0 and PRECEDENCE[self._top] >= PRECEDENCE[token.value]:
            self._apply()

        self._operators.append(token)

    def process(self, token) -> bool:
        if token.type == lexer.Tokens.INTEGER:
            self._operands.append(ast.ExprInteger(token.offset, int(token.value)))
            return True
        elif token.type == lexer.Tokens.SPECIAL and token.value in list('+-*/()'):
            if token.value == '(':
                self._operators.append(token)
            elif token.value == ')':
                while len(self._operators) > 0 and self._top != '(':
                    self._apply()

                if len(self._operators) > 0 and self._top == '(':
                    self._operators.pop()
                else:
                    raise ParserError(token, 'mismatched parentheses')
            else:
                self._process_arithmetic(token)
            return True

        return False

    def finalize(self) -> ast.Expr:
        while len(self._operators) > 0:
            self._apply()

        if len(self._operands) == 0:
            return None

        if len(self._operands) == 1:
            return self._operands[0]

        raise ParserError(self._last_processed_token, 'invalid expression')

parser = Parser('(20 + 1) * 2')
print(parser.parse_expr())
