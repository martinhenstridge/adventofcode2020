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


def is_valid_for_constraint(value, constraint):
    r1, r2 = constraint
    return r1[0] <= value <= r1[1] or r2[0] <= value <= r2[1]


@util.memoize
def is_valid_for_any(value, constraints):
    return any(is_valid_for_constraint(value, c) for c in constraints.values())


def ticket_error(ticket, constraints):
    total = 0
    for value in ticket:
        if not is_valid_for_any(value, constraints):
            total += value
    return total


def assign_fields(constraints, tickets):
    fields = {f: set(range(len(constraints))) for f in constraints}
    for ticket in tickets:
        for idx, val in enumerate(ticket):
            for field, constraint in constraints.items():
                if not is_valid_for_constraint(val, constraint):
                    fields[field].discard(idx)

    while not all(isinstance(i, int) for i in fields.values()):
        for field, idxs in fields.items():
            if isinstance(idxs, set) and len(idxs) == 1:
                known = idxs.pop()
                fields[field] = known
                for idxs in fields.values():
                    if isinstance(idxs, set):
                        idxs.discard(known)
                break

    return fields


def run():
    inputlines = util.get_input_lines("16.txt")
    constraints, your_ticket, nearby_tickets = parse_info(inputlines)

    error_rate = sum(ticket_error(t, constraints) for t in nearby_tickets)

    valid_tickets = [
        t for t in nearby_tickets if all(is_valid_for_any(v, constraints) for v in t)
    ]
    fields = assign_fields(constraints, valid_tickets)
    result = util.product(
        your_ticket[i] for f, i in fields.items() if f.startswith("departure")
    )

    return error_rate, result
