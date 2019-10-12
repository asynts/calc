#!/usr/bin/env python

import lang

tokens = lang.lexer.lex('foo( 2 * (1 + twenty) )')

for token in tokens:
    print(f"{token.category.name}: '{token.value}'")
