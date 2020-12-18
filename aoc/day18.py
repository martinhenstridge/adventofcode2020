import operator
from . import util


def get_expressions(lines):
    return [parse(line.replace(" ", "")) for line in lines]


def parse(string):
    expr = []

    while string:
        char, string = string[0], string[1:]
        if char == "(":
            subexpr, string = parse(string)
            expr.append(subexpr)
        elif char == ")":
            return expr, string
        elif char == "+":
            expr.append(operator.add)
        elif char == "*":
            expr.append(operator.mul)
        else:
            expr.append(int(char))

    return expr


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

    total = sum(evaluate(e) for e in expressions)

    return (total,)
