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


def evaluate1(expr):
    if isinstance(expr, int):
        return expr

    # Pop off the first value, the rest of the terms are then (operator, value)
    # pairs.
    head, expr = expr[0], expr[1:]
    acc = evaluate1(head)

    while expr:
        func, term, expr = expr[0], expr[1], expr[2:]
        acc = func(evaluate1(term), acc)

    return acc


def evaluate2(expr):
    if isinstance(expr, int):
        return expr

    for idx, term in enumerate(expr):
        if term is operator.add:
            # Replace [a, +, b] with [*, *, a + b]. The last index in this slice
            # may be read as part of a subsequent addition, hence the result of
            # the addition is stored there. Fill the remaining indices to avoid
            # resizing the list, use operator.mul since that is already being
            # filtered out of the final product calculation.
            expr[idx + 1] = evaluate2(expr[idx - 1]) + evaluate2(expr[idx + 1])
            expr[idx - 1] = operator.mul
            expr[idx] = operator.mul

    # This expression contains no further additions, calculate the product of
    # everything that's left.
    return util.product(evaluate2(term) for term in expr if term is not operator.mul)


def run():
    inputlines = util.get_input_lines("18.txt")
    expressions = get_expressions(inputlines)

    total1 = sum(evaluate1(e) for e in expressions)
    total2 = sum(evaluate2(e) for e in expressions)

    return total1, total2
