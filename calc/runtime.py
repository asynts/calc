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
        self._functions['help'] = lambda: print('''\
name
name = expr

-expr
(expr)

expr + expr
expr - expr
expr * expr
expr / expr

help()
exit()
''', end='')

    def evaluate(self, node: parser.Expr) -> int:
        if node == None:
            return None

        if isinstance(node, parser.ExprInteger):
            return node.value

        if isinstance(node, parser.ExprLookup):
            if not node.name in self._variables:
                raise RuntimeError(node.offset, 'uninitialized variable')

            return self._variables[node.name]
        
        if isinstance(node, parser.ExprInvoke):
            if not node.name in self._functions:
                raise RuntimeError(node.offset, 'undefined function')

            func = self._functions[node.name]
            args = [self.evaluate(argument) for argument in node.arguments]

            return func(*args)

        if isinstance(node, parser.ExprUnary):
            if node.operator == '-':
                return -self.evaluate(node.expression)
            
            raise NotImplementedError

        if isinstance(node, parser.ExprBinary):
            if node.operator == '+':
                return self.evaluate(node.lhs) + self.evaluate(node.rhs)
            if node.operator == '-':
                return self.evaluate(node.lhs) - self.evaluate(node.rhs)
            if node.operator == '*':
                return self.evaluate(node.lhs) * self.evaluate(node.rhs)
            if node.operator == '/':
                return self.evaluate(node.lhs) / self.evaluate(node.rhs)
            if node.operator == '=':
                if not isinstance(node.lhs, parser.ExprLookup):
                    raise RuntimeError(node.offset, 'left side of assignment not assignable')

                self._variables[node.lhs.name] = self.evaluate(node.rhs)
                return self._variables[node.lhs.name]

            raise NotImplementedError

        raise NotImplementedError
