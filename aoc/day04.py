import re
from . import util


def get_entries(lines):
    parts = []
    for line in lines:
        if line:
            parts.append(line)
        else:
            yield " ".join(parts)
            parts = []
    yield " ".join(parts)


def into_passport(entry):
    passport = {}
    for part in entry.split():
        key, val = part.split(":", maxsplit=1)
        passport[key] = val.strip()
    return passport


def is_valid_byr(val):
    # four digits; at least 1920 and at most 2002.
    if re.fullmatch(r"[0-9]{4}", val) is None:
        return False
    return 1920 <= int(val) <= 2002


def is_valid_iyr(val):
    # four digits; at least 2010 and at most 2020.
    if re.fullmatch(r"[0-9]{4}", val) is None:
        return False
    return 2010 <= int(val) <= 2020


def is_valid_eyr(val):
    # four digits; at least 2020 and at most 2030.
    if re.fullmatch(r"[0-9]{4}", val) is None:
        return False
    return 2020 <= int(val) <= 2030


def is_valid_hgt(val):
    # a number followed by either cm or in:
    # - If cm, the number must be at least 150 and at most 193.
    # - If in, the number must be at least 59 and at most 76.
    match = re.fullmatch(r"([0-9]+)(cm|in)", val)
    if match is None:
        return False
    if match[2] == "cm":
        return 150 <= int(match[1]) <= 193
    if match[2] == "in":
        return 59 <= int(match[1]) <= 76
    return False


def is_valid_hcl(val):
    # a # followed by exactly six characters 0-9 or a-f.
    return re.fullmatch(r"\#[0-9a-f]{6}", val) is not None


def is_valid_ecl(val):
    # exactly one of: amb blu brn gry grn hzl oth.
    return re.fullmatch(r"(amb|blu|brn|gry|grn|hzl|oth)", val) is not None


def is_valid_pid(val):
    # a nine-digit number, including leading zeroes.
    return re.fullmatch(r"[0-9]{9}", val) is not None


FIELDS = {
    "byr": is_valid_byr,
    "iyr": is_valid_iyr,
    "eyr": is_valid_eyr,
    "hgt": is_valid_hgt,
    "hcl": is_valid_hcl,
    "ecl": is_valid_ecl,
    "pid": is_valid_pid,
}


def is_valid_1(passport):
    return all(f in passport for f in FIELDS)


def is_valid_2(passport):
    return all(f in passport and valid(passport[f]) for f, valid in FIELDS.items())


def run():
    inputlines = util.get_input_lines("04.txt")
    passports = [into_passport(e) for e in get_entries(inputlines)]

    count = sum(1 for p in passports if is_valid_1(p))
    print(count)

    count = sum(1 for p in passports if is_valid_2(p))
    print(count)
