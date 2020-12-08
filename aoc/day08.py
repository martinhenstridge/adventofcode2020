import re
from . import util


def decode(line):
    match = re.fullmatch(r"(acc|jmp|nop) ((?:\+|\-)\d+)", line)
    assert match is not None
    return (match[1], int(match[2]))


def perform(instruction, argument):
    if instruction == "nop":
        return +1, 0
    if instruction == "acc":
        return +1, argument
    if instruction == "jmp":
        return argument, 0


def run():
    inputlines = util.get_input_lines("08.txt")

    idx = 0
    acc = 0
    visited = set()

    while idx not in visited:
        visited.add(idx)
        ins, arg = decode(inputlines[idx])

        didx, dacc = perform(ins, arg)
        idx += didx
        acc += dacc

    return (acc,)
