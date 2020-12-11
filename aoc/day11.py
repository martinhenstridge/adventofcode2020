from . import util


class Grid:
    THRESHOLD = 0
    DIRECTIONS = [
        (-1, -1),
        (-1, +0),
        (-1, +1),
        (+0, -1),
        (+0, +1),
        (+1, -1),
        (+1, +0),
        (+1, +1),
    ]

    def __init__(self, lines):
        self.seats = lines
        self.numrows = len(lines)
        self.numcols = len(lines[0])

        self.neighbours = [
            [self.precompute_neighbours(row, col) for col in range(self.numcols)]
            for row in range(self.numrows)
        ]

    def precompute_neighbours(self, row, col):
        raise NotImplementedError

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
                    if count == self.THRESHOLD:
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


class Grid1(Grid):
    THRESHOLD = 4

    def precompute_neighbours(self, row, col):
        neighbours = []
        for drow, dcol in self.DIRECTIONS:
            nrow = row + drow
            ncol = col + dcol
            if nrow < 0 or nrow >= self.numrows:
                continue
            if ncol < 0 or ncol >= self.numcols:
                continue
            neighbours.append((nrow, ncol))
        return neighbours


class Grid2(Grid):
    THRESHOLD = 5

    def precompute_neighbours(self, row, col):
        neighbours = []
        for drow, dcol in self.DIRECTIONS:
            nrow = row
            ncol = col
            while True:
                nrow += drow
                ncol += dcol
                if nrow < 0 or nrow >= self.numrows:
                    break
                if ncol < 0 or ncol >= self.numcols:
                    break
                if self.seats[nrow][ncol] == "L":
                    neighbours.append((nrow, ncol))
                    break
        return neighbours


def run():
    inputlines = util.get_input_lines("11.txt")

    grid1 = Grid1(inputlines)
    stable = False
    while not stable:
        stable = grid1.update()

    grid2 = Grid2(inputlines)
    stable = False
    while not stable:
        stable = grid2.update()

    return (grid1.occupied(), grid2.occupied())
