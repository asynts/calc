#!/usr/bin/env python

import lang

input_ = '1 1 + (2 + 3)'

parser = lang.parser.Parser(input_)

try:
    print(parser.parse_expr())
except (lang.lexer.LexerError, lang.parser.ParserError) as err:
    print(input_)
    print(' ' * err.offset + '^')
    print('error: ' + err.message)
