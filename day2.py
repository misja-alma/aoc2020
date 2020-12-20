import re


def is_valid_password_1(s: str):
    pattern = re.compile(r"(?P<minChars>\d+)-(?P<maxChars>\d+) (?P<char>\w): (?P<password>.*)")
    match = pattern.match(s)

    min_chars = int(match.group("minChars"))
    max_chars = int(match.group("maxChars"))
    char = match.group("char")
    password = match.group("password")
    char_count = password.count(char)
    return min_chars <= char_count <= max_chars


def is_valid_password_2(s: str):
    pattern = re.compile(r"(?P<pos1>\d+)-(?P<pos2>\d+) (?P<char>\w): (?P<password>.*)")
    match = pattern.match(s)

    pos1 = int(match.group("pos1")) - 1
    pos2 = int(match.group("pos2")) - 1
    char = match.group("char")
    password = match.group("password")
    return (password[pos1] == char) ^ (password[pos2] == char)


if __name__ == '__main__':
    inputs = open('input_day2.txt', 'r')
    lines = inputs.readlines()
    inputs.close()
    filtered = filter(is_valid_password_1, lines)

    print('Part 1: {}'.format(len(list(filtered))))

    filtered2 = filter(is_valid_password_2, lines)

    print('Part 2: {}'.format(len(list(filtered2))))



