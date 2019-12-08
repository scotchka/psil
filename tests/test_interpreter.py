from src.interpreter import interpret, run_block
from src.parser import tokenize, parse


def test_arithmetic():
    assert interpret([1, 2, "/"], {}, {}) == 0.5


def test_define():
    namespace = {}
    interpret(["x", 42, "define"], namespace, namespace)
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
    assert interpret([2, 2, "eq?"], {}, {}) is True
    assert interpret([2, 1, "eq?"], {}, {}) is False


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
    assert interpret([["a", "b", "c"], "quote"], {}, {}) == ["a", "b", "c"]
