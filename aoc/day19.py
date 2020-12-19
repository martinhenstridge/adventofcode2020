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


def run():
    inputlines = util.get_input_lines("19.txt")
    rules, messages = get_rules_messages(inputlines)

    rule0 = rules["0"].copy()
    resolved = False

    while not resolved:
        resolved = True
        for idx, token in enumerate(rule0):
            if token in rules:
                if "|" in rules[token]:
                    rule = ["("] + rules[token] + [")"]
                else:
                    rule = rules[token]
                rule0[idx:idx+1] = rule
                resolved = False
                break

    regex = "".join(rule0)
    count = sum(1 for m in messages if re.fullmatch(regex, m))

    return (count,)
