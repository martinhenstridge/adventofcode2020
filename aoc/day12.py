from . import util


def get_instructions(lines):
    for line in lines:
        yield line[0], int(line[1:])


def update1(ship, heading, instruction):
    key, val = instruction
    sx, sy = ship
    dx, dy = heading

    if key == "F":
        sx += dx * val
        sy += dy * val
    elif key == "L":
        for _ in range(val // 90):
            dx, dy = -dy, dx
    elif key == "R":
        for _ in range(val // 90):
            dx, dy = dy, -dx
    elif key == "N":
        sy += val
    elif key == "S":
        sy -= val
    elif key == "E":
        sx += val
    elif key == "W":
        sx -= val
    else:
        assert False

    return (sx, sy), (dx, dy)


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

    ship, heading = (0, 0), (1, 0)
    for instruction in instructions:
        ship, heading = update1(ship, heading, instruction)
    dist1 = manhattan_distance(ship)

    ship, waypoint = (0, 0), (10, 1)
    for instruction in instructions:
        ship, waypoint = update2(ship, waypoint, instruction)
    dist2 = manhattan_distance(ship)

    return (dist1, dist2)
