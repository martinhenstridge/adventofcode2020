from . import util


class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.rows = len(lines)
        self.cols = len(lines[0])

    def neighbours(self, row, col):
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if r != row or c != col:
                    yield self.lines[r][c]

    def nextgen(self, row, col):
        curr = self.lines[row][col]
        if curr == "L":
            if not any(seat == "#" for seat in self.neighbours(row, col)):
                return "#"
        elif curr == "#":
            if sum(1 for seat in self.neighbours(row, col) if seat == "#") > 3:
                return "L"
        return curr

    def update(self):
        newlines = [
            "".join(self.nextgen(row, col) for col in range(self.cols)) for row in range(self.rows)
        ]
        stable = (newlines == self.lines)

        self.lines = newlines
        return stable

    def occupied(self):
        return sum(1 for line in self.lines for seat in line if seat == "#")


def run():
    inputlines = util.get_input_lines("11.txt")

    grid = Grid(inputlines)
    stable = False
    while not stable:
        stable = grid.update()

    return (grid.occupied(),)
