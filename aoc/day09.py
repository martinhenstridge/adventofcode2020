from . import util


def get_numbers(lines):
    return [int(line) for line in lines]


def find_invalid(numbers, plen):
    window = set(numbers[:plen])
    for idx, target in enumerate(numbers[plen:]):
        if not any(target - n != n and target - n in window for n in window):
            return target
        window.remove(numbers[idx])
        window.add(numbers[plen + idx])


def find_sequence(numbers, target):
    head = 0
    tail = 0
    total = 0

    while total != target:
        if total < target:
            head += 1
        else:
            tail += 1
        total = sum(numbers[tail:head])

    return numbers[tail:head]


def run():
    inputlines = util.get_input_lines("09.txt")
    numbers = get_numbers(inputlines)

    invalid = find_invalid(numbers, 25)
    sequence = find_sequence(numbers, invalid)

    return (invalid, min(sequence) + max(sequence))
