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

    def update(self):
        prev = self.seats.copy()
        changed = False

        for idx, seat in enumerate(prev):
            if seat == "L":
                for n in self.neighbours[idx]:
                    if prev[n] == "#":
                        break
                else:
                    self.seats[idx] = "#"
                    changed = True
            elif seat == "#":
                count = 0
                for n in self.neighbours[idx]:
                    if prev[n] == "#":
                        count += 1
                        if count == self.THRESHOLD:
                            self.seats[idx] = "L"
                            changed = True
                            break
        return not changed

    def occupied(self):
        return sum(1 for seat in self.seats if seat == "#")


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
