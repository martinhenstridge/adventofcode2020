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
            key, rule = line.split(": ", maxsplit=1)
            tokens = [token.replace('"', "") for token in rule.split()]
            rules[key] = tokens
        else:
            messages.append(line)

    return rules, messages


@util.memoize
def into_regex(key, rules):
    regex = "".join(into_regex(t, rules) if t in rules else t for t in rules[key])
    if "|" in rules[key]:
        regex = "(?:" + regex + ")"
    return regex


def run():
    inputlines = util.get_input_lines("19.txt")
    rules, messages = get_rules_messages(inputlines)

    # Add variant of rule 8: 42 | 42 8
    # This means rule 42 repeated n times, where n >= 1.
    rules["8+"] = ["42", "+"]

    # Add variant of rule 11: 42 31 | 42 11 31
    # This means rule 42 repeated n times followed by rule 31 repeated n times,
    # where n >= 1. Trial and error reveals the maximum number of repetitions to
    # be 4.
    rules["11+"] = []
    for n in range(4):
        rules["11+"] += ["(?:", "42", f"{{{n+1}}}", "31", f"{{{n+1}}}", ")", "|"]
    rules["11+"].pop()

    # Add variant of rule 0, accounting for modified sub-rules.
    rules["0+"] = [f"{t}+" if t in ("8", "11") else t for t in rules["0"]]

    count1 = sum(1 for m in messages if re.fullmatch(into_regex("0", rules), m))
    count2 = sum(1 for m in messages if re.fullmatch(into_regex("0+", rules), m))

    return count1, count2
