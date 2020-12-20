# format: n token separated by space or new line, separated by 2 newlines

import re


def valid_keys(dct):
    # check the keys: the 7 obligatory ones need to be present
    # the other ones can be max one, cid
    obligatory_keys = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    keys = set(dct.keys())
    obligatory = len(keys.intersection(obligatory_keys))
    optional = 'cid' in keys
    return obligatory == 7 and (len(keys) == 7 or (len(keys) == 8) and optional)


def words_to_dict(wrds):
    def to_tuple(wrd):
        [key, value] = wrd.split(':')
        return key, value

    return dict(list(map(to_tuple, wrds)))


# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.

def invalid_value(keyvalue):
    def valid_cm(x):
        return x.endswith('cm') and 150 <= int(x[0: len(x) - 2]) <= 193

    def valid_in(x):
        return x.endswith('in') and 59 <= int(x[0: len(x) - 2]) <= 76

    (key, value) = keyvalue
    is_valid = {
        'byr': lambda x: len(x) == 4 and 1920 <= int(x) <= 2002,
        'iyr': lambda x: len(x) == 4 and 2010 <= int(x) <= 2020,
        'eyr': lambda x: len(x) == 4 and 2020 <= int(x) <= 2030,
        'hgt': lambda x: valid_cm(x) or valid_in(x),
        'hcl': lambda x: re.compile('#([0-9]|[a-f]){6}').match(x) is not None,
        'ecl': lambda x: x in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
        'pid': lambda x: len(x) == 9 and x.isdigit(),
        'cid': lambda x: True
    }[key](value)
    return not is_valid


def valid_values(dct):
    invalids = filter(invalid_value, dct.items())
    return len(list(invalids)) == 0


if __name__ == '__main__':
    inputs = open('input_day4.txt', 'r')
    text = inputs.read()
    inputs.close()
    lines = text.split('\n\n')
    words = map(lambda line: line.split(), lines)
    dicts = map(words_to_dict, words)
    valid = list(filter(valid_keys, dicts))
    print ("Part 1: {}".format(len(valid)))

    valid_vals = filter(valid_values, valid)
    print("Part 2: {}".format(len(list(valid_vals))))





