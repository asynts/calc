import sys

from dataclasses import dataclass

from . import parser, Error

class RuntimeError(Error):
    pass

class Runtime:
    def __init__(self):
        self._variables = {}
        self._functions = {}

        self._functions['exit'] = lambda: sys.exit()
        self._functions['help'] = lambda: print("""\
OPERATIONS
  a     variable lookup
a = b   variable assignment
a + b   add
a - b   subtract
a * b   multiply
a / b   divide
bar()   function call
 (a)    group

FUNCTIONS
help()  print help
exit()  terminate
""", end='')

    def evaluate(self, ast: parser.Expr) -> int:
        if isinstance(ast, parser.ExprInteger):
            return ast.value

        if isinstance(ast, parser.ExprLookup):
            if not ast.name in self._variables:
                raise RuntimeError(ast.offset, 'unknown variable')

            return self._variables[ast.name]
        
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
                if not isinstance(ast.lhs, parser.ExprLookup):
                    raise RuntimeError(ast.offset, "can't assign to rvalue")

                self._variables[ast.lhs.name] = self.evaluate(ast.rhs)
                return self._variables[ast.lhs.name]

            raise NotImplementedError

        raise NotImplementedError
