# read tiles + id's
# store them as a node in a hashmap by its id
# for each tile, for each side, look for other one connecting to it; attach mutual link to from that node
# in the end, to find the corners; just take one node and follow the links all the way up, right etc.

class Tile:

    def __init__(self, id_nr, grid):
        self.id_nr = id_nr
        self.grid = grid

        left_col = []
        right_col = []
        for row in range(0, len(grid)):
            width = len(grid[row])
            left_col.append(grid[row][0])
            right_col.append(grid[row][width - 1])
        self.left_col = ''.join(left_col)
        self.right_col = ''.join(right_col)

        self.up_col = grid[0]
        height = len(grid)
        self.down_col = grid[height - 1]

    def neighbours(self) -> ['Tile']:
        nbs = [self.up_tile, self.down_tile, self.right_tile, self.left_tile]
        return list(filter(lambda tile: tile is not None, nbs))


def parse_tile(block: str) -> Tile:
    lines = list(filter(lambda line: len(line) > 1, block.split('\n')))
    id_nr = int(lines[0][5:len(lines[0])-1])
    grid = lines[1:]
    return Tile(id_nr, grid)


def find_match(tiles: [Tile], col: str) -> (int, bool, Tile):
    # top = 0, right = 1, down = 2, left = 3. reversed = True
    for tl in tiles:
        if tl.id_nr != tile.id_nr:
            match = match_tile(col, tl)
            if match is not None:
                return tl

    return None


def match_tile(col: str, tl: Tile) -> (int, bool):
    if tl.right_col == col:
        tl.right_tile = tile
        return 1, False
    if tl.left_col == col:
        tl.left_tile = tile
        return 3, False
    if tl.up_col == col:
        tl.up_tile = tile
        return 0, False
    if tl.down_col == col:
        tl.down_tile = tile
        return 2, False

    col = col[::-1]
    if tl.right_col == col:
        tl.right_tile = tile
        return 1, True
    if tl.left_col == col:
        tl.left_tile = tile
        return 3, True
    if tl.up_col == col:
        tl.up_tile = tile
        return 0, True
    if tl.down_col == col:
        tl.down_tile = tile
        return 2, True

    return None


def find_left_match(tiles: [Tile], tile: Tile):
    match = find_match(tiles, tile.left_col)
    tile.left_tile = match


def find_right_match(tiles: [Tile], tile: Tile):
    match = find_match(tiles, tile.right_col)
    tile.right_tile = match


def find_up_match(tiles: [Tile], tile: Tile):
    match = find_match(tiles, tile.up_col)
    tile.up_tile = match


def find_down_match(tiles: [Tile], tile: Tile):
    match = find_match(tiles, tile.down_col)
    tile.down_tile = match


def rotate_left(target: [str]) -> [str]:
    new_width = len(target)
    new_height = len(target[0])
    result = [['.' for x in range(new_width)] for y in range(new_height)]
    for r in range(0, len(target)):
        row = target(r)
        for c in range(0, len(row)):
            result[new_height - c - 1][r] = row[c]

    result_strings = []
    for row in result:
        result_strings.append(''.join(row))
    return result_strings


def rotate_left_times(target: [str], times: int) -> [str]:
    for i in range(0, times):
        target = rotate_left(target)
    return target


def flip(target: [str]) -> [str]:
    result = []
    for r in reversed(target):
        result.append(r.copy())
    return result


def rotated_and_flipped(rotations: int, flipped: bool, target: [str]) -> [str]:
    rotated = rotate_left_times(target, rotations)
    if flipped:
        return flip(rotated)
    else:
        return rotated


def find_matches(grid: [str], monster: [str]) -> int:
    return NotImplemented


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

    # matches can be any other column or the column in reverse ..
    # At this point we don't care about flipping or rotating, we just build a linked list
    for tile in tiles:
        find_left_match(tiles, tile)
        find_right_match(tiles, tile)
        find_up_match(tiles, tile)
        find_down_match(tiles, tile)

    corners = []
    for tile in tiles:
        if len(tile.neighbours()) == 2:
            corners.append(tile)

    product = 1
    for corner in corners:
        product *= corner.id_nr

    print('Part 1: {}'.format(product))

    # Build the matrix by starting in a corner and rotating it until it is top left.
    # keep a rotation 0-4 and a flip y/n
    # start walking to right, rotate and flip the neighbour until it connects correctly, adjust rotation, flip etc
    # then from start or row walk 1 down, rotate/flip, repeat
    # while we go, build the final grid
    top_left = corners[0]
    if top_left.left_tile is None and top_left.up_tile is None:
        rotation = 0
    elif top_left.up_tile is None and top_left.right_tile is None:
        rotation = 1
    elif top_left.right_tile is None and top_left.down_tile is None:
        rotation = 2
    else:
        rotation = 3
    flipped = False

    # TODO rotate the top left

    finished = False
    start_rotation = rotation
    start_flipped = flipped
    final_grid = []

    while not finished:
        left_tile = top_left

        while left_tile.right_tile is not None:
            neighbour = left_tile.right_tile
            (rot, fl) = match_tile(left_tile.right_col, neighbour)
            # TODO rotate + flip grid by both rotations etc
            # adjust current rotation
            left_tile = neighbour

        if top_left.down_tile is None:
            finished = True
        else:
            neighbour = top_left.down_tile
            (rot, fl) = match_tile(top_left.down_col, neighbour)
            # TODO rotate + flip grid by both rotations -> start_rotation! etc
            # adjust start rotation, start flipped etc
            top_left = neighbour

    # then search the grid for matches, rotate while not found, if still not found flip and repeat
    # the result is the nr of '#' in the grid - nr.matches * (nr '#' in sea monster)

    sea_monster = '''
                  # \n
#    ##    ##    ###\n
 #  #  #  #  #  #   \n'''.split('\n')

    nr_matches = find_nr_matches(final_grid, sea_monster)

    def count(char: str, lines: [str]) -> int:
        return sum(map(lambda line: line.count(char), lines))

    result = count('#', final_grid) - nr_matches * count('#', sea_monster)
    print('Part 2: {}'.format(result))



