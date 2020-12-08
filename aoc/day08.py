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
    visited = set()
    terminate = len(instructions)

    while True:
        if idx == terminate:
            return acc, visited, True
        if idx in visited:
            return acc, visited, False
        visited.add(idx)
        ins, arg = instructions[idx]
        idx, acc = update(idx, acc, ins, arg)


def run():
    inputlines = util.get_input_lines("08.txt")
    instructions = [ins for ins in get_instructions(inputlines)]

    # Run the unmodified instruction list.
    acc1, visited, _ = boot(instructions)

    # The faulty instruction must have been visited during part 1, try modifying
    # each in turn.
    for idx in sorted(visited):
        ins, arg = instructions[idx]

        # Modify the instruction as appropriate, making sure to avoid inserting
        # a jmp +0 instruction.
        if ins == "acc":
            continue
        if ins == "jmp":
            instructions[idx] = ("nop", arg)
        elif ins == "nop" and arg != 0:
            instructions[idx] = ("jmp", arg)

        # Run the modified instruction list, replacing the original instruction
        # when finished.
        acc2, _, term = boot(instructions)
        instructions[idx] = (ins, arg)

        # The instruction list now terminates, we're done.
        if term:
            break

    return (acc1, acc2)
