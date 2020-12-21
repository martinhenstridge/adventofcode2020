from . import util


def get_foods(lines):
    for line in lines:
        ingredients, allergens = line[:-1].split(" (contains ")
        yield ingredients.split(" "), allergens.split(", ")


def find_allergen_candidates(foods):
    # If an allergen is listed, the associated ingredient *must* be present in
    # the ingredients list. We can therefore restrict the set of ingredients
    # which may correspond to that allergen to those which appear *every* time
    # the allergen is listed.
    candidates = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen not in candidates:
                candidates[allergen] = set(ingredients)
            else:
                candidates[allergen].intersection_update(ingredients)
    return candidates


def identify_allergens(unknowns):
    knowns = {}

    # When an allergen is left with only one viable ingredient, move it from the
    # set of "unknowns" into the set of "knowns". We can then also discount that
    # ingredient as being a possibility for any other allergen, thus yielding
    # further "known" allergens.
    while unknowns:
        for allergen, options in unknowns.items():
            # The current allergen remains ambiguous, skip to the next one.
            if len(options) > 1:
                continue

            ingredient = options.pop()
            knowns[allergen] = ingredient
            del unknowns[allergen]
            for options in unknowns.values():
                options.discard(ingredient)

            # Break rather than continuing to loop since we've changed the size
            # of the dict being iterated over.
            break

    return knowns


def run():
    inputlines = util.get_input_lines("21.txt")
    foods = [f for f in get_foods(inputlines)]

    candidates = find_allergen_candidates(foods)
    known_allergens = identify_allergens(candidates)

    count = sum(
        1
        for ingredients, _ in foods
        for i in ingredients
        if i not in set(known_allergens.values())
    )
    canonical = ",".join(i for a, i in sorted(known_allergens.items()))

    return count, canonical
