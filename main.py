#!/usr/bin/env python

import lang

tokens = lang.lexer.lex('(20 + 1) * 2')

parser = lang.parser.Parser(tokens)
print('valid:', parser._parse_expression())
print(parser._operands.pop())
