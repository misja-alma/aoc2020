def generate_pairs(nrs_to_check):
    result = set()
    for i1 in range(0, len(nrs_to_check) - 1):
        nr1 = nrs_to_check[i1]
        for i2 in range(i1 + 1, len(nrs_to_check)):
            nr2 = nrs_to_check[i2]
            if nr1 != nr2:
                result.add(nr1 + nr2)
    return result


def find_non_pair(ns):
    for i in range(25, len(ns)):
        preamble = nrs[i-25:i]
        nr = ns[i]
        pairs = generate_pairs(preamble)
        if nr not in pairs:
            return nr
    return -1


def find_sum_range(ns, sm):
    ranges = []
    for nr in ns:
        # add i to all running ranges, check sum of each
        for i in range(0, len(ranges)):
            (smallest, highest, running_sum) = ranges[i]
            if running_sum + nr == sm:
                return smallest if smallest < nr else nr, highest if highest > nr else nr
            ranges[i] = (smallest if smallest < nr else nr,
                         highest if highest > nr else nr,
                         running_sum + nr)
        # add new range starting with i
        ranges.append((nr, nr, nr))


if __name__ == '__main__':
    inputs = open('input_day9.txt', 'r')
    lines = inputs.readlines()
    inputs.close()

    nrs = list(map(int, filter(lambda line: len(line) > 1, lines)))

    non_pair = find_non_pair(nrs)
    print('Part 1: {}'.format(non_pair))

    sum_range = find_sum_range(nrs, non_pair)
    print('Part 2: {}'.format(sum_range[0] + sum_range[1]))





