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
        self.rowmax = len(lines)
        self.colmax = len(lines[0])
        self.seats = [char for line in lines for char in line]

        self.neighbours = [
            self.precompute_neighbours(row, col)
            for row in range(self.rowmax)
            for col in range(self.colmax)
        ]

    def precompute_neighbours(self, row, col):
        raise NotImplementedError

    def nextgen(self, idx):
        curr = self.seats[idx]
        if curr == "L":
            for neighbour in self.neighbours[idx]:
                if self.seats[neighbour] == "#":
                    return curr
            return "#"
        if curr == "#":
            count = 0
            for neighbour in self.neighbours[idx]:
                if self.seats[neighbour] == "#":
                    count += 1
                    if count == self.THRESHOLD:
                        return "L"
        return curr

    def update(self):
        updated = [self.nextgen(idx) for idx in range(len(self.seats))]
        stable = updated == self.seats
        self.seats = updated
        return stable

    def occupied(self):
        return sum(1 for seat in self.seats if seat == "#")

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
            nidx = ncol + (nrow * self.colmax)
            if nrow < 0 or nrow >= self.rowmax:
                continue
            if ncol < 0 or ncol >= self.colmax:
                continue
            if self.seats[nidx] == ".":
                continue
            neighbours.append(nidx)
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
                nidx = ncol + (nrow * self.colmax)
                if nrow < 0 or nrow >= self.rowmax:
                    break
                if ncol < 0 or ncol >= self.colmax:
                    break
                if self.seats[nidx] == "L":
                    neighbours.append(nidx)
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
