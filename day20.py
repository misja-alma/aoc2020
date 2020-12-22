from queue import *
from copy import deepcopy


def rotate_left(target: [str]) -> [str]:
    new_width = len(target)
    new_height = len(target[0])
    result = [['.' for x in range(new_width)] for y in range(new_height)]
    for r in range(0, len(target)):
        row = target[r]
        for c in range(0, len(row)):
            result[new_height - c - 1][r] = row[c]

    result_strings = []
    for row in result:
        result_strings.append(''.join(row))
    return result_strings


def flip(target: [str]) -> [str]:
    result = []
    for r in reversed(target):
        result.append(r)
    return result


def rotated_and_flipped(rotations: int, flipped: bool, target: [str]) -> [str]:
    for i in range(0, rotations):
        target = rotate_left(target)
    if flipped:
        return flip(target)
    else:
        return target


def grid_to_string(grid: [str]) -> str:
    return '\n'.join(list(map(str, grid)))


class Tile:
    # neighbours indexed: up = 0, right = 1, down = 2, left = 3

    def __init__(self, id_nr, grid):
        self.id_nr = id_nr
        self.grid = grid
        self.neighbours = [None, None, None, None]
        self.init_cols()

    def init_cols(self):
        left_col = []
        right_col = []
        for row in range(0, len(self.grid)):
            width = len(self.grid[row])
            left_col.append(self.grid[row][0])
            right_col.append(self.grid[row][width - 1])
        self.left_col = ''.join(left_col)
        self.right_col = ''.join(right_col)

        self.up_col = self.grid[0]
        height = len(self.grid)
        self.down_col = self.grid[height - 1]


    def non_empty_neighbours(self) -> ['Tile']:
        return list(filter(lambda tile: tile is not None, self.neighbours))

    def left_tile(self) -> 'Tile':
        return self.neighbours[3]

    def right_tile(self) -> 'Tile':
        return self.neighbours[1]

    def down_tile(self) -> 'Tile':
        return self.neighbours[2]

    def up_tile(self) -> 'Tile':
        return self.neighbours[0]

    def set_left_tile(self, tile):
        self.neighbours[3] = tile

    def set_right_tile(self, tile):
        self.neighbours[1] = tile

    def set_down_tile(self, tile):
        self.neighbours[2] = tile

    def set_up_tile(self, tile):
        self.neighbours[0] = tile

    def rotate_left(self):
        self.grid = rotate_left(self.grid)
        self.init_cols()
        first_nb = self.neighbours[0]
        self.neighbours = self.neighbours[1:]
        self.neighbours.append(first_nb)

    def flip(self):
        self.grid = flip(self.grid)
        self.init_cols()
        old_up = self.neighbours[0]
        self.neighbours[0] = self.neighbours[2]
        self.neighbours[2] = old_up

    def __str__(self):
        return '\n'.join([grid_to_string(self.grid),
        'left col:',
        str(self.left_col),
        'right col:',
        str(self.right_col),
        'up col:',
        str(self.up_col),
        'down col:',
        str(self.down_col)])


def parse_tile(block: str) -> Tile:
    lines = list(filter(lambda line: len(line) > 1, block.split('\n')))
    id_nr = int(lines[0][5:len(lines[0])-1])
    grid = lines[1:]
    return Tile(id_nr, grid)


def find_match(tiles: [Tile], position: int, tile: Tile) -> Tile:
    # top = 0, right = 1, down = 2, left = 3. reversed = True
    for tl in tiles:
        if tl.id_nr != tile.id_nr:
            match = match_tile(position, tile, tl)
            if match is not None:
                return match

    return None


# Just rotate tl and flip it until there is a match at the opposite side.
# The returned Tile, if not None, is already flipped and rotated to place
# Notices that this method modifies tl
def match_tile(position: int, match_this: Tile, tl: Tile) -> Tile:
    # rotate object to top
    rotated_copy = deepcopy(match_this)
    source_rotations = 0
    while position > 0:
        rotated_copy.rotate_left()
        position -= 1
        source_rotations += 1

    rotated = 0
    while rotated < 4 and tl.down_col != rotated_copy.up_col:
        tl.rotate_left()
        rotated += 1

    if rotated < 4:
        rotate_left_times(tl, 4 - source_rotations)
        return tl

    tl.flip()

    rotated = 0
    while rotated < 4 and tl.down_col != rotated_copy.up_col:
        tl.rotate_left()
        rotated += 1

    if rotated < 4:
        rotate_left_times(tl, 4 - source_rotations)
        return tl

    tl.flip()
    return None


def rotate_left_times(target: Tile, times: int):
    for i in range(0, times):
        target.rotate_left()


def find_matches(grid: [str], monster: [str]) -> int:
    def match_at(r, c):
        for mr in range(0, len(monster)):
            g_row = grid[r + mr]
            m_row = monster[mr]
            for mc in range(0, len(m_row)):
                if m_row[mc] == '#' and g_row[c + mc] != '#':
                    return False

        return True

    matches = 0
    monster_width = len(monster[0])
    monster_height = len(monster)
    # assumes that there can be overlapping monsters
    for row in range(0, len(grid) - monster_height):
        grid_row = grid[row]
        for col in range(0, len(grid_row) - monster_width):
            if match_at(row, col):
                matches += 1

    return matches


def find_nr_matches(final_grid, sea_monster) -> int:
    for rotations in range(0,4):
        for flip in [False, True]:
            translated_monster = rotated_and_flipped(rotations, flip, sea_monster)
            nr_matches = find_matches(final_grid, translated_monster)
            if nr_matches > 0:
                return nr_matches

    return 0


if __name__ == '__main__':
    inputs = open('input_day20.txt', 'r')
    blocks = inputs.read().split('\n\n')
    inputs.close()

    tiles_by_id = {}
    for block in blocks:
        if len(block) > 1:
            tile = parse_tile(block)
            tiles_by_id[tile.id_nr] = tile

    tiles = list(tiles_by_id.values())

    # Start with some tile, then just follow all its neighbours. Flip/rotate each of them when they come
    # This can be done with BFS. Keep track of visited tiles, put new (rotated + flipped) neighbours in a queue
    # run until queue is empty

    some_tile = tiles[0]
    used_ids = set()
    candidates = SimpleQueue()
    candidates.put_nowait(some_tile)
    used_ids.add(some_tile.id_nr)

    while not candidates.empty():
        candidate = candidates.get_nowait()
        # get all neighbours which are not used yet
        # flip/rotate them, add them to grid and to used, candidates

        print('-------- Candidate: -------')
        print(candidate)
        tl = find_match(tiles, 3, candidate)
        if tl is not None:
            candidate.set_left_tile(tl)
            tl.set_right_tile(candidate)

            if tl.id_nr not in used_ids:
                used_ids.add(tl.id_nr)
                candidates.put_nowait(tl)

            print('Left neighbour:')
            print(tl)

        tl = find_match(tiles, 0, candidate)
        if tl is not None:
            candidate.set_up_tile(tl)
            tl.set_down_tile(candidate)

            if tl.id_nr not in used_ids:
                used_ids.add(tl.id_nr)
                candidates.put_nowait(tl)

            print('Top neighbour:')
            print(tl)

        tl = find_match(tiles, 1, candidate)
        if tl is not None:
            candidate.set_right_tile(tl)
            tl.set_left_tile(candidate)

            if tl.id_nr not in used_ids:
                used_ids.add(tl.id_nr)
                candidates.put_nowait(tl)

            print('Right neighbour:')
            print(tl)

        tl = find_match(tiles, 2, candidate)
        if tl is not None:
            candidate.set_down_tile(tl)
            tl.set_up_tile(candidate)

            if tl.id_nr not in used_ids:
                used_ids.add(tl.id_nr)
                candidates.put_nowait(tl)

            print('Bottom neighbour:')
            print(tl)

    corners = []
    for tile in tiles:
        if len(tile.non_empty_neighbours()) == 2:
            corners.append(tile)

    product = 1
    for corner in corners:
        product *= corner.id_nr

    print('Part 1: {}'.format(product))

    for tile in corners:
        if tile.left_tile() is None and tile.up_tile() is None:
            top_left = tile
            break

    finished = False
    final_tiles = []

    while not finished:
        left_tile = top_left
        tile_row = [left_tile.grid]

        while left_tile.right_tile() is not None:
            neighbour = left_tile.right_tile()
            tile_row.append(neighbour.grid)
            left_tile = neighbour

        final_tiles.append(tile_row)

        if top_left.down_tile() is None:
            finished = True
        else:
            neighbour = top_left.down_tile()
            top_left = neighbour

    # flatten final_tiles
    some_tile = final_tiles[0][0]
    tile_width = len(some_tile[0]) - 2
    tile_height = len(some_tile) - 2
    tiles_width = len(final_tiles[0])
    tiles_height = len(final_tiles)
    final_grid = [['.' for x in range(tile_width * tiles_width)] for y in range(tile_height * tiles_height)]
    for x in range(0, tiles_width):
        for y in range(0, tiles_height):
            tile = final_tiles[y][x]
            for tx in range(1, tile_width+1):
                for ty in range(1, tile_height+1):
                    final_grid[tile_height * y + ty - 1][tile_width * x + tx - 1] = tile[ty][tx]

    # then search the grid for matches, rotate while not found, if still not found flip and repeat
    # the result is the nr of '#' in the grid - nr.matches * (nr '#' in sea monster)

    sea_monster = '''
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''.split('\n')[1:]

    nr_matches = find_nr_matches(final_grid, sea_monster)

    def count(char: str, lines: [str]) -> int:
        return sum(map(lambda line: line.count(char), lines))

    result = count('#', final_grid) - nr_matches * count('#', sea_monster)
    print('Part 2: {}'.format(result))



