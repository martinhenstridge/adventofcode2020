from . import util


def get_starting_numbers(lines):
    return [int(n) for n in lines[0].split(",")]


def game(starting):
    turns = {}

    for idx, num in enumerate(starting):
        turns[num] = (idx, idx)
        yield num

    idx = len(starting)
    num = starting[-1]
    while True:
        num = turns[num][0] - turns[num][1]
        if num in turns:
            turns[num] = (idx, turns[num][0])
        else:
            turns[num] = (idx, idx)
        yield num
        idx += 1


def play(generator, count):
    for _ in range(count):
        result = next(generator)
    return result


def run():
    inputlines = util.get_input_lines("15.txt")
    starting = get_starting_numbers(inputlines)

    number1 = play(game(starting), 2020)
    number2 = play(game(starting), 30000000)

    return number1, number2
