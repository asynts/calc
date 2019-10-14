#!/usr/bin/env python

import lang
import graphviz

tokens = lang.lexer.lex('42 + foo(2 * (20 + 1))')

parser = lang.parser.Parser(tokens)
parser._parse_expression()

assert len(parser._operands) == 1
ast = parser._operands.pop()

print(graphviz.create_graph(ast))
