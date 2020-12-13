import math
from . import util


def get_bus_data(lines):
    timestamp = int(lines[0])
    buses = {}
    for idx, bus in enumerate(lines[1].split(",")):
        if bus != "x":
            buses[int(bus)] = idx
    return timestamp, buses


def find_earliest_after(timestamp, buses):
    best = 0, math.inf
    for bus in buses:
        earliest = bus * math.ceil(timestamp / bus)
        if earliest < best[1]:
            best = bus, earliest
    return best


def run():
    inputlines = util.get_input_lines("13.txt")
    timestamp, buses = get_bus_data(inputlines)

    bus, departs = find_earliest_after(timestamp, buses)

    return (bus * (departs - timestamp),)
