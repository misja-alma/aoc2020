class Boundaries4d:
    def __init__(self, min_x, min_y, min_z, min_p, max_x, max_y, max_z, max_p):
        self.min_x = min_x
        self.min_y = min_y
        self.min_z = min_z
        self.min_p = min_p
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z
        self.max_p = max_p


def count_neighbours4d(x: int, y: int, z: int, p: int, active_points: set) -> int:
    count = 0
    for x2 in range(x-1, x+2):
        for y2 in range(y-1, y+2):
            for z2 in range(z-1, z+2):
                for p2 in range(p - 1, p + 2):
                    if x2 != x or y2 != y or z2 != z or p2 != p:
                        if (x2,y2,z2,p2) in active_points:
                            count += 1
    return count


def generation_generator4d(active_points: set, boundaries: Boundaries4d):
    while len(active_points) > 0:  # or maybe better, continue until active_points doesn't change anymore
        new_active_points = set()
        min_x = 1000000000
        min_y = 1000000000
        min_z = 1000000000
        min_p = 1000000000
        max_x = -1000000000
        max_y = -1000000000
        max_z = -1000000000
        max_p = -1000000000
        for x in range(boundaries.min_x - 1, boundaries.max_x + 2):
            for y in range(boundaries.min_y - 1, boundaries.max_y + 2):
                for z in range(boundaries.min_z - 1, boundaries.max_z + 2):
                    for p in range(boundaries.min_p - 1, boundaries.max_p + 2):
                        nbs = count_neighbours4d(x,y,z,p,active_points)
                        if (x,y,z,p) in active_points:
                            active = 2 <= nbs <= 3
                        else:
                            active = nbs == 3
                        if active:
                            new_active_points.add((x,y,z,p))
                            if x < min_x:
                                min_x = x
                            if y < min_y:
                                min_y = y
                            if z < min_z:
                                min_z = z
                            if p < min_p:
                                min_p = p
                            if x > max_x:
                                max_x = x
                            if y > max_y:
                                max_y = y
                            if z > max_z:
                                max_z = z
                            if p > max_p:
                                max_p = p

        boundaries = Boundaries4d(min_x, min_y, min_z, min_p, max_x, max_y, max_z, max_p)
        active_points = new_active_points
        yield active_points, boundaries

    while True:  # Steady state
        yield active_points, boundaries


def get_generation4d(active_points: set, boundaries: Boundaries4d, generation: int) -> [[str]]:
    for i, v in enumerate(generation_generator4d(active_points, boundaries)):
        if i >= generation - 1:
            return v


class Boundaries:
    def __init__(self, min_x, min_y, min_z, max_x, max_y, max_z):
        self.min_x = min_x
        self.min_y = min_y
        self.min_z = min_z
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z


def count_neighbours(x: int, y: int, z: int, active_points: set) -> int:
    count = 0
    for x2 in range(x-1, x+2):
        for y2 in range(y-1, y+2):
            for z2 in range(z-1, z+2):
                if x2 != x or y2 != y or z2 != z:
                    if (x2,y2,z2) in active_points:
                        count += 1
    return count


def generation_generator(active_points: set, boundaries: Boundaries):
    while len(active_points) > 0:  # or maybe better, continue until active_points doesn't change anymore
        new_active_points = set()
        min_x = 1000000000
        min_y = 1000000000
        min_z = 1000000000
        max_x = -1000000000
        max_y = -1000000000
        max_z = -1000000000
        for x in range(boundaries.min_x - 1, boundaries.max_x + 2):
            for y in range(boundaries.min_y - 1, boundaries.max_y + 2):
                for z in range(boundaries.min_z - 1, boundaries.max_z + 2):
                    nbs = count_neighbours(x,y,z,active_points)
                    if (x,y,z) in active_points:
                        active = 2 <= nbs <= 3
                    else:
                        active = nbs == 3
                    if active:
                        new_active_points.add((x,y,z))
                        if x < min_x:
                            min_x = x
                        if y < min_y:
                            min_y = y
                        if z < min_z:
                            min_z = z
                        if x > max_x:
                            max_x = x
                        if y > max_y:
                            max_y = y
                        if z > max_z:
                            max_z = z

        boundaries = Boundaries(min_x, min_y, min_z, max_x, max_y, max_z)
        active_points = new_active_points
        yield active_points, boundaries

    while True:  # Steady state
        yield active_points, boundaries


def get_generation(active_points: set, boundaries: Boundaries, generation: int) -> [[str]]:
    for i, v in enumerate(generation_generator(active_points, boundaries)):
        if i >= generation - 1:
            return v


if __name__ == '__main__':
    inputs = open('input_day17.txt', 'r')
    lines = inputs.readlines()
    inputs.close()

    # have set of active points (3d) plus active boundaries:
    # smallest/largest coordinate of each dimension of an active point
    # for each next dimension, a cube of 1 layer around those dimension should be searched and every time
    # the active set should be queries for neighbours.
    # counting the active points then becomes trivial
    active_points = set()
    min_x = 1000000000
    min_y = 1000000000
    min_z = 0
    max_x = -1
    max_y = -1
    max_z = 0
    z = 0
    for x in range(0, len(lines)):
        line = lines[x]
        for y in range(0, len(line)):
            if line[y] == '#':
                active_points.add((x,y,z))
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y

    result_world = get_generation(active_points, Boundaries(min_x, min_y, min_z, max_x, max_y, max_z), 6)
    result = len(result_world[0])
    print('Part 1: {}'.format(result))

    active_points4d = set()
    for (x,y,z) in active_points:
        active_points4d.add((x,y,z,0))
    result_world = get_generation4d(active_points4d, Boundaries4d(min_x, min_y, min_z, 0, max_x, max_y, max_z, 0), 6)
    result = len(result_world[0])
    print('Part 1: {}'.format(result))
