if __name__ == '__main__':
    inputs = open('input_day10.txt', 'r')
    lines = inputs.readlines()
    inputs.close()

    nrs = list(map(int, filter(lambda line: len(line) > 1, lines)))
    nrs.sort()

    last_nr = 0
    diff_ones = 0
    diff_threes = 0
    for nr in nrs:
        dif = nr - last_nr
        if dif == 1:
            diff_ones += 1
        elif dif == 3:
            diff_threes += 1
        last_nr = nr

    result = diff_ones * (diff_threes + 1)
    print('Part 1: {}'.format(result))

    # walk through list. Keep track of current chains; there can be max 3
    # with the new nr:
    # for each chain; check if the nr < 3 away from it. If so, duplicate the chain with the new nr
    # if the chain is exactly 3 away then just add the nr
    # if the chain is > 3 away then throw it away
    # if multiple chains end at the same nr, merge them and add their counts
    # when the nrs are finished, the count of the chain which ends at the last nr in the list is the answer

    def add_or_put(dct, key, cnt):
        if key in dct:
            existing = dct[key]
            dct[key] = existing + cnt
        else:
            dct[key] = cnt

    counts_by_end = {0: 1}
    for nr in nrs:
        new_chains = {}
        for (end, count) in counts_by_end.items():
            dif = nr - end
            if dif < 3:
                add_or_put(new_chains, nr, count)
                add_or_put(new_chains, end, count)
            elif dif == 3:
                add_or_put(new_chains, nr, count)
        counts_by_end = new_chains

    last_nr = nrs[-1]
    count_at_last_nr = counts_by_end[last_nr]

    print('Part 2: {}'.format(count_at_last_nr))


