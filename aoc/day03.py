from . import util


class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.ymax = len(lines)
        self.xmax = len(lines[0])

    def walk(self, dx, dy):
        x = 0
        y = 0
        while y < self.ymax:
            yield x, y
            x, y = (x + dx) % self.xmax, y + dy

    def count(self, symbol, dx, dy):
        return sum(1 for x, y in self.walk(dx, dy) if self.lines[y][x] == symbol)


def run():
    inputlines = util.get_input_lines("03.txt")
    grid = Grid(inputlines)

    count = grid.count("#", 3, 1)
    print(count)

    product = 1
    for dx, dy in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        product *= grid.count("#", dx, dy)
    print(product)
