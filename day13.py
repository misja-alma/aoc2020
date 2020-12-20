from functools import reduce


# check: does this require a >= b ?
def ext_euclidian(a: int, b: int) -> (int, int):
    r0 = a
    r1 = b
    s0 = 1
    s1 = 0
    t0 = 0
    t1 = 1

    while True:
        q = r0 // r1
        r = r0 % r1
        s = s0 - q * s1
        t = t0 - q * t1
        if r == 0:
            return s1, t1
        r0 = r1
        r1 = r
        s0 = s1
        s1 = s
        t0 = t1
        t1 = t


# Solves pair of equation for x, like:
# x = a1 (mod n1)
# x = a2 (mod n2)
# n1 and n2 need to be co-prime!
# returns (x, n1*n2)
def solve_chinese_remainder(n1: int, a1: int, n2: int, a2: int) -> (int, int):
    (m1, m2) = ext_euclidian(n1, n2)
    solution = a1 * m2 * n2 + a2 * m1 * n1
    return solution % (n1 * n2), n1 * n2


if __name__ == '__main__':
    inputs = open('input_day13.txt', 'r')
    lines = inputs.readlines()
    inputs.close()

    timestamp = int(lines[0])
    schedule = lines[1].split(',')
    intervals = map(int, filter(lambda x: x.strip().isnumeric(), schedule))

    time_diffs = map(lambda x: (x, x - timestamp % x), intervals)

    (min_id, min_diff) = min(time_diffs, key=lambda td: td[1])

    print('Part 1: {}'.format(min_id * min_diff))

    # parse schedule again, this time store both divider and mod - index
    index_modulos = []
    for i in range(0, len(schedule)):
        x = schedule[i].strip()
        if x.isnumeric():
            modu = int(x)
            index_modulos.append((modu - i % modu, modu))

    # Reduce a,b -> Extended Euclidian Algorithm

    def solve_for_2(indmod1: int, indmod2: int) -> (int, int):
        (index1, modulo1) = indmod1
        (index2, modulo2) = indmod2
        return solve_chinese_remainder(modulo1, index1, modulo2, index2)

    (final_index, final_modulo) = reduce(solve_for_2, index_modulos)

    print('Part 2: {}'.format(final_index))