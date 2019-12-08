from src.interpreter import interpret


def test_arithmetic():
    assert interpret([1, 2, "/"]) == 0.5
