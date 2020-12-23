from . import util


class Cup:
    def __init__(self, val):
        self.val = val
        self.next = None


def get_cups(lines):
    return [int(cup) for cup in lines[0]]


def construct_ring(vals):
    cups = {}
    tail = Cup(None)

    # Connect cups together in a linked list.
    for val in vals:
        cup = Cup(val)
        cups[val] = cup
        tail.next = cup
        tail = cup

    # Connect the tail around to the head to make a ring.
    tail.next = cups[vals[0]]
    return cups


def get_cups_after(cups, val, count):
    result = []

    cup = cups[val]
    for _ in range(count):
        cup = cup.next
        result.append(cup.val)

    return result


def play(vals, turns, retcount):
    cups = construct_ring(vals)
    size = len(vals)

    curr_cup = cups[vals[0]]
    for _ in range(turns):
        # Pick out the following three cups. Leave them connected up for now -
        # they may not actually need to be moved.
        picked_cups = []
        picked_head = curr_cup.next
        picked_tail = curr_cup
        for _ in range(3):
            picked_tail = picked_tail.next
            picked_cups.append(picked_tail.val)

        # Decide where to re-insert them.
        dest_val = (curr_cup.val - 1) % size
        while dest_val in picked_cups:
            dest_val = (dest_val - 1) % size
        dest_cup = cups[dest_val]

        # Re-insert cups, noting that work is only required in the case that
        # they're actually being moved from their starting position.
        if dest_cup.val != curr_cup.val:
            curr_cup.next = picked_tail.next
            picked_tail.next = dest_cup.next
            dest_cup.next = picked_head

        # Move around the ring to the next cup.
        curr_cup = curr_cup.next

    return get_cups_after(cups, 0, retcount)


def run():
    inputlines = util.get_input_lines("23.txt")
    cups = get_cups(inputlines)

    # Shift cup values by -1 to allow use of modulo arithmetic.
    starting = [c - 1 for c in cups]
    finished = play(starting, 100, len(cups) - 1)
    result1 = int("".join([str(c + 1) for c in finished]))

    # Ditto shift by -1, plus expand to 1 million cups.
    starting = [c - 1 for c in cups] + list(range(len(cups), 1000000))
    finished = play(starting, 10000000, 2)
    result2 = (finished[0] + 1) * (finished[1] + 1)

    return result1, result2
