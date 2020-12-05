from . import util


def apply_f(row, col):
    rmin, rmax = row
    step = (1 + rmax - rmin) // 2
    return (rmin, rmax - step), col


def apply_b(row, col):
    rmin, rmax = row
    step = (1 + rmax - rmin) // 2
    return (rmin + step, rmax), col


def apply_l(row, col):
    cmin, cmax = col
    step = (1 + cmax - cmin) // 2
    return row, (cmin, cmax - step)


def apply_r(row, col):
    cmin, cmax = col
    step = (1 + cmax - cmin) // 2
    return row, (cmin + step, cmax)


APPLY = {
    "F": apply_f,
    "B": apply_b,
    "L": apply_l,
    "R": apply_r,
}


def find_seat(chars):
    row = (0, 127)
    col = (0, 7)

    for char in chars:
        row, col = APPLY[char](row, col)

    assert row[0] == row[1]
    assert col[0] == col[1]

    return row[0], col[0]


def seat_id(row, col):
    return col + (row * 8)


def run():
    inputlines = util.get_input_lines("05.txt")
    seats = [find_seat(line) for line in inputlines]

    idmax = max(seat_id(row, col) for row, col in seats)
    print(idmax)
