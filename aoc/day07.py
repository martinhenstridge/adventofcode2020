from . import util


def get_baginfo(lines):
    baginfo = {}

    for line in lines:
        words = line.split()

        # words ~ ["pale", "cyan", "bags", "contain", ...]
        (adj, col, _, _), words = words[:4], words[4:]
        bag = f"{adj} {col}"

        baginfo[bag] = {}
        while words:
            if words[0] == "no":
                # words ~ ["no", "other", "bags."]
                break
            else:
                # words ~ ["2", "posh", "black", "bags," ...]
                (num, adj, col, _), words = words[:4], words[4:]
                baginfo[bag][f"{adj} {col}"] = int(num)

    return baginfo


@util.memoize
def is_parent(bag, baginfo, target):
    return target in baginfo[bag] or any(
        is_parent(child, baginfo, target) for child in baginfo[bag]
    )


@util.memoize
def count_children(bag, baginfo):
    return sum(
        count * (1 + count_children(child, baginfo))
        for child, count in baginfo[bag].items()
    )


def run():
    inputlines = util.get_input_lines("07.txt")
    baginfo = get_baginfo(inputlines)

    num_parents = sum(1 for bag in baginfo if is_parent(bag, baginfo, "shiny gold"))
    num_children = count_children("shiny gold", baginfo)

    return num_parents, num_children
