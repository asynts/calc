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

"""
This grammar accepts an input if and only if it would be accepted by the previous parser.
The star '*' operator is greedy.

<expr> ::= <term> INFIX <term> ;

<term> :: = PREFIX* <expr> POSTFIX* ;

<operand> ::= '(' <expr> ')'
           / INTEGER
           / IDENTIFIER '(' <args>? ')'
           / IDENTIFIER
           ;

<args> ::= <expr> (',' <expr>)* ;
"""
