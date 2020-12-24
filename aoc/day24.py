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


def get_tile_directions(lines):
    for line in lines:
        steps = []
        prefix = ""
        for char in line:
            if char == "n" or char == "s":
                prefix = char
            else:
                steps.append(DIRECTIONS[prefix + char])
                prefix = ""
        yield steps


def find_starting_tiles(directions):
    tiles = set()

    for steps in directions:
        tx = 0
        ty = 0
        for dx, dy in steps:
            tx += dx
            ty += dy
        tile = tx, ty
        if tile not in tiles:
            tiles.add(tile)
        else:
            tiles.discard(tile)

    return tiles


@util.memoize
def find_neighbours(tile):
    return [(tile[0] + dx, tile[1] + dy) for dx, dy in DIRECTIONS.values()]


def evolve_floor(starting, days):
    currgen = starting

    for _ in range(days):
        # Count neighbouring black tiles.
        counts = collections.defaultdict(int)
        for tile in currgen:
            for neighbour in find_neighbours(tile):
                counts[neighbour] += 1

        # Update the floor.
        nextgen = set()
        for tile, count in counts.items():
            if tile in currgen:
                # Tile is currently black.
                if count == 1 or count == 2:
                    nextgen.add(tile)
            else:
                # Tile is currently white.
                if count == 2:
                    nextgen.add(tile)
        currgen = nextgen

    return currgen


def run():
    inputlines = util.get_input_lines("24.txt")
    directions = [d for d in get_tile_directions(inputlines)]

    starting = find_starting_tiles(directions)
    finished = evolve_floor(starting, 100)

    return len(starting), len(finished)
