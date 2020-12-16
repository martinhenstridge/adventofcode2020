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


def invalid_values(ticket, constraints):
    return [v for v in ticket if not is_valid_for_any(v, constraints)]


def assign_fields(constraints, tickets):
    # Initially, every field could appear at any index - nothing is known.
    unknowns = {f: set(range(len(constraints))) for f in constraints}
    knowns = {}

    # Run through all of the valid tickets. For each field, discount any indices
    # with values which do not conform to the constraints for that field.
    for ticket in tickets:
        for idx, val in enumerate(ticket):
            for field, constraint in constraints.items():
                if not is_valid_for_constraint(val, constraint):
                    unknowns[field].discard(idx)

    # When a field is left with only one viable index, move it from the set of
    # "unknowns" into the set of "knowns". We can then also discaount that index
    # as being a possibility for any other field, thus yielding further "known"
    # fields.
    while unknowns:
        for field, options in unknowns.items():
            # The current field remains ambiguous, skip to the next one.
            if len(options) > 1:
                continue

            index = options.pop()
            knowns[field] = index
            del unknowns[field]
            for options in unknowns.values():
                options.discard(index)

            # Break rather than continuing to loop since we've changed the size
            # of the dict being iterated over.
            break

    return knowns


def run():
    inputlines = util.get_input_lines("16.txt")
    constraints, your_ticket, nearby_tickets = parse_info(inputlines)

    error_rate = 0
    valid_tickets = []
    for ticket in nearby_tickets:
        ivs = invalid_values(ticket, constraints)
        if ivs:
            error_rate += sum(ivs)
        else:
            valid_tickets.append(ticket)

    fields = assign_fields(constraints, valid_tickets)
    result = util.product(
        your_ticket[i] for f, i in fields.items() if f.startswith("departure")
    )

    return error_rate, result
