import collections
from . import util


def get_initial_configuration(lines):
    active_cubes = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                active_cubes.add((x, y, 0))
    return active_cubes


_DELTAS = [-1, 0, +1]
DIRECTIONS = [
    (x, y, z)
    for x in _DELTAS
    for y in _DELTAS
    for z in _DELTAS
    if (x, y, z) != (0, 0, 0)
]


def run():
    inputlines = util.get_input_lines("17.txt")
    active_cubes = get_initial_configuration(inputlines)

    for _ in range(6):
        # Count each currently active cube once for each of its neighbours.
        neighbours = collections.defaultdict(int)
        for cx, cy, cz in active_cubes:
            for dx, dy, dz in DIRECTIONS:
                neighbours[cx + dx, cy + dy, cz + dz] += 1

        next_gen = set()
        # First, consider previously active cubes.
        for cube in active_cubes:
            count = neighbours[cube]
            if count == 2 or count == 3:
                next_gen.add(cube)
        # Next, consider *any* cubes known to have at least one neighbour.
        for cube, count in neighbours.items():
            if cube not in active_cubes and count == 3:
                next_gen.add(cube)

        active_cubes = next_gen

    return len(active_cubes),
