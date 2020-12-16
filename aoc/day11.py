from . import util


class WaitingRoom:

    def __init__(self, lines, threshold, find_neighbours):
        self.seats = [char for line in lines for char in line]
        self.rowmax = len(lines)
        self.colmax = len(lines[0])
        self.threshold = threshold

        # Pre-compute the set of neighbours for each seat.
        self.neighbours = [
            find_neighbours(self.seats, self.rowmax, self.colmax, row, col)
            if lines[row][col] != "." else []
            for row in range(self.rowmax)
            for col in range(self.colmax)
        ]

    def update(self):
        # The neighbour relationship is reciprocal, so any occupied seat counts
        # once for each of its neighbours. Pre-counting the number of occupied
        # neighbours is much faster than doing it on the fly.
        counts = [0] * len(self.seats)
        for idx, seat in enumerate(self.seats):
            if seat == "#":
                for neighbour in self.neighbours[idx]:
                    counts[neighbour] += 1

        changed = False
        for idx, seat in enumerate(self.seats):
            if seat == "L":
                if counts[idx] == 0:
                    self.seats[idx] = "#"
                    changed = True
            elif seat == "#":
                if counts[idx] >= self.threshold:
                    self.seats[idx] = "L"
                    changed = True
        return changed

    def run(self):
        unstable = True
        while unstable:
            unstable = self.update()
        return sum(1 for seat in self.seats if seat == "#")


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


def find_neighbours1(seats, rowmax, colmax, row, col):
    neighbours = []
    for drow, dcol in DIRECTIONS:
        nrow = row + drow
        ncol = col + dcol
        nidx = ncol + (nrow * colmax)
        if nrow < 0 or nrow >= rowmax:
            continue
        if ncol < 0 or ncol >= colmax:
            continue
        if seats[nidx] == ".":
            continue
        neighbours.append(nidx)
    return neighbours


def find_neighbours2(seats, rowmax, colmax, row, col):
    neighbours = []
    for drow, dcol in DIRECTIONS:
        nrow = row
        ncol = col
        while True:
            nrow += drow
            ncol += dcol
            nidx = ncol + (nrow * colmax)
            if nrow < 0 or nrow >= rowmax:
                break
            if ncol < 0 or ncol >= colmax:
                break
            if seats[nidx] == "L":
                neighbours.append(nidx)
                break
    return neighbours


def run():
    inputlines = util.get_input_lines("11.txt")

    wr1 = WaitingRoom(inputlines, 4, find_neighbours1)
    count1 = wr1.run()

    wr2 = WaitingRoom(inputlines, 5, find_neighbours2)
    count2 = wr2.run()

    return count1, count2
