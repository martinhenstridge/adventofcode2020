import collections
from enum import Enum
from . import util


# def print_bits(bits):
#    print(f"{bits:0>36b}")


class Instruction(Enum):
    MASK = 0
    MEM = 1


def get_instructions(lines):
    for line in lines:
        key, val = line.split(" = ")
        if key == "mask":
            yield Instruction.MASK, val
        else:
            addr = int(key[4:-1])
            data = int(val)
            yield Instruction.MEM, (addr, data)


def mask_interpreter1(mask):
    bitmask0 = 0
    bitmask1 = 0
    for idx, bit in enumerate(reversed(mask)):
        if bit == "X":
            continue
        elif bit == "0":
            bitmask0 |= 1 << idx
        elif bit == "1":
            bitmask1 |= 1 << idx
    bitmask0 = ~bitmask0

    def execfn(mem, data):
        addr, val = data
        mem[addr] = val & bitmask0 | bitmask1
    return execfn


def execute(instructions, mask_interpreter):
    mem = collections.defaultdict(int)
    execfn = None

    for kind, data in instructions:
        if kind is Instruction.MASK:
            execfn = mask_interpreter(data)
        elif kind is Instruction.MEM:
            execfn(mem, data)
        else:
            assert False

    return mem


def run():
    inputlines = util.get_input_lines("14.txt")
    instructions = [i for i in get_instructions(inputlines)]

    mem1 = execute(instructions, mask_interpreter1)
    total1 = sum(mem1.values())

    return (total1,)
