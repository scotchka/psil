class ParseError(Exception):
    pass


def convert_if_number(token):
    try:
        token = int(token)
    except ValueError:
        try:
            token = float(token)
        except ValueError:
            pass

    return token


def tokenize(string):
    tokens = []
    token = ""

    i = 0
    while i < len(string):

        char = string[i]
        if char in ("(", ")") or char.isspace():
            if token:
                tokens.append(convert_if_number(token))
                token = ""

        if char in ("(", ")"):
            tokens.append(char)
        elif char.strip() != "":
            token += char

        i += 1

    if token:
        tokens.append(convert_if_number(token))

    return tokens


def parse(tokens):
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

    return ast
