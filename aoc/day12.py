from . import util


def get_instructions(lines):
    for line in lines:
        yield line[0], int(line[1:])


HEADING = {
    0: (0, +1),
    90: (+1, 0),
    180: (0, -1),
    270: (-1, 0),
}

def update(position, heading, instruction):
    key, val = instruction
    x, y = position

    if key == "F":
        dx, dy = HEADING[heading]
        x += dx * val
        y += dy * val
    elif key == "L":
        heading = (heading - val) % 360
    elif key == "R":
        heading = (heading + val) % 360
    elif key == "N":
        y += val
    elif key == "S":
        y -= val
    elif key == "E":
        x += val
    elif key == "W":
        x -= val
    else:
        assert False

    return (x, y), heading


def manhattan_distance(position):
    return abs(position[0]) + abs(position[1])


def run():
    inputlines = util.get_input_lines("12.txt")

    position, heading = (0, 0), 90
    for instruction in get_instructions(inputlines):
        position, heading = update(position, heading, instruction)
    dist = manhattan_distance(position)

    return (dist,)
