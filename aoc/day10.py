import collections
from . import util


def get_joltages(lines):
    return [int(line) for line in lines]


def get_joltage_pairs(chain):
    yield from zip(chain[:-1], chain[1:])


def count_differences(chain):
    diffs = collections.defaultdict(int)
    for a, b in get_joltage_pairs(chain):
        diffs[b - a] += 1
    return diffs


# Consecutive adapters in the valid chain all differ from their immediate
# neighbours by either 1 jolt or 3 jolts. Since the maximum allowed difference
# is 3 jolts, the only additional valid chains of adapters are those omitting
# some combination of adapters from a streak of adapters which all differ from
# their neighbours by 1 jolt.
#
# The total number of valid combinations is equal to the product of the number
# of valid combinations for each such streak. The location and contents of each
# streak is irrelevant, only its length is significant.
#
# The longest streak of consecutive joltage values from the input provided has a
# length of 5, and the shortest streak which can possibly have at least one
# adapter removed is of length 3. For this range, all possible permutations are
# listed below:
#
# x x x
# x . x
#
# x x x x
# x . x x
# x x . x
# x . . x
#
# x x x x x
# x . x x x
# x x . x x
# x x x . x
# x . . x x
# x . x . x
# x x . . x
COMBINATIONS = {
    3: 2,
    4: 4,
    5: 7,
}


def find_streaks(chain):
    start = None
    for idx, (a, b) in enumerate(get_joltage_pairs(chain)):
        if b - a == 1:
            if start is None:
                start = idx
        else:
            if start is not None and idx - start > 1:
                yield chain[start : idx + 1]
            start = None


def count_combinations(chain):
    return util.product(COMBINATIONS[len(streak)] for streak in find_streaks(chain))


def run():
    inputlines = util.get_input_lines("10.txt")
    joltages = get_joltages(inputlines)

    # Add in the special cased joltage values at either end, then sort to get
    # the adapter chain.
    joltages.append(0)
    joltages.append(max(joltages) + 3)
    chain = sorted(joltages)

    diffs = count_differences(chain)
    combs = count_combinations(chain)

    return (diffs[1] * diffs[3], combs)
