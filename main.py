#!/usr/bin/env python

import lang

for token in lang.lexer.lex('x = 42'):
    print(f"{token.category.name}: '{token.value}'")
