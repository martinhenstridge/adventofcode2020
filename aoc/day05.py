from . import util


def apply_f(rows, cols):
    rmin, rmax = rows
    step = (1 + rmax - rmin) // 2
    return (rmin, rmax - step), cols


def apply_b(rows, cols):
    rmin, rmax = rows
    step = (1 + rmax - rmin) // 2
    return (rmin + step, rmax), cols


def apply_l(rows, cols):
    cmin, cmax = cols
    step = (1 + cmax - cmin) // 2
    return rows, (cmin, cmax - step)


def apply_r(rows, cols):
    cmin, cmax = cols
    step = (1 + cmax - cmin) // 2
    return rows, (cmin + step, cmax)


APPLY = {
    "F": apply_f,
    "B": apply_b,
    "L": apply_l,
    "R": apply_r,
}


def get_seatid(chars):
    rows = (0, 127)
    cols = (0, 7)

    for char in chars:
        rows, cols = APPLY[char](rows, cols)

    assert rows[0] == rows[1]
    assert cols[0] == cols[1]

    return cols[0] + (8 * rows[0])


def find_vacant_seat(filled):
    vacant = {seatid for seatid in range(128 * 8) if seatid not in filled}
    for seatid in vacant:
        if (seatid + 1) in vacant:
            continue
        if (seatid - 1) in vacant:
            continue
        return seatid
    assert False


def run():
    inputlines = util.get_input_lines("05.txt")
    seatids = {get_seatid(line) for line in inputlines}

    maxid = max(seatids)
    myseat = find_vacant_seat(seatids)

    return maxid, myseat
