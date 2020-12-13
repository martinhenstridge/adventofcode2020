from . import util


def get_bus_data(lines):
    return int(lines[0]), [int(bus) for bus in lines[1].split(",") if bus != "x"]


def find_earliest_after(timestamp, buses):
    earliest = {}
    for bus in buses:
        t = 0
        while t < timestamp:
            t += bus
        earliest[bus] = t

    ranked = sorted(earliest.items(), key=lambda x: x[1])
    return ranked[0]


def run():
    inputlines = util.get_input_lines("13.txt")
    timestamp, buses = get_bus_data(inputlines)

    bus, departs = find_earliest_after(timestamp, buses)

    return (bus * (departs - timestamp),)
