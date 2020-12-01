def get_numbers(path):
    with open(path) as f:
        return [int(line) for line in f.read().splitlines()]


def find_sum_pair(target, numbers):
    while numbers:
        head, tail = numbers[0], numbers[1:]
        for candidate in tail:
            if head + candidate == target:
                return (head, candidate)
        numbers = tail
    raise ValueError


def main(path, target):
    numbers = get_numbers(path)
    a, b = find_sum_pair(target, numbers)
    return a * b


if __name__ == "__main__":
    result = main("input", 2020)
    print(result)
