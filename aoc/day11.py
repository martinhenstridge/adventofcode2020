from . import util


class Grid:
    def __init__(self, lines):
        self.seats = lines
        self.numrows = len(lines)
        self.numcols = len(lines[0])

        self.neighbours = [
            [self.precompute_neighbours(row, col) for col in range(self.numcols)]
            for row in range(self.numrows)
        ]

    NEIGHBOURS = [
        (-1, -1),
        (-1, +0),
        (-1, +1),
        (+0, -1),
        (+0, +1),
        (+1, -1),
        (+1, +0),
        (+1, +1),
    ]

    def precompute_neighbours(self, row, col):
        neighbours = []
        for drow, dcol in self.NEIGHBOURS:
            nrow, ncol = row + drow, col + dcol
            if nrow >= 0 and nrow < self.numrows and ncol >= 0 and ncol < self.numcols:
                neighbours.append((nrow, ncol))
        return neighbours

    def nextgen(self, row, col):
        curr = self.seats[row][col]
        if curr == "L":
            for r, c in self.neighbours[row][col]:
                if self.seats[r][c] == "#":
                    return curr
            return "#"
        if curr == "#":
            count = 0
            for r, c in self.neighbours[row][col]:
                if self.seats[r][c] == "#":
                    count += 1
                    if count == 4:
                        return "L"
        return curr

    def update(self):
        newseats = [
            "".join(self.nextgen(row, col) for col in range(self.numcols))
            for row in range(self.numrows)
        ]
        stable = newseats == self.seats

        self.seats = newseats
        return stable

    def occupied(self):
        return sum(1 for row in self.seats for seat in row if seat == "#")

    def dump(self):
        for row in self.seats:
            print(row)


def run():
    inputlines = util.get_input_lines("11.txt")

    grid = Grid(inputlines)
    stable = False
    while not stable:
        stable = grid.update()

    return (grid.occupied(),)
