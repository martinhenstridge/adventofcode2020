import re
from . import util


def get_rules_messages(lines):
    rules = {}
    messages = []

    rule_section = True
    for line in lines:
        if not line:
            rule_section = False
            continue

        if rule_section:
            rnum, rule = line.split(": ", maxsplit=1)
            rules[rnum] = [token.replace("\"", "") for token in rule.split()]
        else:
            messages.append(line)

    return rules, messages


def construct_regex(rules):
    rule0 = rules["0"].copy()

    resolved = False
    while not resolved:
        resolved = True
        for idx, token in enumerate(rule0):
            if token in rules:
                rule = rules[token]
                if "|" in rule:
                    rule = ["(?:"] + rule + [")"]
                rule0[idx:idx+1] = rule
                resolved = False
                break

    return "".join(rule0)


def run():
    inputlines = util.get_input_lines("19.txt")
    rules, messages = get_rules_messages(inputlines)

    regex1 = construct_regex(rules)
    count1 = sum(1 for m in messages if re.fullmatch(regex1, m))

    return (count1,)
