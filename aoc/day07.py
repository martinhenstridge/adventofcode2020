from . import util


def get_baginfo(lines):
    baginfo = {}

    for line in lines:
        words = line.split()

        # words ~ ["pale", "cyan", "bags", "contain", ...]
        (adj, col, _, _), words = words[:4], words[4:]

        children = {}
        baginfo[f"{adj} {col}"] = children

        while words:
            if words[0] == "no":
                # words ~ ["no", "other", "bags.", ...]
                words = words[3:]
            else:
                # words ~ ["2", "posh", "black", "bags,"]
                (num, adj, col, _), words = words[:4], words[4:]
                children[f"{adj} {col}"] = int(num)

    return baginfo


@util.memoize
def can_contain(bag, baginfo, target):
    return target in baginfo[bag] or any(
        can_contain(child, baginfo, target) for child in baginfo[bag]
    )


@util.memoize
def contains(bag, baginfo):
    return sum(count * (1 + contains(child, baginfo)) for child, count in baginfo[bag].items())


def run():
    inputlines = util.get_input_lines("07.txt")
    baginfo = get_baginfo(inputlines)

    containers = sum(1 for bag in baginfo if can_contain(bag, baginfo, "shiny gold"))
    contained = contains("shiny gold", baginfo)

    return containers, contained
