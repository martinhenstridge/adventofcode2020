import re
from . import util


def get_instructions(lines):
    for line in lines:
        match = re.fullmatch(r"(acc|jmp|nop) ((?:\+|\-)\d+)", line)
        assert match is not None
        yield (match[1], int(match[2]))


def update(idx, acc, ins, arg):
    if ins == "nop":
        return idx + 1, acc
    if ins == "acc":
        return idx + 1, acc + arg
    if ins == "jmp":
        return idx + arg, acc


def boot(instructions):
    idx = 0
    acc = 0
    eof = len(instructions)
    visited = set()

    while idx not in visited and idx != eof:
        visited.add(idx)
        ins, arg = instructions[idx]
        idx, acc = update(idx, acc, ins, arg)
    return acc, visited, idx == eof


def run():
    inputlines = util.get_input_lines("08.txt")
    instructions = [ins for ins in get_instructions(inputlines)]

    acc1, visited, _ = boot(instructions)

    # The faulty instruction must have been visited during part 1 above.
    for idx in sorted(visited):
        ins, arg = instructions[idx]

        if ins == "jmp":
            instructions[idx] = ("nop", arg)
        elif ins == "nop" and arg != 0:
            instructions[idx] = ("jmp", arg)
        else:
            continue
        acc2, _, term = boot(instructions)
        instructions[idx] = (ins, arg)

        if term:
            break

    return (acc1, acc2)
