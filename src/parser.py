class ParseError(Exception):
    pass


def convert_if_number(token):
    """Return number if token represents number, otherwise token itself."""
    try:
        token = int(token)
    except ValueError:
        try:
            token = float(token)
        except ValueError:
            pass

    return token


def tokenize(string):
    """Produces list of tokens from source."""
    tokens = []
    token = ""

    i = 0
    while i < len(string):

        char = string[i]
        if char in ("(", ")", "'") or char.isspace():
            if token:
                tokens.append(convert_if_number(token))
                token = ""

        if char in ("(", ")", "'"):
            tokens.append(char)
        elif char.strip() != "":
            token += char

        i += 1

    if token:
        tokens.append(convert_if_number(token))

    return tokens


def expand_quote(ast):
    """Syntactic sugar for single quotation mark."""
    i = 0
    while i < len(ast):
        if isinstance(ast[i], list):
            expand_quote(ast[i])
            i += 1
        elif ast[i] == "'":
            if i == 0:
                raise IndexError
            ast[i - 1 : i + 1] = [[ast[i - 1], "quote"]]

        else:
            i += 1


def parse(tokens):
    """Produces syntax tree (nested list) from tokens."""
    ast = []
    stack = [ast]
    for token in tokens:
        try:
            if token == "(":
                stack[-1].append([])
                stack.append(stack[-1][-1])
            elif token == ")":
                stack.pop()
            else:
                stack[-1].append(token)
        except IndexError:
            raise ParseError("unbalanced expression")

    if len(stack) != 1:
        raise ParseError("unbalanced expression")

    try:
        expand_quote(ast)
    except IndexError:
        raise ParseError("misplaced quote")

    return ast
