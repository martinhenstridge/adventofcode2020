import re
from enum import Enum
from . import util


class Mode(Enum):
    SKIP = 0
    CONSTRAINT = 1
    YOUR_TICKET = 2
    NEARBY_TICKETS = 3


def parse_constraint(line):
    match = re.fullmatch(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)", line)
    return match[1], (int(match[2]), int(match[3])), (int(match[4]), int(match[5]))


def parse_ticket(line):
    return [int(val) for val in line.split(",")]


def parse_info(lines):
    constraints = {}
    your_ticket = None
    nearby_tickets = []

    mode = Mode.CONSTRAINT
    for line in lines:
        if not line:
            mode = Mode.SKIP
        elif line == "your ticket:":
            mode = Mode.YOUR_TICKET
        elif line == "nearby tickets:":
            mode = Mode.NEARBY_TICKETS
        elif mode == Mode.CONSTRAINT:
            key, range1, range2 = parse_constraint(line)
            constraints[key] = (range1, range2)
        elif mode == Mode.YOUR_TICKET:
            your_ticket = parse_ticket(line)
        elif mode == Mode.NEARBY_TICKETS:
            nearby_tickets.append(parse_ticket(line))
        else:
            assert False

    return constraints, your_ticket, nearby_tickets


@util.memoize
def is_value_valid(value, constraints):
    return any(
        r1[0] <= value <= r1[1] or r2[0] <= value <= r2[1]
        for r1, r2 in constraints.values()
    )


def ticket_error_rate(ticket, constraints):
    total = 0
    for value in ticket:
        if not is_value_valid(value, constraints):
            total += value
    return total


EXAMPLE = [
    "class: 1-3 or 5-7",
    "row: 6-11 or 33-44",
    "seat: 13-40 or 45-50",
    "",
    "your ticket:",
    "7,1,14",
    "",
    "nearby tickets:",
    "7,3,47",
    "40,4,50",
    "55,2,20",
    "38,6,12",
]


def run():
    inputlines = util.get_input_lines("16.txt")
    constraints, your_ticket, nearby_tickets = parse_info(inputlines)

    error_rate = sum(ticket_error_rate(t, constraints) for t in nearby_tickets)

    return (error_rate,)
