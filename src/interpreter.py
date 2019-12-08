import operator
from functools import reduce

MATH_OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}

namespace = {}


class Function:
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def __call__(self, args):
        self.namespace = dict(zip(self.params, args))
        return interpret(self.body, locals=self.namespace, globals=namespace)


def interpret(expr, locals, globals):
    # print(expr)
    if not isinstance(expr, list):
        if isinstance(expr, str):
            return locals[expr] if expr in locals else globals[expr]
        return expr

    op = expr[-1]
    if op in MATH_OPS:
        # operands = [
        #     namespace[term] if isinstance(term, str) else term for term in expr[:-1]
        # ]
        operands = []
        for term in expr[:-1]:
            if isinstance(term, str):
                operands.append(locals[term] if term in locals else globals[term])
            else:
                operands.append(term)
        return reduce(MATH_OPS[op], operands)

    if op == "define":
        symbol = expr[0]
        value = interpret(expr[1], locals, globals)
        locals[symbol] = value
        return

    if op == "lambda":
        params = expr[0]
        body = expr[1]
        return Function(params, body)

    if isinstance(op, str):
        obj = locals[op] if op in locals else globals[op]

        if isinstance(obj, Function):
            args = expr[:-1]
            return obj(args)


def run_block(block):
    for expr in block:
        result = interpret(expr, locals=namespace, globals=namespace)
    # print(namespace)
    return result
