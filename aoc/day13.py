import math
from . import util


def get_bus_data(lines):
    earliest = int(lines[0])
    schedule = {i: int(t) for i, t in enumerate(lines[1].split(",")) if t != "x"}
    return earliest, schedule


def find_first_bus(schedule, earliest):
    result = 0, math.inf

    for bus in schedule.values():
        departs = bus * math.ceil(earliest / bus)
        if departs < result[1]:
            result = bus, departs

    return result


def find_first_timestamp(schedule):
    # Each offset:bus pair constrains the solution (t) as follows:
    #
    # (t + offset) % bus == 0
    #
    # Take the following as an example:
    #
    # 7,13,x,x,59,x,31,19 => { 0:7, 1:13, 4:59, 6:31, 7:19 }
    #
    # The 0:7 constraint is trivially satisfied by t = 0. Further conforming
    # values then occur at an interval of 7.
    #
    # The 1:13 constraint is satisfied by incrementing t by 7 until we encounter
    # a value such that t+1 is exactly divisible by 13, i.e. (t + 1) % 13 == 0.
    # The first such value is 77. Further conforming values can then be found at
    # an interval of 7 * 13 == 91.
    #
    # Note: all bus times are prime, so we need not consider intermediate values
    # (there are no common divisors).
    #
    # The 4:59 constraint is satisfied by incrementing t (== 77) by 91 until we
    # encounter a value such that (t + 4) % 59 == 0. The first such value is
    # 350. Further values are available at an interval of 7 * 13 * 59 == 5369.
    #
    # Similarly, applying the 6:31 constraint yields a timestamp of 70147, with
    # further values at an interval of 7 * 13 * 59 * 31 == 166439.
    #
    # Finally, applying the 7:19 constraint yields the solution: 1068781.
    timestamp = 0
    interval = 1

    for offset, bus in schedule.items():
        while (timestamp + offset) % bus != 0:
            timestamp += interval
        interval *= bus

    return timestamp


# EXAMPLES = {
#    1068781: {0: 7, 1: 13, 4: 59, 6: 31, 7: 19},
#    3417: {0: 17, 2: 13, 3: 19},
#    754018: {0: 67, 1: 7, 2: 59, 3: 61},
#    779210: {0: 67, 2: 7, 3: 59, 4: 61},
#    1261476: {0: 67, 1: 7, 3: 59, 4: 61},
#    1202161486: {0: 1789, 1: 37, 2: 47, 3: 1889},
# }
# for soln, schedule in EXAMPLES.items():
#    assert find_first_timestamp(schedule) == soln


def run():
    inputlines = util.get_input_lines("13.txt")
    earliest, schedule = get_bus_data(inputlines)

    bus, departs = find_first_bus(schedule, earliest)
    timestamp = find_first_timestamp(schedule)

    return bus * (departs - earliest), timestamp
