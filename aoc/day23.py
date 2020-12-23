from . import util


class Cup:
    __slots__ = "val", "next"

    def __init__(self, val):
        self.val = val
        self.next = None


def get_cups(lines):
    return [int(cup) for cup in lines[0]]


def construct_ring(vals):
    cups = [None] * len(vals)
    tail = Cup(None)

    # Connect cups together in a linked list.
    for val in vals:
        cup = Cup(val)
        cups[val] = cup
        tail.next = cup
        tail = cup

    # Connect the tail around to the head to make a ring.
    head = cups[vals[0]]
    tail.next = head
    return cups, head


def get_cups_after(cups, val, count):
    result = []

    cup = cups[val]
    for _ in range(count):
        cup = cup.next
        result.append(cup.val)

    return result


def play(vals, turns, retcount):
    size = len(vals)
    cups, curr = construct_ring(vals)

    for _ in range(turns):
        # Pick out the following three cups. Leave them connected up for now -
        # they may not actually need to be moved.
        picked_cups = []
        picked_head = curr.next
        picked_tail = curr
        for _ in range(3):
            picked_tail = picked_tail.next
            picked_cups.append(picked_tail.val)

        # Decide where to re-insert them.
        val = (curr.val - 1) % size
        while val in picked_cups:
            val = (val - 1) % size
        dest = cups[val]

        # Re-insert cups, noting that work is only required in the case that
        # they're actually being moved from their starting position.
        if dest.val != curr.val:
            curr.next = picked_tail.next
            picked_tail.next = dest.next
            dest.next = picked_head

        # Move around the ring to the next cup.
        curr = curr.next

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
