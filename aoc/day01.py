from . import util


def get_numbers(lines):
    return {int(line) for line in lines}


def find_sum_pair(target, inputs):
    numbers = inputs.copy()
    while numbers:
        n1 = numbers.pop()
        n2 = target - n1
        if n2 in numbers:
            return n1, n2
    raise ValueError


def find_sum_triple(target, inputs):
    numbers = inputs.copy()
    while numbers:
        n1 = numbers.pop()
        try:
            pair = find_sum_pair(target - n1, numbers)
        except ValueError:
            continue
        else:
            return n1, pair[0], pair[1]
    raise ValueError


def run():
    inputlines = util.get_input_lines("01.txt")
    numbers = get_numbers(inputlines)

    pair = find_sum_pair(2020, numbers)
    triple = find_sum_triple(2020, numbers)

    return util.product(pair), util.product(triple)
