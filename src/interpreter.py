import operator
from functools import reduce

MATH_OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}

namespace = {}  # global namespace


class InterpreterError(Exception):
    """Runtime error."""

    pass


class Function:
    """Mock up function object"""

    def __init__(self, params, body):
        """Function declared with parameters and code (body)"""
        self.params = params
        self.body = body

    def __call__(self, args):
        """Calling function adds arguments to local namespace
        and then interprets body."""
        self.namespace = dict(zip(self.params, args))
        return interpret(self.body, locals=self.namespace, globals=namespace)


def interpret(expr, locals, globals):
    """Evaluates the expression tree."""
    if not isinstance(expr, list):  # expr is leaf
        if isinstance(expr, str):  # expr is a name: look up in locals then globals
            return locals[expr] if expr in locals else globals[expr]

        return expr  # expr is a number

    op = expr[-1]  # postfix!

    if isinstance(op, str) and op in MATH_OPS:  # op is +, -, *, or /
        operands = [interpret(term, locals, globals) for term in expr[:-1]]
        return reduce(MATH_OPS[op], operands)

    if op == "define":  # assign name and value to local namespace
        name = expr[0]
        value = interpret(expr[1], locals, globals)
        locals[name] = value
        return

    if op == "lambda":  # create function object
        params = expr[0]
        body = expr[1]
        return Function(params, body)

    if op == "eq?":
        lhs = interpret(expr[0], locals, globals)
        rhs = interpret(expr[1], locals, globals)
        return lhs == rhs

    if op == "atom?":
        operand = interpret(expr[0], locals, globals)
        return not isinstance(operand, list)

    if op == "quote":
        return expr[0]  # do not evaluate

    if op == "cons":
        head = interpret(expr[0], locals, globals)
        tail = interpret(expr[1], locals, globals)

        # we are not using linked list, so handle atom and list separately
        if isinstance(tail, list):
            return [head] + tail
        else:
            return head, tail

    if op == "car":
        pair = interpret(expr[0], locals, globals)
        return pair[0]

    if op == "cdr":
        pair = interpret(expr[0], locals, globals)

        # we are not using linked list, so handle atom and list separately
        if isinstance(pair, list):
            return pair[1:]
        else:
            return pair[1]

    if op == "cond":
        clauses = expr[:-1]
        for condition, value in clauses:
            if condition == "else" or interpret(condition, locals, globals) is True:
                return interpret(value, locals, globals)

    if isinstance(op, str):
        obj = locals[op] if op in locals else globals[op]

        args = [interpret(term, locals, globals) for term in expr[:-1]]
        return obj(args)

    # allow calling of lambda expression inline
    op = interpret(op, locals, globals)
    if isinstance(op, Function):
        args = [interpret(term, locals, globals) for term in expr[:-1]]
        return op(args)

    raise InterpreterError("unknown operation")


def run_block(block):
    """Evaluate block of expressions and return last value."""
    for expr in block:
        result = interpret(expr, locals=namespace, globals=namespace)
    return result
