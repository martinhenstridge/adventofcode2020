from . import util


def get_foods(lines):
    for line in lines:
        ingredients, allergens = line[:-1].split(" (contains ")
        yield ingredients.split(" "), allergens.split(", ")


def run():
    inputlines = util.get_input_lines("21.txt")
    foods = [f for f in get_foods(inputlines)]
    return ()
