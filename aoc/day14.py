import collections
from enum import Enum
from . import util


# def print_bits(bits):
#    print(f"{bits:0>36b}")


class Instruction(Enum):
    MASK = 0
    MEM = 1


def parse_mask(val):
    # mask = X1011100000X111X01001000001110X00000
    mask = {0: 0, 1: 0}
    for idx, bit in enumerate(reversed(val)):
        if bit == "X":
            continue
        elif bit == "0":
            mask[0] |= 1 << idx
        elif bit == "1":
            mask[1] |= 1 << idx
    return mask


def get_instructions(lines):
    for line in lines:
        key, val = line.split(" = ")
        if key == "mask":
            yield Instruction.MASK, val
        else:
            addr = int(key[4:-1])
            data = int(val)
            yield Instruction.MEM, (addr, data)


def execute1(instructions):
    mask = {}
    mem = collections.defaultdict(int)

    for kind, data in instructions:
        if kind is Instruction.MASK:
            mask = parse_mask(data)
        elif kind is Instruction.MEM:
            addr, val = data
            mem[addr] = val & ~mask[0] | mask[1]
        else:
            assert False

    return mem


def run():
    inputlines = util.get_input_lines("14.txt")
    instructions = [i for i in get_instructions(inputlines)]

    mem1 = execute1(instructions)
    total1 = sum(mem1.values())

    return (total1,)
