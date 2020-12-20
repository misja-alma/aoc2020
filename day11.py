def count_occupied_adjacent(mtrx, x, y):
    total = 0

    def count_safe(nx, ny):
        if 0 <= nx < len(mtrx[0]) and 0 <= ny < len(mtrx):
            if mtrx[ny][nx] == '#':
                return 1
            else:
                return 0
        else:
            return 0

    total += count_safe(x - 1, y - 1)
    total += count_safe(x, y - 1)
    total += count_safe(x + 1, y - 1)

    total += count_safe(x - 1, y)
    total += count_safe(x + 1, y)

    total += count_safe(x - 1, y + 1)
    total += count_safe(x, y + 1)
    total += count_safe(x + 1, y + 1)

    return total


def count_occupied_in_sight(mtrx, x, y):
    total = 0

    def count_line(dx, dy):
        nx = x
        ny = y
        finished = False
        while not finished:
            nx += dx
            ny += dy
            if 0 <= nx < len(mtrx[0]) and 0 <= ny < len(mtrx):
                if mtrx[ny][nx] == '#':
                    return 1
                elif mtrx[ny][nx] == 'L':
                    return 0
            else:
                finished = True

        return 0

    total += count_line(-1, -1)
    total += count_line(0, -1)
    total += count_line(+1, -1)

    total += count_line(-1, 0)
    total += count_line(+1, 0)

    total += count_line(-1, +1)
    total += count_line(0, +1)
    total += count_line(+1, +1)

    return total


def next_generation(mtrx, occ_threshold, occ_detector):
    new_mtrx = []
    for y in range(len(mtrx)):
        new_line = []
        for x in range(len(mtrx[y])):
            occ_adjacent = occ_detector(mtrx, x, y)
            if mtrx[y][x] == 'L':
                if occ_adjacent == 0:
                    new_line.append('#')
                else:
                    new_line.append(mtrx[y][x])
            elif mtrx[y][x] == '#':
                if occ_adjacent >= occ_threshold:
                    new_line.append('L')
                else:
                    new_line.append(mtrx[y][x])
            else:
                new_line.append('.')

        new_mtrx.append(new_line)

    return new_mtrx


if __name__ == '__main__':
    inputs = open('input_day11.txt', 'r')
    lines = inputs.readlines()
    inputs.close()

    input_matrix = list(filter(lambda line: len(line) > 1, lines))

    matrix = input_matrix
    known_matrices = set(str(matrix))
    stable = False
    while not stable:
        matrix = next_generation(matrix, 4, count_occupied_adjacent)
        stable = str(matrix) in known_matrices
        known_matrices.add(str(matrix))

    total_occupied = sum(map(lambda line: line.count('#'), matrix))
    print('Part 1: {}'.format(total_occupied))

    matrix = input_matrix
    known_matrices = set(str(matrix))
    stable = False
    while not stable:
        matrix = next_generation(matrix, 5, count_occupied_in_sight)
        stable = str(matrix) in known_matrices
        known_matrices.add(str(matrix))

    total_occupied = sum(map(lambda line: line.count('#'), matrix))
    print('Part 2: {}'.format(total_occupied))



