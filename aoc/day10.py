import collections
from . import util


def get_joltages(lines):
    return [int(line) for line in lines]


def count_differences(chain):
    diffs = collections.defaultdict(int)
    for a, b in zip(chain[:-1], chain[1:]):
        diffs[b - a] += 1
    return diffs


# Consecutive adapters in the valid chain all differ from their neighbours by
# either 1 jolt or 3 jolts. Since the maximum allowed difference is 3 jolts, the
# only extra valid chains of adapters are those which remove some combination of
# adapters which differ from their neighboutrs by 1 jolt.
#
# The longest streak of consecutive joltage values is 5, and the shorted streak
# which can possibly have at least one adapter removed is 3. For this range, the
# possible combinations are listed below:
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
    streak = 0
    for a, b in zip(chain[:-1], chain[1:]):
        if b - a == 1:
            if streak == 0:
                streak = 1
            streak += 1
        else:
            if streak > 2:
                yield streak
            streak = 0


def run():
    inputlines = util.get_input_lines("10.txt")
    joltages = get_joltages(inputlines)

    # Add in the special cased joltage values at either end, then sort to get
    # the adapter chain.
    joltages.append(0)
    joltages.append(max(joltages) + 3)
    chain = sorted(joltages)

    diffs = count_differences(chain)
    combs = util.product(COMBINATIONS[streak] for streak in find_streaks(chain))

    return (diffs[1] * diffs[3], combs)
