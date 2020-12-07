import operator
from os.path import abspath, dirname, join
from functools import reduce, wraps


_ROOT = dirname(dirname(abspath(__file__)))


def get_input_lines(name):
    path = join(_ROOT, "inputs", name)
    with open(path) as f:
        return f.read().splitlines()


def product(numbers):
    return reduce(operator.mul, numbers, 1)


def memoize(fn):
    cache = {}
    @wraps(fn)
    def wrapped(key, *args):
        if key not in cache:
            cache[key] = fn(key, *args)
        return cache[key]
    return wrapped
