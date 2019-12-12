import operator
from functools import reduce

MATH_OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}

namespace = {}  # global namespace


class Profiler:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1


profiler = Profiler()


class InterpreterError(Exception):
    """Runtime error."""


class Function:
    """Mock up function object"""

    def __init__(self, params, body, closure=None):
        """Function declared with parameters and code (body)"""
        self.params = params
        self.body = body
        self.closure = closure or {}
        self.cache = {}

    def __call__(self, args):
        """Calling function adds arguments to local namespace
        and then interprets body."""
        args = tuple(args)
        if args in self.cache:
            return self.cache[args]
        self.namespace = dict(zip(self.params, args))
        result = run_block(
            self.body, locals=self.namespace, globals=namespace, closure=self.closure
        )
        self.cache[args] = result
        return result


def interpret(expr, locals, globals, closure):
    """Evaluates the expression tree."""
    closure = closure or {}
    profiler()
    if not isinstance(expr, list):  # expr is leaf
        if isinstance(expr, str):  # expr is a name: look up in locals then globals

            if expr in locals:
                return locals[expr]

            if expr in closure:
                return closure[expr]

            return globals[expr]

        return expr  # expr is a number

    op = expr[-1]  # postfix!

    if isinstance(op, str) and op in MATH_OPS:  # op is +, -, *, or /
        operands = [interpret(term, locals, globals, closure) for term in expr[:-1]]
        return reduce(MATH_OPS[op], operands)

    if op == "define":  # assign name and value to local namespace
        name = expr[0]
        value = interpret(expr[1], locals, globals, closure)
        locals[name] = value
        return

    if op == "lambda":  # create function object
        params = expr[0]
        body = expr[1:-1]
        func = Function(params, body, closure=locals)
        return func

    if op == "eq?":
        lhs = interpret(expr[0], locals, globals, closure)
        rhs = interpret(expr[1], locals, globals, closure)
        return lhs == rhs

    if op == "atom?":
        operand = interpret(expr[0], locals, globals, closure)
        return not isinstance(operand, list)

    if op == "quote":
        return expr[0]  # do not evaluate

    if op == "cons":
        head = interpret(expr[0], locals, globals, closure)
        tail = interpret(expr[1], locals, globals, closure)

        # we are not using linked list, so handle atom and list separately
        if isinstance(tail, list):
            return [head] + tail
        else:
            return head, tail

    if op == "car":
        pair = interpret(expr[0], locals, globals, closure)
        return pair[0]

    if op == "cdr":
        pair = interpret(expr[0], locals, globals, closure)

        # we are not using linked list, so handle atom and list separately
        if isinstance(pair, list):
            return pair[1:]
        else:
            return pair[1]

    if op == "cond":
        clauses = expr[:-1]
        for condition, value in clauses:
            if (
                condition == "else"
                or interpret(condition, locals, globals, closure) is True
            ):
                return interpret(value, locals, globals, closure)

    if isinstance(op, str):

        obj = locals[op] if op in locals else globals[op]

        args = [interpret(term, locals, globals, closure) for term in expr[:-1]]

        result = obj(args)
        return result

    # allow calling of lambda expression inline
    op = interpret(op, locals, globals, closure)
    if isinstance(op, Function):
        args = [interpret(term, locals, globals, closure) for term in expr[:-1]]
        return op(args)

    raise InterpreterError("unknown operation")


def run_block(block, locals=namespace, globals=namespace, closure=None):
    """Evaluate block of expressions and return last value."""
    for expr in block:
        result = interpret(expr, locals=locals, globals=globals, closure=closure)

    return result
