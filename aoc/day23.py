from . import util


def get_cups(lines):
    return [int(cup) for cup in lines[0]]


def construct_ring(vals, length):
    cups = [0] * length

    # Connect cups together in a linked list, the value is the index of the next
    # entry in the list.
    head = vals[0]
    prev = head
    for curr in vals[1:]:
        cups[prev] = curr
        prev = curr
    for curr in range(len(vals), length):
        cups[prev] = curr
        prev = curr

    # Connect the tail around to the head to make a ring.
    cups[prev] = head

    return cups, head


def get_following_cups(cups, count):
    result = []

    cup = 0
    for _ in range(count):
        cup = cups[cup]
        result.append(cup)

    return result


def play(cups, first, turns):
    size = len(cups)
    curr = first

    for _ in range(turns):
        # Pick out the following three cups. Leave them connected up for now -
        # they may not actually need to be moved.
        picked_cups = []
        picked_head = cups[curr]
        picked_tail = curr
        for _ in range(3):
            picked_tail = cups[picked_tail]
            picked_cups.append(picked_tail)

        # Decide where to re-insert them.
        dest = (curr - 1) % size
        while dest in picked_cups:
            dest = (dest - 1) % size

        # Re-insert cups, noting that work is only required in the case that
        # they're actually being moved from their starting position.
        if dest != curr:
            cups[curr] = cups[picked_tail]
            cups[picked_tail] = cups[dest]
            cups[dest] = picked_head

        # Move around the ring to the next cup.
        curr = cups[curr]

    return cups


def run():
    inputlines = util.get_input_lines("23.txt")
    cups = get_cups(inputlines)

    # Shift cup values by -1 to allow use of modulo arithmetic.
    starting, first = construct_ring([c - 1 for c in cups], len(cups))
    finished = play(starting, first, 100)
    following = get_following_cups(finished, len(starting) - 1)
    result1 = int("".join([str(c + 1) for c in following]))

    # Ditto shift by -1, plus expand to 1 million cups.
    starting, first = construct_ring([c - 1 for c in cups], 1000000)
    finished = play(starting, first, 10000000)
    following = get_following_cups(finished, 2)
    result2 = util.product([c + 1 for c in following])

    return result1, result2
