from . import util


def get_starting_numbers(lines):
    return [int(n) for n in lines[0].split(",")]


def play(starting, count):
    turns = [None] * count

    for idx, num in enumerate(starting):
        turns[num] = (idx, idx)

    num = starting[-1]
    for idx in range(len(starting), count):
        num = turns[num][0] - turns[num][1]
        if turns[num] is None:
            turns[num] = (idx, idx)
        else:
            turns[num] = (idx, turns[num][0])
    return num


def run():
    inputlines = util.get_input_lines("15.txt")
    starting = get_starting_numbers(inputlines)

    number1 = play(starting, 2020)
    number2 = play(starting, 30000000)

    return number1, number2
