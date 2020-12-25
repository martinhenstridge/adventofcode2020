from . import util


def get_public_keys(lines):
    return tuple(int(l) for l in lines)


def transform_subject(subject, loop_size):
    return pow(subject, loop_size, 20201227)


def find_loop_size(public_key):
    value = 1
    count = 0
    while value != public_key:
        value = (value * 7) % 20201227
        count += 1
    return count


def run():
    inputlines = util.get_input_lines("25.txt")
    public_keys = get_public_keys(inputlines)

    # The encryption key must be the same whether we calculate it from the door
    # credentials or the card credentials, so we only need to reverse engineer
    # the loop size for one of them.
    loop_size = find_loop_size(public_keys[0])
    encryption_key = transform_subject(public_keys[1], loop_size)

    return encryption_key, None
