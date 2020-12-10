import sys
import time
from . import DAYS


def run(solvers, day):
    start = time.monotonic()
    parts = solvers[day].run()
    end = time.monotonic()

    print()
    for idx, part in enumerate(parts):
        print(f"[{day}/{idx+1}] {part}")
    print(f"{1000 * (end - start):.3f}ms")


if len(sys.argv) > 1:
    run(DAYS, sys.argv[1])
else:
    for day in DAYS:
        run(DAYS, day)
