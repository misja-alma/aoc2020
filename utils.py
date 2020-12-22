def non_empty_lines(string: str) -> [str]:
    return list(filter(lambda line: len(line) > 0, string.split('\n')))
