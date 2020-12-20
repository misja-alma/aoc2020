if __name__ == '__main__':
    inputs = open('input_day1.txt', 'r')
    lines = inputs.readlines()
    inputs.close()
    ints = set()
    for line in lines:
        ints.add(int(line))
    print('Read {} numbers'.format(len(ints)))
    # put all in set. Then iterate:
    # for each, check if 2020-val is in set
    # if so, exit with result
    for n in ints:
        if (2020 - n) in ints:
            print('Part 1: ' + str(n * (2020-n)))
            break

    twoSums = {}
    for i1 in range(len(lines)):
        val1 = int(lines[i1])
        for i2 in range(i1 + 1, len(ints)):
            val2 = int(lines[i2])
            twoSums[val1 + val2] = val1 * val2

    for n in ints:
        if (2020 - n) in twoSums:
            others = twoSums[2020-n]
            print('Part 2: ' + str(n * others))
            break
