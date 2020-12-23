from . import util


def get_cups(lines):
    return [int(cup) for cup in lines[0]]


def play(cups, turns):
    for _ in range(turns):
        curr = cups[0]
        three = cups[1:4]

        # Work out where to move the cups to.
        dest = curr - 1
        if dest == 0:
            dest = 9
        while dest in three:
            dest -= 1
            if dest == 0:
                dest = 9
        didx = cups.index(dest)

        # Work out which cups to move to make space.
        if didx == 0:
            count = 0
        else:
            count = didx - 3
            cups[1:1+count] = cups[4:4+count]
        cups[1+count:4+count] = three

        # Rotate the list to move the next "current" cup to position 0.
        cups.append(cups.pop(0))
    return cups


EXAMPLE = ["389125467"]

def run():
    inputlines = util.get_input_lines("23.txt")
    #inputlines = EXAMPLE
    cups = get_cups(inputlines)

    sequence = play(cups.copy(), 100)
    string = "".join(str(cup) for cup in sequence)
    before, after = string.split("1")
    result = int(after + before)

    return result, None
