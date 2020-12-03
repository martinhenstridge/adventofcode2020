from . import util


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.ymax = len(grid)
        self.xmax = len(grid[0])

    def step(self, start, delta):
        x0, y0 = start
        dx, dy = delta

        x1 = (x0 + dx) % self.xmax
        y1 = y0 + dy

        return x1, y1

    def walk(self, dx, dy):
        locations = []
        x = 0
        y = 0

        while y < self.ymax:
            locations.append((x, y))
            x, y = self.step((x, y), (dx, dy))

        return locations

    def is_tree(self, x, y):
        return self.grid[y][x] == "#"

    def tree_count(self, dx, dy):
        return sum(1 for x, y in self.walk(dx, dy) if self.is_tree(x, y))


def run():
    inputlines = util.get_input_lines("03.txt")
    grid = Grid(inputlines)

    count = grid.tree_count(3, 1)
    print(count)

    product = 1
    for dx, dy in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        product *= grid.tree_count(dx, dy)
    print(product)
