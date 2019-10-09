#!/usr/bin/env python

import lang

lexer = lang.lexer.Lexer('(20+1)*2')
assert lexer._lex_expression()
print(lexer._output)

parser = lang.parser.Parser(lexer._output)
print(parser.parse_expression())
