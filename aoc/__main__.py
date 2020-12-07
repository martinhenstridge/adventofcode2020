import sys
from . import DAYS


def run(solvers, day):
    print()
    parts = solvers[day].run()
    for idx, part in enumerate(parts):
        print(f"[{day}|{idx+1}] {part}")


if len(sys.argv) > 1:
    run(DAYS, sys.argv[1])
else:
    for day in DAYS:
        run(DAYS, day)
