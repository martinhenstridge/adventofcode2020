import collections
from enum import Enum
from . import util


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


def mask_interpreter_v1(mask):
    bitmask = {"0": 0, "1": 0}
    for idx, bit in enumerate(reversed(mask)):
        if bit != "X":
            bitmask[bit] |= 1 << idx

    def interpreter(mem, data):
        addr, val = data
        mem[addr] = val & ~bitmask["0"] | bitmask["1"]

    return interpreter


def mask_interpreter_v2(mask):
    bitmask = 0
    xs = []
    for idx, bit in enumerate(reversed(mask)):
        if bit != "0":
            bitmask |= 1 << idx
        if bit == "X":
            xs.append(1 << idx)

    def interpreter(mem, data):
        addr, val = data
        addrs = [addr | bitmask]
        for x in xs:
            complements = [a & ~x for a in addrs]
            addrs.extend(complements)
        for a in addrs:
            mem[a] = val

    return interpreter


def execute(instructions, mask_interpreter):
    mem = collections.defaultdict(int)
    interpreter = lambda *_: None

    for kind, data in instructions:
        if kind is Instruction.MASK:
            interpreter = mask_interpreter(data)
        elif kind is Instruction.MEM:
            interpreter(mem, data)
        else:
            assert False

    return mem


def run():
    inputlines = util.get_input_lines("14.txt")
    instructions = [i for i in get_instructions(inputlines)]

    mem1 = execute(instructions, mask_interpreter_v1)
    mem2 = execute(instructions, mask_interpreter_v2)

    return (sum(mem1.values()), sum(mem2.values()))
