from collections import deque


if __name__ == '__main__':
    inputs = [2, 1, 5, 6, 9, 4, 7, 8, 3]  # 46978532
    # inputs = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    ring = deque()
    for input in inputs:
        ring.append(input)
    next = inputs[0]

    moves = 0

    while moves < 100:  # 100
        print('Move ' + str(moves + 1))
        print('Cups: ' + str(ring))
        print('Current: ' + str(next))
        current_el = ring.index(next)
        # remove 3 els right of current
        ring.rotate(-(current_el + 1))
        removed = []
        for i in range(0, 3):
            el = ring.popleft()
            removed.append(el)
        print('Pick up: ' + str(removed))
        dest = next - 1
        while dest not in ring and dest >= 1:
            dest -= 1
        try:
            dest_index = ring.index(dest)
        except ValueError:
            # find max el
            max_el = max(ring)
            dest_index = ring.index(max_el)
        print('Destination: ' + str(ring[dest_index]))
        # insert removed els after index;
        # rotate index to right, append them afterwards
        ring.rotate(-(dest_index + 1))
        for i in reversed(range(3)):
            el = removed[i]
            ring.appendleft(el)
        # new current: right of current
        current_el = ring.index(next)
        ring.rotate(-(current_el + 1))
        next = ring[0]
        moves += 1

    # rotate ring so that '1' is at te left, the remainder after '1' is the solution
    one_index = ring.index(1)
    ring.rotate(-one_index)
    solution = []
    for el in ring:
        solution.append(el)
    print('Part 1: {}'.format(''.join(map(str, solution[1:]))))

    # initialize array 1 .. 1000000; first are as above, next starts at first free index
    # each one, also the above, has a pointer to the next

    next_by_el = [-1] + inputs  # ring[0] is not used, inputs will be overwritten
    print('----- Part 2, inputs: ' + str(inputs))
    first_input = inputs[0]
    inputs_len = len(inputs)
    first_outside = inputs_len + 1
    for i in range(inputs_len):
        el = inputs[i]
        if i + 1 < inputs_len:
            next_el = inputs[i + 1]
        else:
            next_el = first_outside
        next_by_el[el] = next_el

    for i in range(inputs_len + 1, 1000000 + 1):
        next_by_el.append(i + 1)
    max_index = len(next_by_el) - 1
    next_by_el[max_index] = inputs[0]
    # algo as before but now with indexed linked list

    def pointer_str(pointers: [int]) -> str:
        one_index = pointers[1]
        res = str(one_index)
        index = pointers[one_index]
        while index != one_index:
            res += str(index)
            index = pointers[index]
        return res

    moves = 0
    current_el = inputs[0]
    next = next_by_el[current_el]

    while moves < 10000000:
        # print('Move ' + str(moves + 1))
        # print('Cups: ' + pointer_str(next_by_el))
        # print('Current index: ' + str(current_el))
        # print('Current points at: ' + str(next))
        # remove 3 els right of current
        # so current will point to whatever 3 from current pointed to
        picked_up = []
        picked_up.append(next_by_el[next])
        picked_up.append(next_by_el[picked_up[0]])
        picked_up.append(next_by_el[picked_up[1]])
        next_by_el[current_el] = picked_up[2]
        # print('After cut: ' + pointer_str(next_by_el))

        picked_up_indices = [next, picked_up[0], picked_up[1]]
        # print('Pick up: ' + str(picked_up_indices)) # str(picked_up))
        dest = current_el - 1
        # decrease dest while dest in picked up 3
        # if dest becomes < 1; dest = 100000 and repeat
        if dest == 0:
            dest = max_index
        while dest in picked_up_indices:
            dest -= 1
            if dest == 0:
                dest = max_index

        # print('Destination: ' + str(dest))
        # insert removed els after dest;
        # so [dest] will point to first of removed,
        # last will point to whatever dest was pointing to
        old_dest = next_by_el[dest]
        next_by_el[dest] = next
        next_by_el[picked_up[1]] = old_dest

        # new current: right of current
        moves += 1
        current_el = next_by_el[current_el]
        next = next_by_el[current_el]

    # print('Cups: ' + pointer_str(next_by_el))
    el_after_1 = next_by_el[1]
    el_after_after = next_by_el[el_after_1]
    print('Part 2: {}'.format(el_after_1 * el_after_after)) # 457720818338