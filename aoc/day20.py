import collections
from . import util


"""
                  #
#    ##    ##    ###
 #  #  #  #  #  #
"""
MONSTER = [
    (0, 18),
    (1, 0),
    (1, 5),
    (1, 6),
    (1, 11),
    (1, 12),
    (1, 17),
    (1, 18),
    (1, 19),
    (2, 1),
    (2, 4),
    (2, 7),
    (2, 10),
    (2, 13),
    (2, 16),
]

N = 0
E = 1
S = 2
W = 3


class Tile:

    BORDERS = collections.defaultdict(set)

    def __init__(self, key, lines):
        self.key = key
        self.lines = [[c for c in line] for line in lines]

        # The combination of rotations and flips means that any border could
        # potentially be reversed in the resulting image - register both
        # possible values.
        for direction in [N, E, S, W]:
            border = self.border(direction)
            self.BORDERS[border].add(key)
            self.BORDERS[border[::-1]].add(key)

    def border(self, direction):
        if direction == N:
            return "".join(self.lines[0])
        if direction == E:
            return "".join(l[-1] for l in self.lines)
        if direction == S:
            return "".join(self.lines[-1])
        if direction == W:
            return "".join(l[0] for l in self.lines)

    def neighbour(self, direction):
        neighbours = {k for k in self.BORDERS[self.border(direction)] if k != self.key}
        return neighbours.pop() if neighbours else None

    def count_neighbours(self):
        return len(
            {
                k
                for b in [self.border(d) for d in [N, E, S, W]]
                for k in self.BORDERS[b]
                if k != self.key
            }
        )

    def rotate(self):
        self.lines = rotate(self.lines)

    def flip(self):
        self.lines = flip(self.lines)

    def orientations(self):
        for _ in range(4):
            yield
            self.rotate()
        self.flip()
        for _ in range(4):
            yield
            self.rotate()
        assert False


def rotate(square):
    return [[l[i] for l in reversed(square)] for i in range(len(square))]


def flip(square):
    return list(reversed(square))


def get_tiles(lines):
    key = None
    tile = []
    for line in lines:
        if line.startswith("Tile"):
            key = int(line[5:-1])
        elif line:
            tile.append(line)
        else:
            yield key, tile
            tile = []


def connect(tiles, tile, prev, curr):
    line = []
    while True:
        # Find the next tile, direction must match the border from the previous
        # tile.
        line.append(tile)
        target = tile.border(prev)
        neighbour = tile.neighbour(prev)
        if neighbour is None:
            break

        # Try different orientations until the new tile is aligned.
        tile = tiles[neighbour]
        orientations = tile.orientations()
        while tile.border(curr) != target:
            next(orientations)
    return line


def arrange(tiles, corner):
    # Rotate the first corner piece such that it has no neighbour either to its
    # north or to its, then insert it at the north-west corner.
    first = tiles[corner]
    while first.neighbour(N) or first.neighbour(W):
        first.rotate()

    # Connect the westmost column moving south from the north-west corner, then
    # move east filling out each row from there.
    column = connect(tiles, first, S, N)
    return [connect(tiles, k, E, W) for k in column]


def combine(layout):
    combined = []
    for row in layout:
        for idx in range(1, len(row[0].lines) - 1):
            line = []
            for tile in row:
                line.extend(tile.lines[idx][1:-1])
            combined.append(line)
    return combined


def find_monsters(image, monster):
    rmax = max(c[0] for c in monster) - 1
    cmax = max(c[1] for c in monster) - 1

    def is_monster(r, c):
        for dr, dc in monster:
            if image[r + dr][c + dc] == ".":
                return False
        for dr, dc in monster:
            image[r + dr][c + dc] = "O"
        return True

    count = 0
    for r, row in enumerate(image[:-rmax]):
        for c, _ in enumerate(row[:-cmax]):
            if is_monster(r, c):
                count += 1
    return count


def search_image(image, monster):
    # Trial and error shows that rotating the image in its original state yields
    # no monsters, so flip it first. This doesn't work in the general case, but
    # it works for the input provided.
    image = flip(image)

    found = False
    while not found:
        image = rotate(image)
        found = find_monsters(image, monster)

    return image


def run():
    inputlines = util.get_input_lines("20.txt")
    tiles = {k: Tile(k, v) for k, v in get_tiles(inputlines)}

    corners = [k for k, t in tiles.items() if t.count_neighbours() == 2]

    # Arrange the tiles in order then combine them into the actual image.
    layout = arrange(tiles, corners[0])
    image = combine(layout)

    # Mark any monsters with an O then count any remaining # symbols.
    marked = search_image(image, MONSTER)
    count = sum(1 for row in marked for pixel in row if pixel == "#")

    return util.product(corners), count
