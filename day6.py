def group_to_chars(group):
    chars = set(group)
    chars.discard('\n')
    return chars


def group_to_shared_chars(group):
    members = group.split("\n")
    chars_per_member = list(filter(lambda s: len(s) > 0, map(group_to_chars, members)))
    return set.intersection(*chars_per_member)


if __name__ == '__main__':
    inputs = open('input_day6.txt', 'r')
    groups = inputs.read().split("\n\n")
    inputs.close()

    chars_per_group = map(group_to_chars, groups)
    len_per_group = map(len, chars_per_group)
    print("Part 1: {}".format(sum(list(len_per_group))))

    shared_chars_per_group = map(group_to_shared_chars, groups)
    len_per_group = map(len, shared_chars_per_group)
    print("Part 2: {}".format(sum(list(len_per_group))))





