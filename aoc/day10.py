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


def count_permutations(subsection):
    # As it happens, in the current input dataset, all differences < 3 jolts are
    # exactly 1 jolt. This means the contents of each section is irrelevant,
    # only its length is significant when counting permutations.
    for a, b in get_joltage_pairs(subsection):
        assert b - a == 1

    # Within the current input dataset, the longest streak of consecutive values
    # is of length 5. The shortest possible streak is of length 2. All possible
    # permutations for sections of these lengths are listed below:
    #
    # 1 - x x
    #
    # 1 - x x x
    # 2 - x . x
    #
    # 1 - x x x x
    # 2 - x . x x
    # 3 - x x . x
    # 4 - x . . x
    #
    # 1 - x x x x x
    # 2 - x . x x x
    # 3 - x x . x x
    # 4 - x x x . x
    # 5 - x . . x x
    # 6 - x . x . x
    # 7 - x x . . x
    PERMUTATIONS = {
        2: 1,
        3: 2,
        4: 4,
        5: 7,
    }
    return PERMUTATIONS[len(subsection)]


def find_subsections(chain):
    start = None
    for idx, (a, b) in enumerate(get_joltage_pairs(chain)):
        if b - a < 3:
            if start is None:
                start = idx
        else:
            if start is not None:
                yield chain[start : idx + 1]
            start = None


def run():
    inputlines = util.get_input_lines("10.txt")
    joltages = get_joltages(inputlines)

    # Add in the special cased joltage values at either end, then sort to get
    # the adapter chain.
    joltages.append(0)
    joltages.append(max(joltages) + 3)
    chain = sorted(joltages)

    diffs = count_differences(chain)

    # The maximum allowed joltage difference between adjacent adapters is 3
    # jolts, so adapters differing from either of its neighbours by this amount
    # cannot be removed. The full chain can therefore be split at these points
    # to form distinct sub-sections from which adapters _can_ be removed. The
    # total number of permutations for the whole chain is then the product of
    # the number of permutations for each such sub-section.
    perms = util.product(count_permutations(s) for s in find_subsections(chain))

    return diffs[1] * diffs[3], perms
