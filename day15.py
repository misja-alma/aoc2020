from collections.abc import Iterable


def nr_generator(inputs: [int]) -> Iterable:
    last_indices = {}
    for i in range(0, len(inputs)):
        last_indices[inputs[i]] = i
        yield inputs[i]
        i += 1

    i = len(inputs) - 1
    nr = inputs[i]
    while True:
        if nr not in last_indices:
            new_nr = 0
        else:
            last_index = last_indices[nr]
            new_nr = i - last_index
        last_indices[nr] = i
        nr = new_nr
        i += 1
        yield nr


def find_nr_at(inputs: [int], index: int) -> int:
    for i, v in enumerate(nr_generator(inputs)):
        if i == index - 1:
            return v


if __name__ == '__main__':
    inputs = [1, 2, 16, 19, 18, 0]

    print('Part 1: {}'.format(find_nr_at(inputs, 2020)))

    print('Part 2: {}'.format(find_nr_at(inputs, 30000000)))
