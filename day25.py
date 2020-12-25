def loop_size(key: int) -> int:
    # subject nr is 7: mult x by subject nr, divide by 20201227
    # start with 1
    # this is subject^size = key (mod divider)
    nr = 1
    size = 0
    while nr != key:
        nr *= 7
        nr = nr % 20201227
        size += 1
    return size


if __name__ == '__main__':
    inputs = open('input_day25.txt', 'r')
    lines = inputs.readlines()
    inputs.close()

    door_key = int(lines[0])
    card_key = int(lines[1])

    print(str(door_key) + ' ' + str(card_key))

    # determine loop size that leads to both keys
    door_size = loop_size(door_key)
    card_size = loop_size(card_key)

    print("ds: " + str(door_size) + " cs: " + str(card_size))

    solution = 1
    for i in range(0, card_size):
        solution *= door_key
        solution = solution % 20201227

    print("solution for door: " + str(solution))

    solution = 1
    for i in range(0, door_size):
        solution *= card_key
        solution = solution % 20201227

    print("solution for card: " + str(solution))