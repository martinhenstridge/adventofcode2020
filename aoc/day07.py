from . import util


def get_baginfo(lines):
    baginfo = {}

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

        baginfo[bag] = {}
        while rest:
            if rest[0] == "no":
                # info ~ [no other bags.]
                info, rest = rest[:3], rest[3:]
            else:
                # info ~ [2 posh black bags,]
                info, rest = rest[:4], rest[4:]
                child = " ".join(info[1:3])
                baginfo[bag][child] = int(info[0])

    return baginfo


CACHE1 = {}
CACHE2 = {}


def can_contain(bag, baginfo, target):
    if bag not in CACHE1:
        CACHE1[bag] = target in baginfo[bag] or any(
            can_contain(child, baginfo, target) for child in baginfo[bag]
        )
    return CACHE1[bag]


def contains(baginfo, bag):
    if bag not in CACHE2:
        CACHE2[bag] = sum(count * (1 + contains(baginfo, child)) for child, count in baginfo[bag].items())
    return CACHE2[bag]


def run():
    inputlines = util.get_input_lines("07.txt")
    baginfo = get_baginfo(inputlines)

    capable = [bag for bag in baginfo if can_contain(bag, baginfo, "shiny gold")]
    inside = contains(baginfo, "shiny gold")

    return len(capable), inside
