#!/usr/bin/env python

import lang

tokens = lang.lexer.lex('foo(2 * (20 + 1), 42)')

parser = lang.parser.Parser(tokens)
print('valid:', parser._parse_expression())
print(parser._operands.pop())
