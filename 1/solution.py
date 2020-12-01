def get_numbers(path):
    with open(path) as f:
        return {int(line) for line in f.read().splitlines()}


def find_sum_pair(target, inputs):
    numbers = inputs.copy()
    while numbers:
        n1 = numbers.pop()
        n2 = target - n1
        if n2 in numbers:
            return n1, n2
    raise ValueError


def find_sum_triple(target, inputs):
    numbers = inputs.copy()
    while numbers:
        n1 = numbers.pop()
        try:
            pair = find_sum_pair(target - n1, numbers)
        except ValueError:
            continue
        else:
            return n1, pair[0], pair[1]


def main(path, target):
    numbers = get_numbers(path)

    pair = find_sum_pair(target, numbers)
    product = pair[0] * pair[1]
    print("Pair:")
    print(product, pair)

    triple = find_sum_triple(target, numbers)
    product = triple[0] * triple[1] * triple[2]
    print("Triple:")
    print(product, triple)


if __name__ == "__main__":
    main("input", 2020)
