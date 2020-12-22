def parse_contents(line: str) -> (set, set):
    # returns (ingredients, allergens)
    contains_index = line.find(' (contains ')
    close_index = line.find(')')
    ingredients = line[:contains_index].split(' ')
    allerg_str = line[contains_index + 11: close_index]
    return set(ingredients), set(allerg_str.split(', '))


if __name__ == '__main__':
    inputs = open('input_day21.txt', 'r')
    lines = inputs.readlines()
    inputs.close()

    # for each allergent:
    # take the intersection of all ingredient in which they are listed, and also the union - intersection (complement?)
    # the allergent is present in one of the allergens in the intersection, but impossibly one of the complement
    contents = list(map(parse_contents, filter(lambda line: len(line) > 1, lines)))

    all_ingredients = set()
    all_allergents = set()

    ingredient_union_by_allergent = {}
    ingredient_intersection_by_allergent = {}

    # for each, calc their allergen union and intersection, and finally their complement
    for (ingredients, allergents) in contents:
        all_ingredients = all_ingredients.union(ingredients)
        all_allergents = all_allergents.union(allergents)

        for allergent in allergents:
            if allergent in ingredient_union_by_allergent:
                ingredient_union = ingredient_union_by_allergent[allergent]
            else:
                ingredient_union = set()
            ingredient_union_by_allergent[allergent] = ingredient_union.union(ingredients)

            if allergent in ingredient_intersection_by_allergent:
                ingredient_intersection = ingredient_intersection_by_allergent[allergent]
                ingredient_intersection_by_allergent[allergent] = ingredient_intersection.intersection(ingredients)
            else:
                ingredient_intersection_by_allergent[allergent] = set(ingredients)

    in_some_allergent = set()
    for (allergent, ingredients) in ingredient_intersection_by_allergent.items():
        in_some_allergent = in_some_allergent.union(ingredients)

    impossible_for_allergens = all_ingredients - in_some_allergent

    count = 0
    for (ingredients, allergens) in contents:
        working_copy = impossible_for_allergens.intersection(ingredients)
        count += len(working_copy)

    print('Part 1: {}'.format(count))

    # take all allergens with 1 item intersection. Remove those ingredients from all other intsersections.
    # Keep track of handled allergens above.
    # Repeat for unhandled allergens until all intersections are 1 item.

    checked_allergens = set()
    keep_going = True
    while keep_going:
        keep_going = False
        for (allergent, ingredients) in ingredient_intersection_by_allergent.items():
            if allergent not in checked_allergens and len(ingredients) == 1:
                checked_allergens.add(allergent)
                remove_this = next(iter(ingredients))
                for (allergent2, ingredients2) in ingredient_intersection_by_allergent.items():
                    if allergent2 != allergent and remove_this in ingredients2:
                        ingredients2.remove(remove_this)
                        keep_going = True

    # now sort ingredients by their allergen, take ingredients, concatenate with comma
    lst = list(ingredient_intersection_by_allergent.items())
    lst.sort(key=lambda x: x[0])
    ingredients = list(map(lambda x: next(iter(x[1])), lst))
    print('Part 2: {}'.format(','.join(ingredients)))
