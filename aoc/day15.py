from . import util


def get_starting_numbers(lines):
    return [int(n) for n in lines[0].split(",")]


def play(starting, count):
    # Using a dict here uses a *lot* less memory (especially during part 2), but
    # takes around twice as long to run.
    history = [None] * count

    # Bootstrap the game using the starting numbers. Avoid inserting the last
    # number into the history until we've used its presence (or otherwise) there
    # to determine the next number.
    for idx, num in enumerate(starting[:-1]):
        history[num] = idx
    prevnum = starting[-1]
    previdx = len(starting) - 1

    for idx in range(len(starting), count):
        num = 0 if history[prevnum] is None else previdx - history[prevnum]
        history[prevnum] = previdx
        prevnum = num
        previdx = idx

    return num


def run():
    inputlines = util.get_input_lines("15.txt")
    starting = get_starting_numbers(inputlines)

    number1 = play(starting, 2020)
    number2 = play(starting, 30000000)

    return number1, number2
