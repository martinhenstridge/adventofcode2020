import math
from . import util


def get_bus_data(lines):
    earliest = int(lines[0])
    schedule = {}
    for idx, time in enumerate(lines[1].split(",")):
        if time != "x":
            schedule[int(time)] = idx
    return earliest, schedule


def first_multiple_at_least(minimum, factor):
    return factor * math.ceil(minimum / factor)


def find_first_bus(schedule, earliest):
    result = 0, math.inf
    for bus in schedule:
        departs = first_multiple_at_least(earliest, bus)
        if departs < result[1]:
            result = bus, departs
    return result


def find_first_timestamp(schedule, lowerbound):
    # [439, 13, 17, 23, 41] are aligned at offset 17
    step = 91488917
    offset = 17

    schedule.pop(13)
    schedule.pop(17)
    schedule.pop(23)
    schedule.pop(41)
    print(schedule)

    t = first_multiple_at_least(lowerbound, step)
    t -= offset

    while True:
        t += step
        for bus, offset in schedule.items():
            if (t + offset) % bus != 0:
                break
        else:
            return t


def run():
    inputlines = util.get_input_lines("13.txt")
    earliest, schedule = get_bus_data(inputlines)

    bus, departs = find_first_bus(schedule, earliest)
    timestamp = find_first_timestamp(schedule, 100000000000000)

    return (bus * (departs - earliest), timestamp)
