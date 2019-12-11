import sys
from src.parser import parse, tokenize
from src.interpreter import run_block, profiler


path = sys.argv[1]


if __name__ == "__main__":
    with open(path) as f:
        source = f.read()

    tokens = tokenize(source)
    block = parse(tokens)
    output = run_block(block)
    print(output)
    print("profiler - times called:", profiler.count)
