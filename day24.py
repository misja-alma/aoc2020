from utils import *


def neighbours(xy: (int, int)) -> set:
    x, y = xy
    result = [(x-1, y-1), (x+1, y-1), (x-2,y), (x+2, y), (x-1, y+1), (x+1, y+1), xy]
    return set(result)


def count_black_neighbours(xy: (int, int), universe: set) -> int:
    nbrs = neighbours(xy)
    result = 0
    for n in nbrs:
        if n != xy and n in universe:
            result += 1
    return result


if __name__ == '__main__':
    inputs = open('input_day24.txt', 'r')
    lines = inputs.read()
    inputs.close()

    # grid overlaps in x direction;
    # e = x - 2, w = x + 2, ne = x - 1, y - 1, nw = x + 1, y - 1,
    # s = y + 1, n = y - 1
    directions = non_empty_lines(lines)

    black_coords = set()
    for direction in directions:
        # parse direction, get final coord
        # flip (check if known first, if not know flip goes to black)
        index = 0
        first_char = None
        x = 0
        y = 0
        while index < len(direction):
            char = direction[index]
            if first_char is None:
                if char == 'e':
                    x += 2
                elif char == 'w':
                    x -= 2
                else:
                    first_char = char
            else:
                direct = first_char + char
                if direct == 'se':
                    x += 1
                    y += 1
                elif direct == 'sw':
                    x -= 1
                    y += 1
                elif direct == 'ne':
                    x += 1
                    y -= 1
                elif direct == 'nw':
                    x -= 1
                    y -= 1
                else:
                    raise Exception('Unknown direction: ' + direct)
                first_char = None

            index += 1

        if (x,y) in black_coords:
            black_coords.remove((x,y))
        else:
            black_coords.add((x, y))

    print('Part 1: {}'.format(len(black_coords)))

    # algo:
    # take all black tiles in current generation
    # for them and their neighbours:
    # check if already checked. If not: add transformed to new generation
    nr_generations = 0
    current_generation = black_coords.copy()
    while nr_generations < 100:
        checked = set()
        new_generation = set()
        for pt in current_generation:
            cells_to_check = filter(lambda c: c not in checked, neighbours(pt))
            for cell in cells_to_check:
                nr_neighbours = count_black_neighbours(cell, current_generation)
                if cell in current_generation:  # cell is black
                    if 0 < nr_neighbours <= 2:
                        new_generation.add(cell)
                else:
                    if nr_neighbours == 2:
                        new_generation.add(cell)
                checked.add(cell)
        nr_generations += 1
        current_generation = new_generation

    print('Part 2: {}'.format(len(current_generation)))