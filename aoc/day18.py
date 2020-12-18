import operator
from . import util


def get_expressions(lines):
    return [line.replace(" ", "") for line in lines]


def evaluate(expr):
    acc = 0
    op = operator.add

    while expr:
        char, expr = expr[0], expr[1:]
        if char == "+":
            op = operator.add
        elif char == "*":
            op = operator.mul
        elif char == "(":
            val, expr = evaluate(expr)
            acc = op(val, acc)
        elif char == ")":
            return acc, expr
        else:
            acc = op(int(char), acc)


    return acc, []


def run():
    inputlines = util.get_input_lines("18.txt")
    expressions = get_expressions(inputlines)

    total = sum(evaluate(e)[0] for e in expressions)

    return (total,)
