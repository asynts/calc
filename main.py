#!/usr/bin/env python

import calc

runtime = calc.runtime.Runtime()

try:
    while True:
        input_ = input('>>> ')

        try:
            tokens = calc.lexer.lex(input_)
            ast = calc.parser.parse(tokens)

            value = runtime.evaluate(ast)

            if value == None:
                pass
            elif isinstance(value, int):
                print(value)
            else:
                raise NotImplementedError
        except calc.Error as err:
            print('    ' + ' ' * err.offset + '^')
            print(f'error, {err.message}')
except (KeyboardInterrupt, EOFError):
    print()
