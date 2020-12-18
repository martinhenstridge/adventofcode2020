import operator
from . import util


def get_expressions(lines):
    return [parse(line.replace(" ", "")) for line in lines]


def parse(string):
    expr = []
    idx = 0

    while idx < len(string):
        char = string[idx]
        if char.isdigit():
            expr.append(int(char))
        elif char == "+":
            expr.append(operator.add)
        elif char == "*":
            expr.append(operator.mul)
        elif char == "(":
            subexpr, length = parse(string[idx + 1 :])
            expr.append(subexpr)
            idx += length
        elif char == ")":
            return expr, idx + 1
        idx += 1

    return expr, idx


def evaluate(expr):
    acc, expr = expr[0], expr[1:]
    if isinstance(acc, list):
        acc = evaluate(acc)

    while expr:
        op, val, expr = expr[0], expr[1], expr[2:]
        if isinstance(val, list):
            val = evaluate(val)
        acc = op(acc, val)

    return acc


def run():
    inputlines = util.get_input_lines("18.txt")
    expressions = get_expressions(inputlines)

    total = sum(evaluate(e) for e, _ in expressions)

    return (total,)
