import sys
from . import DAYS


if len(sys.argv) > 1:
    DAYS[sys.argv[1]].run()
else:
    for day, solution in DAYS.items():
        print("\n>>> Day", day)
        solution.run()
