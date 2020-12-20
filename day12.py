def rotate_right(dxdy):
    (dx, dy) = dxdy
    s = 1
    c = 0
    xnew = dx * c - dy * s
    ynew = dx * s + dy * c
    return xnew, ynew


class Turn:
    def __init__(self, rotation):
        self.rotation = (rotation // 90) % 4

    def __str__(self):
        return 'Turn ' + str(self.rotation)

    def execute(self, pos, direction):
        new_direction = (direction + self.rotation) % 4
        return pos, new_direction

    def execute2(self, pos, waypoint):
        new_waypoint = waypoint
        for i in range(0, self.rotation):
            new_waypoint = rotate_right(new_waypoint)

        return pos, new_waypoint


class DirectedMove:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def __str__(self):
        return 'dx: ' + str(self.dx) + ', dy: ' + str(self.dy)

    def execute(self, pos, direction):
        return (pos[0] + self.dx, pos[1] + self.dy), direction

    def execute2(self, pos, waypoint):
        return pos, (waypoint[0] + self.dx, waypoint[1] + self.dy)


class UndirectedMove:
    def __init__(self, movement):
        self.movement = movement

    def __str__(self):
        return 'move ' + str(self.movement)

    def execute(self, pos, direction):
        if direction == 0:
            (dx, dy) = (0, -self.movement)
        elif direction == 1:
            (dx, dy) = (self.movement, 0)
        elif direction == 2:
            (dx, dy) = (0, self.movement)
        elif direction == 3:
            (dx, dy) = (-self.movement, 0)
        else:
            raise Exception("Invalid direction: " + str(direction))

        return (pos[0] + dx, pos[1] + dy), direction

    def execute2(self, pos, waypoint):
        return (pos[0] + waypoint[0] * self.movement, pos[1] + waypoint[1] * self.movement), waypoint


def parse_move(line):
    direction = line[0]
    distance = int(line[1:])
    if direction == 'L':
        return Turn(-distance)
    elif direction == 'R':
        return Turn(distance)
    elif direction == 'F':
        return UndirectedMove(distance)
    elif direction == 'N':
        return DirectedMove(0, -distance)
    elif direction == 'E':
        return DirectedMove(distance, 0)
    elif direction == 'S':
        return DirectedMove(0, distance)
    elif direction == 'W':
        return DirectedMove(-distance, 0)
    else:
        raise Exception('Unknown direction: ' + direction)


if __name__ == '__main__':
    inputs = open('input_day12.txt', 'r')
    lines = inputs.readlines()
    inputs.close()

    directions = filter(lambda line: len(line) > 1, lines)
    moves = list(map(parse_move, directions))

    position = (0, 0)
    # N = 0, E = 1, S = 2, W = 3
    dirction = 1
    for move in moves:
        (position, dirction) = move.execute(position, dirction)

    (x, y) = position
    print('Part 1: {}'.format(abs(x) + abs(y)))

    # parsing stays the same, but give moves an extra execute2 method that moves either the waypoint or the ship
    position = (0, 0)
    way_point = (10, -1)

    for move in moves:
        (position, way_point) = move.execute2(position, way_point)

    (x, y) = position
    print('Part 2: {}'.format(abs(x) + abs(y)))

