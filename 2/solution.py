import re


def get_entries(path):
    # 5-11 t: glhbttzvzttkdx
    def parse_line(line):
        match = re.match(r"(\d+)-(\d+) (\w)\: (\w+)", line)
        assert match is not None
        return match[3], int(match[1]), int(match[2]), match[4]
        
    with open(path) as f:
        return [parse_line(line) for line in f.read().splitlines()]


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


def main(path):
    entries = get_entries(path)

    count = sum(1 for e in entries if is_valid_1(*e))
    print(count)

    count = sum(1 for e in entries if is_valid_2(*e))
    print(count)


if __name__ == "__main__":
    main("input")
