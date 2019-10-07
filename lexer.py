def unary_expr():
    for op in ['-']:
        if match(op):
            emit(UNARY, op)
            return expr()
    return False

def call_expr():
    pass

def integer_expr():
    pass

def variable_expr():
    pass

def atomic_expr():
    unary_expr() or call_expr() or integer_expr() or variable_expr()

def infix_expr():
    pass

def postfix_expr():
    pass

def expr():
    pass

