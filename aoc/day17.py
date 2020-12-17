import collections
from . import util


def get_initial_configuration(lines):
    actives = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                actives.append((x, y))
    return actives


DELTAS = [-1, 0, +1]
DIRECTIONS = {
    3: [
        (x, y, z, 0)
        for x in DELTAS
        for y in DELTAS
        for z in DELTAS
        if (x, y, z) != (0, 0, 0)
    ],
    4: [
        (x, y, z, w)
        for x in DELTAS
        for y in DELTAS
        for z in DELTAS
        for w in DELTAS
        if (x, y, z, w) != (0, 0, 0, 0)
    ],
}


def boot(initial, dimensions, steps):
    actives = {(x, y, 0, 0) for x, y in initial}

    for _ in range(steps):
        # Count each currently active cube once for each of its neighbours.
        neighbours = collections.defaultdict(int)
        for cx, cy, cz, cw in actives:
            for dx, dy, dz, dw in DIRECTIONS[dimensions]:
                coord = (cx + dx, cy + dy, cz + dz, cw + dw)
                neighbours[coord] += 1

        nextgen = set()
        # First, consider previously active cubes.
        for cube in actives:
            count = neighbours[cube]
            if count == 2 or count == 3:
                nextgen.add(cube)
        # Next, consider *any* cubes known to have at least one neighbour.
        for cube, count in neighbours.items():
            if cube not in actives and count == 3:
                nextgen.add(cube)
        actives = nextgen

    return actives


def run():
    inputlines = util.get_input_lines("17.txt")
    initial = get_initial_configuration(inputlines)

    actives3d = boot(initial, dimensions=3, steps=6)
    actives4d = boot(initial, dimensions=4, steps=6)

    return len(actives3d), len(actives4d)
