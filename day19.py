from abc import *


class BaseRule:
    @abstractmethod
    def evaluate(self, string: str, index: int, rules_map: dict) -> [int]:
        # Return all indices ending after successful evaluations
        return NotImplemented


class AtomicRule(BaseRule):
    def __init__(self, char: str):
        self.char = char

    def evaluate(self, string: str, index: int, rules_map: dict) -> [int]:
        if index >= len(string):
            return []
        else:
            if string[index] == self.char:
                return [index + 1]
            else:
                return []


class SequenceRule(BaseRule):
    def __init__(self, rules: [str]):
        self.rules = rules

    def evaluate(self, string: str, index: int, rules_map: dict) -> [int]:
        valid_indices = [index]
        for rule_index in self.rules:
            new_valid_indices = []
            rule = rules_map[rule_index]
            for valid_index in valid_indices:
                if valid_index < len(string):
                    new_indices = rule.evaluate(string, valid_index, rules_map)
                    new_valid_indices.extend(new_indices)
            valid_indices = new_valid_indices
        return valid_indices


class BranchRule(BaseRule):
    def __init__(self, rule1: BaseRule, rule2: BaseRule):
        self.rule1 = rule1
        self.rule2 = rule2

    def evaluate(self, string: str, index: int, rules_map: dict) -> [int]:
        if index >= len(string):
            return []

        valid_for_rule1 = self.rule1.evaluate(string, index, rules_map)
        valid_for_rule2 = self.rule2.evaluate(string, index, rules_map)
        valid_for_rule1.extend(valid_for_rule2)
        return valid_for_rule1


def parse_rule(rule_str: str) -> BaseRule:
    or_index = rule_str.find('|')
    if or_index > 0:
        left = rule_str[0:or_index].strip()
        right = rule_str[or_index + 1:].strip()
        left_rule = parse_rule(left)
        right_rule = parse_rule(right)
        return BranchRule(left_rule, right_rule)

    if rule_str.find('"') < 0:
        elements = rule_str.split(' ')
        return SequenceRule(elements)
    else:
        return AtomicRule(rule_str[1:len(rule_str) - 1])


def parse_key_rule(line: str) -> (str, BaseRule):
    key_rule = line.split(':')
    key = key_rule[0]
    rule_str = key_rule[1].strip()
    return key, parse_rule(rule_str)


def full_match(rule: BaseRule, string: str, rules_map: dict) -> bool:
    indices = rule.evaluate(string, 0, rules_map)
    return len(string) in indices


if __name__ == '__main__':
    inputs = open('input_day19.txt', 'r')
    blocks = inputs.read().split('\n\n')
    inputs.close()

    rules = list(filter(lambda line: len(line) > 0, blocks[0].split('\n')))
    messages = list(filter(lambda line: len(line) > 0, blocks[1].split('\n')))

    # parse rules and put them in a hashmap by key
    # for each rule: compose it of its subrules; a composed rule is a list of subrules where a subrule can either
    # be a:
    # sequenceRule (containing 2 other rules that have to be valid in sequence)
    # branchRule (containing 2 other rules of which one needs to be valid)
    # atomicRule (containing only a char)
    # Then take rule 0 and let it evaluate all the inputs.

    rules_map = {}
    for rule in rules:
        (key, parsed_rule) = parse_key_rule(rule)
        rules_map[key] = parsed_rule

    rule0 = rules_map['0']
    valid_rules = list(filter(lambda rule: full_match(rule0, rule, rules_map), messages))
    print('Part 1: {}'.format(len(valid_rules)))

    rules_map['8'] = parse_rule('42 | 42 8')
    rules_map['11'] = parse_rule('42 31 | 42 11 31')

    valid_rules = list(filter(lambda rule: full_match(rule0, rule, rules_map), messages))
    print('Part 2: {}'.format(len(valid_rules)))
