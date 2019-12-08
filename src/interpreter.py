import operator
from functools import reduce

MATH_OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def interpret(expr):
    op = expr[-1]
    if op in MATH_OPS:
        return reduce(MATH_OPS[op], expr[:-1])
