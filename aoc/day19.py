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
            tokens = [token.replace("\"", "") for token in rule.split()]
            if "|" in tokens:
                tokens = ["(?:"] + tokens + [")"]
            rules[rnum] = tokens
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
                rule0[idx:idx+1] = rules[token]
                resolved = False
                break

    return "".join(rule0)


def run():
    inputlines = util.get_input_lines("19.txt")
    rules, messages = get_rules_messages(inputlines)

    regex1 = construct_regex(rules)
    count1 = sum(1 for m in messages if re.fullmatch(regex1, m))

    # 8: 42 | 42 8
    rules["8"] = ["(?:", "42", ")+"]

    # 11: 42 31 | 42 11 31
    rules["11"] = [
        "(?:",
        "(?:", "(?:", "42", "){1}", "(?:", "31", "){1}", ")", "|",
        "(?:", "(?:", "42", "){2}", "(?:", "31", "){2}", ")", "|",
        "(?:", "(?:", "42", "){3}", "(?:", "31", "){3}", ")", "|",
        "(?:", "(?:", "42", "){4}", "(?:", "31", "){4}", ")", ")",
    ]

    regex2 = construct_regex(rules)
    count2 = sum(1 for m in messages if re.fullmatch(regex2, m))

    return count1, count2
