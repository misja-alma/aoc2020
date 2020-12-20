import re


class Acc:
    def __init__(self, diff):
        self.diff = diff

    def execute(self, pc, acc):
        return pc + 1, acc + self.diff


class Jmp:
    def __init__(self, diff):
        self.diff = diff

    def execute(self, pc, acc):
        return pc + self.diff, acc


class Nop:
    def __init__(self, diff):
        self.diff = diff

    @staticmethod
    def execute(pc, acc):
        return pc + 1, acc


command_patterns = [
    (re.compile(r"acc (?P<diff>[+|-]\d+)"), lambda match: Acc(int(match.group('diff')))),
    (re.compile(r"jmp (?P<diff>[+|-]\d+)"), lambda match: Jmp(int(match.group('diff')))),
    (re.compile(r"nop (?P<diff>[+|-]\d+)"), lambda match: Nop(int(match.group('diff')))),
]


def parse_command(s: str):
    for pattern_gen in command_patterns:
        (pattern, generator) = pattern_gen
        match = pattern.match(s)
        if match is not None:
            return generator(match)


def run_program(cmds, pc_acc):
    seen_pcs = set()
    (pc, acc) = pc_acc
    while pc < len(cmds) and pc not in seen_pcs:
        seen_pcs.add(pc)
        command = cmds[pc]
        (pc, acc) = command.execute(pc, acc)

    return pc, acc, pc == len(cmds)


def change_command(cmd):
    if isinstance(cmd, Nop):
        return Jmp(cmd.diff)
    if isinstance(cmd, Jmp):
        return Nop(cmd.diff)
    return cmd


if __name__ == '__main__':
    inputs = open('input_day8.txt', 'r')
    lines = inputs.readlines()
    inputs.close()

    commands = list(map(parse_command, filter(lambda line: len(line) > 1, lines)))

    (_, result, _) = run_program(commands, (0, 0))

    print('Part 1: {}'.format(result))

    normal_exit = False
    next_cmd_to_change = 0
    while not normal_exit:
        old_command = commands[next_cmd_to_change]
        new_command = change_command(old_command)
        commands[next_cmd_to_change] = new_command
        (_, result, normal_exit) = run_program(commands, (0, 0))
        commands[next_cmd_to_change] = old_command
        next_cmd_to_change = next_cmd_to_change + 1

    print('Part 2: {}'.format(result))



