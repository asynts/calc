#!/usr/bin/env python

import lang

tokens = lang.lexer.lex('(1 + 2) * 3')

parser = lang.parser.Parser(tokens)
