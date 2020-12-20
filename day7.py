from parsec import *

if __name__ == '__main__':
    inputs = open('input_day7.txt', 'r')
    lines = inputs.readlines()
    inputs.close()

#  .... bags contain [comma separated bagNrs].
# bagNr = [space] [nr] bag(s)
# the input can be immediately processed to an adjacency list
# the adjency list is a forest, trees can have cycles
# parse each entry but only if not present in shiny gold bag counts yet
# backtrack and count shiny gold bags, for each node update entry in hashmap with count upon returning
# finally go trough all entries and count the one with gold bag counts >= 1
    def parse_lines():
        bag = space() >> regex(r'bag[s]?')
        coloured = regex(r'[a-z]+\s[a-z]+')
        coloured_bag = coloured << bag
        number = regex(r'[0-9]+').parsecmap(int) << space()
        number_bags = (number + coloured_bag) | string('no other bags').result((0, 'none'))
        number_list = endBy(number_bags, string(', ') | string('.'))
        sentence = (coloured_bag << string(' contain ')) + number_list
        return list(map(sentence.parse, lines))

    adj_list = dict(parse_lines())  # [(color, [(nr, color),(nr,color),..]), ..]

    gold_bags_in_bag = {}
    seen_bags = set()

    def gather_contents(bag_with_contents):
        (bag, contents) = bag_with_contents
        if bag not in seen_bags:
            seen_bags.add(bag)
            if bag == 'shiny gold':
                gold_bags = 1
            else:
                gold_bags = 0
                for c in contents:
                    (nr, colour) = c
                    if colour != 'none':
                        c_contents = adj_list[colour]
                        gold_bags = gold_bags + nr * gather_contents((colour, c_contents))
            gold_bags_in_bag[bag] = gold_bags

        return gold_bags_in_bag[bag]


    for bwc in adj_list.items():
        gather_contents(bwc)

    gold_bag_containers = len(list(filter(lambda x: x[1] > 0, gold_bags_in_bag.items())))
    print('Part 1: {}'.format(gold_bag_containers - 1))  # discount the gold bag itself

    bags_in_bag = {}
    seen_bags = set()

    def gather_all_contents(bag_with_contents):
        (bag, contents) = bag_with_contents
        if bag not in seen_bags:
            seen_bags.add(bag)
            all_bags = 0
            for c in contents:
                (nr, colour) = c
                if colour != 'none':
                    c_contents = adj_list[colour]
                    all_bags = all_bags + nr * gather_all_contents((colour, c_contents))
            bags_in_bag[bag] = all_bags + 1

        return bags_in_bag[bag]

    gold_bag_contents = adj_list['shiny gold']
    result = gather_all_contents(('shiny gold', gold_bag_contents))
    print('Part 2: {}'.format(result - 1))  # deduct the gold bag itself






