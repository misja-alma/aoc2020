import re


def apply_mask(val: int, mask: (int, int)) -> int:
    (dont_care, override) = mask
    return (val & dont_care) | override


def single_bits(x: int) -> [int]:
    result = []
    shifted_x = x
    shift = 0
    while shifted_x != 0:
        if shifted_x & 1 == 1:
            result.append(1 << shift)
        shift += 1
        shifted_x >>= 1

    return result


def apply_mask2(addr: int, mask: (int, int)) -> [int]:
    (floatings, override) = mask
    overridden_addr = addr | override
    addresses = [overridden_addr]

    for bit in single_bits(floatings):
        new_addresses = []
        for address in addresses:
            new_addresses.append(address | bit)
            new_addresses.append(address & ~ bit)
        addresses = new_addresses

    return addresses


def parse_mask(mask: str) -> (int, int):
    dont_care = 0
    override = 0
    for c in mask:
        dont_care *= 2
        override *= 2
        if c == 'X':
            dont_care += 1
        elif c == '1':
            override += 1
    return dont_care, override


class Mask:
    def __init__(self, mask):
        self.mask = parse_mask(mask)

    def execute(self, mem, _):
        return mem, self.mask

    def execute2(self, mem, _):
        return mem, self.mask


class Assign:
    def __init__(self, addr, val):
        self.addr = addr
        self.val = val

    def execute(self, mem, mask):
        mem[self.addr] = apply_mask(self.val, mask)
        return mem, mask

    def execute2(self, mem, mask):
        for addr in apply_mask2(self.addr, mask):
            mem[addr] = self.val
        return mem, mask


command_patterns = [
    (re.compile(r"mask = (?P<mask>[01X]+)"), lambda match: Mask(match.group('mask'))),
    (re.compile(r"mem\[(?P<addr>\d+)\] = (?P<val>\d+)"), lambda match: Assign(int(match.group('addr')), int(match.group('val')))),
]


def parse_command(s: str):
    for pattern_gen in command_patterns:
        (pattern, generator) = pattern_gen
        match = pattern.match(s)
        if match is not None:
            return generator(match)


def run_program(cmds, mem, mask):
    for command in cmds:
        (mem, mask) = command.execute(mem, mask)
    return mem, mask


def run_program2(cmds, mem, mask):
    for command in cmds:
        (mem, mask) = command.execute2(mem, mask)
    return mem, mask


if __name__ == '__main__':
    inputs = open('input_day14.txt', 'r')
    lines = inputs.readlines()
    inputs.close()

    commands = list(map(parse_command, filter(lambda line: len(line) > 1, lines)))

    mem = {}
    mask = []
    (mem, mask) = run_program(commands, mem, mask)

    sum = 0
    for (adr, val) in mem.items():
        sum += val

    print('Part 1: {}'.format(sum))

    mem = {}
    mask = []
    (mem, mask) = run_program2(commands, mem, mask)

    sum = 0
    for (adr, val) in mem.items():
        sum += val

    print('Part 2: {}'.format(sum))




