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

    head, expr = expr[0], expr[1:]
    acc = evaluate1(head)

    while expr:
        func, term, expr = expr[0], expr[1], expr[2:]
        acc = func(evaluate1(term), acc)

    return acc


def evaluate2(expr):
    if isinstance(expr, int):
        return expr

    while operator.add in expr:
        for idx, term in enumerate(expr):
            if term is operator.add:
                lval = expr[idx - 1]
                rval = expr[idx + 1]
                added = evaluate2(lval) + evaluate2(rval)
                expr[idx - 1 : idx + 2] = [added]
                break

    return util.product(evaluate2(term) for term in expr if term is not operator.mul)


def run():
    inputlines = util.get_input_lines("18.txt")
    expressions = get_expressions(inputlines)

    total1 = sum(evaluate1(e) for e in expressions)
    total2 = sum(evaluate2(e) for e in expressions)

    return total1, total2
