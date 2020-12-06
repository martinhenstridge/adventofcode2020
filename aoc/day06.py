import re
from . import util


def get_groups(lines):
    parts = []
    for line in lines:
        if line:
            parts.append(line)
        else:
            yield "".join(parts)
            parts = []
    yield "".join(parts)


def run():
    inputlines = util.get_input_lines("06.txt")
    groups = [set(group) for group in get_groups(inputlines)]

    countsum = sum(len(group) for group in groups)
    print(countsum)
