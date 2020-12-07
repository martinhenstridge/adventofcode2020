import re
from . import util


def get_entries(lines):
    def parse_line(line):
        match = re.match(r"(\d+)-(\d+) (\w)\: (\w+)", line)
        assert match is not None
        return match[3], int(match[1]), int(match[2]), match[4]
    return [parse_line(line) for line in lines]


def is_valid_1(char, nmin, nmax, password):
    count = sum(1 for c in password if c == char)
    if count < nmin:
        return False
    if count > nmax:
        return False
    return True


def is_valid_2(char, index1, index2, password):
    match1 = password[index1 - 1] == char
    match2 = password[index2 - 1] == char
    return match1 != match2


def run():
    inputlines = util.get_input_lines("02.txt")
    entries = get_entries(inputlines)

    count_1 = sum(1 for e in entries if is_valid_1(*e))
    count_2 = sum(1 for e in entries if is_valid_2(*e))

    return count_1, count_2
