# read matrix
# function char at pos: gets line with y, modulo x and reads from line

import math


if __name__ == '__main__':
    inputs = open('input_day3.txt', 'r')
    lines = inputs.readlines()
    inputs.close()

    def char_at_pos(x, y):
        line = lines[y]
        line_length = len(line) - 1  # strip LF
        return line[x % line_length]

    def trees_at_slope(dxdy):
        (dx, dy) = dxdy
        (x, y) = (0, 0)
        nr_trees = 0
        while y < len(lines):
            if char_at_pos(x, y) == '#':
                nr_trees += 1
            y += dy
            x += dx
        return nr_trees

    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    trees = map(trees_at_slope, slopes)

    print('Part 2: {}'.format(math.prod(trees)))



