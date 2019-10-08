"""
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
