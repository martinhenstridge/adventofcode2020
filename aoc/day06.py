from . import util


def get_groups(lines):
    members = []
    for line in lines:
        if line:
            members.append(line)
        else:
            yield members
            members = []
    yield members


def count_1(group):
    answers = {answer for member in group for answer in member}
    return len(answers)


def count_2(group):
    answers = set("abcdefghijklmnopqrstuvwxyz")
    for member in group:
        answers.intersection_update(member)
    return len(answers)


def run():
    inputlines = util.get_input_lines("06.txt")
    groups = [group for group in get_groups(inputlines)]

    countsum_1 = sum(count_1(group) for group in groups)
    countsum_2 = sum(count_2(group) for group in groups)

    return countsum_1, countsum_2
