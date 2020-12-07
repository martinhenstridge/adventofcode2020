from . import util


def get_bags(lines):
    bags = {}

    for line in lines:
        # words ~ [
        #     pale cyan bags contain
        #     2 posh black bags,
        #     4 wavy gold bags,
        #     2 vibrant brown bags.
        # ]
        words = line.split()

        # head ~ [pale cyan bags contain]
        head, rest = words[:4], words[4:]
        bag = " ".join(head[:2])

        bags[bag] = {}
        while rest:
            if rest[0] == "no":
                # info ~ [no other bags.]
                info, rest = rest[:3], rest[3:]
            else:
                # info ~ [2 posh black bags,]
                info, rest = rest[:4], rest[4:]
                child = " ".join(info[1:3])
                bags[bag][child] = int(info[0])

    return bags


CACHE = {}


def can_contain(bags, candidate, target):
    if candidate not in CACHE:
        CACHE[candidate] = target in bags[candidate] or any(
            can_contain(bags, child, target) for child in bags[candidate]
        )
    return CACHE[candidate]


def run():
    inputlines = util.get_input_lines("07.txt")
    bags = get_bags(inputlines)

    capable = [bag for bag in bags if can_contain(bags, bag, "shiny gold")]

    return len(capable),
