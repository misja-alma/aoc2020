def to_seat_nr(line):
    row_str = line[0:7]
    col_str = line[7:10]

    space = 128
    row_index = 0
    for c in row_str:
        if c == 'B':
            row_index += space // 2
        space = space // 2

    space = 8
    col_index = 0
    for c in col_str:
        if c == 'R':
            col_index += space // 2
        space = space // 2

    return row_index * 8 + col_index


if __name__ == '__main__':
    inputs = open('input_day5.txt', 'r')
    lines = inputs.readlines()
    inputs.close()
    seat_nrs = list(map(to_seat_nr, lines))
    max_nr = max(seat_nrs)
    print("Part 1: {}".format(max_nr))

    all_seat_nrs = set(seat_nrs)
    all_possible_seat_nrs = set(range(0, 8 * 128 - 1))
    missing_nrs = all_possible_seat_nrs - all_seat_nrs  # Note that missing_nrs also contains rows not in the plane
    seat = filter(lambda x: (x - 1) in all_seat_nrs and (x + 1) in all_seat_nrs, missing_nrs)
    print("Part 2: {}".format(list(seat)))





