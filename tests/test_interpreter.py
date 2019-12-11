import pytest
from src.interpreter import interpret, run_block, InterpreterError
from src.parser import tokenize, parse


def test_arithmetic():
    assert interpret([1, 2, "/"], {}, {}, {}) == 0.5


def test_define():
    namespace = {}
    interpret(["x", 42, "define"], namespace, namespace, None)
    assert namespace == {"x": 42}


def test_run_block():
    block = [["x", 42, "define"], "x"]
    assert run_block(block) == 42


def test_lambda():
    source = """
    (square ((x) (x x *) lambda) define)
    (5 square)
    """
    block = parse(tokenize(source))
    assert run_block(block) == 25


def test_equality():
    assert interpret([2, 2, "eq?"], {}, {}, {}) is True
    assert interpret([2, 1, "eq?"], {}, {}, {}) is False


def test_cond():
    source = """
    (a 3 define)
    (
        ((a 1 eq?) (a quote))
        ((a 2 eq?) (b quote))
        ((a 3 eq?) (c quote))
        (else (no-idea quote))
    cond
    )
    """
    block = parse(tokenize(source))
    assert run_block(block) == "c"


def test_quote():
    assert interpret([["a", "b", "c"], "quote"], {}, {}, {}) == ["a", "b", "c"]


def test_single_quote():
    source = """
    (a b c)'
    """
    ast = parse(tokenize(source))
    assert interpret(ast[0], {}, {}, {}) == ["a", "b", "c"]


def test_cons():
    assert interpret([3, 4, "cons"], {}, {}, {}) == (3, 4)


def test_cons_list():
    assert interpret([1, [[2, 3], "quote"], "cons"], {}, {}, {}) == [1, 2, 3]


def test_car():
    pair = interpret([3, 4, "cons"], {}, {}, {})
    assert interpret([pair, "car"], {}, {}, {}) == 3


def test_car_list():
    assert interpret([[[1, 2, 3], "quote"], "car"], {}, {}, {}) == 1


def test_cdr():
    pair = interpret([3, 4, "cons"], {}, {}, {})
    assert interpret([pair, "cdr"], {}, {}, {}) == 4


def test_cdr_list():
    assert interpret([[[1, 2, 3], "quote"], "cdr"], {}, {}, {}) == [2, 3]


def test_interpreter_error():
    with pytest.raises(InterpreterError):
        assert interpret([1, 2, 3], {}, {}, {})


def test_atom():
    assert interpret([1, "atom?"], {}, {}, {}) is True


def test_not_atom():
    assert interpret([[[1, 2, 3], "quote"], "atom?"], {}, {}, {}) is False


def test_inline():
    source = """
    (   -2
        ((x) (1 x +) lambda)
    )
    """
    block = parse(tokenize(source))
    assert run_block(block) == -1


def test_fibonacci():
    with open("fib.psil") as f:
        source = f.read()

    block = parse(tokenize(source))
    assert run_block(block) == 121393
