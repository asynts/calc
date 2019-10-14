import sys

from dataclasses import dataclass

from . import parser, Error

class RuntimeError(Error):
    pass

class Runtime:
    def __init__(self):
        self._bindings = {}
        self._functions = {}

        self._functions['exit'] = lambda: sys.exit()
        self._functions['help'] = lambda: print("""\
OPERATIONS
  a     lookup a binding
a = b   assign a binding

bar()   call a function

 (a)    group operations

a + b   add
a - b   subtract
a * b   multiply
a / b   divide

FUNCTIONS
help()  print this help
exit()  terminate
""", end='')

    def evaluate(self, ast: parser.Expr) -> int:
        if isinstance(ast, parser.ExprInteger):
            return ast.value

        if isinstance(ast, parser.ExprBinding):
            if not ast.name in self._bindings:
                raise RuntimeError(ast.offset, 'unknown binding')

            return self._bindings[ast.name]
        
        if isinstance(ast, parser.ExprInvoke):
            if not ast.name in self._functions:
                raise RuntimeError(ast.offset, 'unknown function')

            func = self._functions[ast.name]
            args = [self.evaluate(argument) for argument in ast.arguments]

            return func(*args)

        if isinstance(ast, parser.ExprBinary):
            if ast.operator == '+':
                return self.evaluate(ast.lhs) + self.evaluate(ast.rhs)
            if ast.operator == '-':
                return self.evaluate(ast.lhs) - self.evaluate(ast.rhs)
            if ast.operator == '*':
                return self.evaluate(ast.lhs) * self.evaluate(ast.rhs)
            if ast.operator == '/':
                return self.evaluate(ast.lhs) / self.evaluate(ast.rhs)
            if ast.operator == '=':
                if not isinstance(ast.lhs, parser.ExprBinding):
                    raise RuntimeError(ast.offset, "can't assign to rvalue")

                self._bindings[ast.lhs.name] = self.evaluate(ast.rhs)
                return self._bindings[ast.lhs.name]

            raise NotImplementedError

        raise NotImplementedError
