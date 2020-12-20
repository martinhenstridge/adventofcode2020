import collections
from . import util


class Tile:

    SIDEMAP = collections.defaultdict(set)

    def __init__(self, key, lines):
        self.key = key
        self.t = lines[0]
        self.b = lines[-1]
        self.l = "".join(line[0] for line in lines)
        self.r = "".join(line[-1] for line in lines)

        for side in self.sides:
            self.SIDEMAP[side].add(key)
            self.SIDEMAP[side[::-1]].add(key)

    @property
    def sides(self):
        return [self.t, self.r, self.b, self.l]

    @property
    def neighbours(self):
        return {n for s in self.sides for n in self.SIDEMAP[s] if n != self.key}

    def rotate(self):
        self.t, self.r, self.b, self.l = self.l[::-1], self.t, self.r[::-1], self.b


def get_tiles(lines):
    key = 0
    tile = []
    for line in lines:
        if line.startswith("Tile"):
            key = int(line[5:-1])
        elif line:
            tile.append(line)
        else:
            yield key, tile
            tile = []


def run():
    inputlines = util.get_input_lines("20.txt")
    tiles = {k: Tile(k, v) for k, v in get_tiles(inputlines)}

    corners = [k for k, t in tiles.items() if len(t.neighbours) == 2]

    return util.product(corners),
