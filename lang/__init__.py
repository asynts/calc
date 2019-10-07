"""
Rules are matched from left to right.
The first alternative takes precedence if there is a conflict.
The star '*' operator is greedy.

<args> ::= <expr> (',' <expr>)* ;

<expr> ::= <expr> INFIX <expr>
        / PREFIX <expr>
        / <expr> POSTFIX
        /  '(' <expr> ')'
        / INTEGER
        / IDENTIFIER '(' <args>? ')'
        / IDENTIFIER
        ;
"""
from . import parser

"""
Rules are matched from left to right.
The first alternative takes precedence if there is a conflict.
The star '*' operator is greedy.

<expr> ::= <term> (INFIX <term>)* ;

<term> :: = PREFIX* <operand> POSTFIX* ;

<operand> ::= '(' <expr> ')'
           / INTEGER
           / IDENTIFIER '(' <args>? ')'
           / IDENTIFIER
           ;

<args> ::= <expr> (',' <expr>)* ;
"""
from . import lexer
