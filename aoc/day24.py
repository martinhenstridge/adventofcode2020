import collections
from . import util


DIRECTIONS = {
    "e": (+2, 0),
    "w": (-2, 0),
    "se": (+1, -1),
    "sw": (-1, -1),
    "nw": (-1, +1),
    "ne": (+1, +1),
}

def get_directions(lines):
    for line in lines:
        directions = []
        prefix = ""
        for char in line:
            if char == "n" or char == "s":
                prefix = char
                continue
            directions.append(prefix + char)
            prefix = ""
        yield directions


def run():
    inputlines = util.get_input_lines("24.txt")

    tiles = collections.defaultdict(bool)
    for directions in get_directions(inputlines):
        tx = 0
        ty = 0
        for direction in directions:
            dx, dy = DIRECTIONS[direction]
            tx += dx
            ty += dy
        tiles[tx, ty] = not tiles[tx, ty]
    count = sum(1 for t in tiles.values() if t)

    return count, None
