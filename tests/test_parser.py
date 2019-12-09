import pytest
from src.parser import parse, tokenize, ParseError


def test_tokenize():
    string = "( hello 2 3.14 (world)  ) goodbye"

    assert tokenize(string) == [
        "(",
        "hello",
        2,
        3.14,
        "(",
        "world",
        ")",
        ")",
        "goodbye",
    ]


def test_parser():
    tokens = ["(", "hello", 2, 3.14, "(", "world", ")", ")", "goodbye"]

    assert parse(tokens) == [["hello", 2, 3.14, ["world"]], "goodbye"]


def test_parser_exception_left():
    with pytest.raises(ParseError):
        parse(["("])


def test_parser_exception_stack_empty():
    with pytest.raises(ParseError):
        parse([")", "x"])


def test_replace_quote():
    assert parse([["a", "b"], "'"]) == [[["a", "b"], "quote"]]


def test_replace_quote_error():
    with pytest.raises(ParseError):
        parse(["'", "a"])
