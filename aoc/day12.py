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

def update1(position, heading, instruction):
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


def update2(ship, waypoint, instruction):
    key, val = instruction
    sx, sy = ship
    wx, wy = waypoint

    if key == "F":
        sx += wx * val
        sy += wy * val
    elif key == "L":
        for _ in range(val // 90):
            wx, wy = -wy, wx
    elif key == "R":
        for _ in range(val // 90):
            wx, wy = wy, -wx
    elif key == "N":
        wy += val
    elif key == "S":
        wy -= val
    elif key == "E":
        wx += val
    elif key == "W":
        wx -= val
    else:
        assert False

    return (sx, sy), (wx, wy)


def manhattan_distance(position):
    return abs(position[0]) + abs(position[1])


def run():
    inputlines = util.get_input_lines("12.txt")
    instructions = [i for i in get_instructions(inputlines)]

    position, heading = (0, 0), 90
    for instruction in instructions:
        position, heading = update1(position, heading, instruction)
    dist1 = manhattan_distance(position)

    ship, waypoint = (0, 0), (10, 1)
    for instruction in instructions:
        ship, waypoint = update2(ship, waypoint, instruction)
    dist2 = manhattan_distance(ship)

    return (dist1, dist2)
