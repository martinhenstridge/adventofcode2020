import collections
from . import util


def get_joltages(lines):
    return [int(line) for line in lines]


def count_differences(chain):
    diffs = collections.defaultdict(int)
    for a, b in zip(chain[:-1], chain[1:]):
        diffs[b - a] += 1
    return diffs


def run():
    inputlines = util.get_input_lines("10.txt")
    joltages = get_joltages(inputlines)

    # Add in the special cased joltage values at either end, then sort to get
    # the adapter chain.
    joltages.append(0)
    joltages.append(max(joltages) + 3)
    chain = sorted(joltages)

    diffs = count_differences(chain)
    return (diffs[1] * diffs[3],)
