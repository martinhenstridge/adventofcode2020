from . import util


def get_numbers(lines):
    return [int(line) for line in lines]


def find_invalid(numbers):
    window = set(numbers[:25])
    for idx, target in enumerate(numbers[25:]):
        if not any(target - n != n and target - n in window for n in window):
            return target
        window.remove(numbers[idx])
        window.add(numbers[idx + 25])


def run():
    inputlines = util.get_input_lines("09.txt")
    numbers = get_numbers(inputlines)

    invalid = find_invalid(numbers)

    return (invalid,)
