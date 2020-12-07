from . import util


DIGITS = {
    "F": 0,
    "B": 1,
    "L": 0,
    "R": 1,
}


def get_seatid(chars):
    # Input maps to seat ID in binary, with F|L = 0 and B|R = 1.
    seatid = 0
    for char in chars:
        seatid = DIGITS[char] + (2 * seatid)
    return seatid


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
