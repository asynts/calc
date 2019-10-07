p_identifier = p.regex('[_a-z0-9]+')
p_function_arguments = p.maybe(p.chain(
    p_expr, # ???
    p.maybe(p.repeat(p.chain(
        p.match(','),
        p_expr
    )))
))

p_expr_integer = p.regex('[0-9]+')
p_expr_variable = p.identifier()
p_expr_invoke = p.chain(
    p.identifier(),
    p.match('('),
    p.any(
        p.chain(
            p_function_arguments,
            p.match(')')
        ),
        p.error('expected function arguments')
    )
)
p_expr_prefix = p.chain(
    p.any(
        p.match('++'),
        p.match('--'),
        p.match('-')
    ),
    p.any(
        p_expr,  # ???
        p.error('expected expression')
    )
)

p_expr_simple = p.any(
    p_expr_invoke,
    p_expr_prefix,

    p_expr_integer,
    p_expr_variable
)

p_expr_postfix = p.chain(
    p_expr, # ???
    p.any(
        p.match('++'),
        p.match('--')
    )
)

p_expr_infix = p.chain(
    p_expr, # ???
    p.any(
        p.match('+'),
        p.match('-'),
        p.match('*'),
        p.match('/'),
    ),
    p_expr # ???
)

p_expr = p.any(
    p_expr_postfix,
    p_expr_infix,
    p_expr_simple
)
