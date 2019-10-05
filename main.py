#!/usr/bin/env python

from lexer import Lexer

lx = Lexer('(20+1)*2')

while lx.has_more_input:
    node = lx.next_integer()
    if node is not None:
        print(node)
        continue

    node = lx.next_special()
    if node is not None:
        print(node)
        continue

    raise SyntaxError
