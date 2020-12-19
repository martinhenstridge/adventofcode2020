from . import util


def get_expressions(lines):
    return [line.replace(" ", "") for line in lines]


def shunting_yard_algo(tokens, precedence):
    output = []
    opstack = []

    for token in tokens:
        if token == "(":
            opstack.append(token)
        elif token == ")":
            while opstack and opstack[-1] != "(":
                op = opstack.pop()
                output.append(op)
            opstack.pop()  # <-- should be "("
        elif token in precedence:
            while (
                opstack
                and opstack[-1] != "("
                and precedence[opstack[-1]] >= precedence[token]
            ):
                op = opstack.pop()
                output.append(op)
            opstack.append(token)
        else:
            output.append(int(token))

    while opstack:
        op = opstack.pop()
        output.append(op)

    return output


def evaluate(rpn):
    stack = []

    for token in rpn:
        if isinstance(token, int):
            stack.append(token)
        elif token == "+":
            result = stack.pop() + stack.pop()
            stack.append(result)
        elif token == "*":
            result = stack.pop() * stack.pop()
            stack.append(result)

    return stack.pop()


def run():
    inputlines = util.get_input_lines("18.txt")
    expressions = get_expressions(inputlines)

    rpns = [shunting_yard_algo(expr, {"+": 0, "*": 0}) for expr in expressions]
    total1 = sum(evaluate(rpn) for rpn in rpns)

    rpns = [shunting_yard_algo(expr, {"+": 1, "*": 0}) for expr in expressions]
    total2 = sum(evaluate(rpn) for rpn in rpns)

    return total1, total2
