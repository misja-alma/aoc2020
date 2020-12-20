import re
import copy

# departure location: 42-322 or 347-954
pattern = re.compile(r"(?P<name>.+): (?P<start1>[\d]+)-(?P<end1>[\d]+) or (?P<start2>[\d]+)-(?P<end2>[\d]+)")


def parse_field(field: str) -> ([range], str):
    match = pattern.match(field)
    start1 = int(match.group('start1'))
    end1 = int(match.group('end1'))
    start2 = int(match.group('start2'))
    end2 = int(match.group('end2'))
    name = match.group('name')
    return [range(start1, end1 + 1), range(start2, end2 + 1)], name


def parse_fields(fields: [str]) -> [([range], str)]:
    return list(map(parse_field, fields))


def matches_any_range(field: int, rngs: [range]) -> bool:
    for rng in rngs:
        if field in rng:
            return True

    return False


def select_position_with_fewest_possible_fields(possible_field_indices_per_position: [set], unmatched_field_positions: set) -> int:
    smallest_size = 100000000
    smallest_index = None
    for position in unmatched_field_positions:
        poss_size = len(possible_field_indices_per_position[position])
        if poss_size < smallest_size:
            smallest_size = poss_size
            smallest_index = position
    return smallest_index


def smart_find_valid_field_order(possible_field_indices_per_position: [set],
                                 matched_fields_by_position: {int, str},
                                 unmatched_field_positions: set) -> {int, str}:
    if len(unmatched_field_positions) == 0:
        return matched_fields_by_position

    position = select_position_with_fewest_possible_fields(possible_field_indices_per_position, unmatched_field_positions)
    possible_field_indices_for_pos = possible_field_indices_per_position[position]
    if len(possible_field_indices_for_pos) == 0:
        return None
    new_matched_fields_by_position = matched_fields_by_position.copy()
    new_unmatched_field_positions = unmatched_field_positions.copy()

    for field in possible_field_indices_for_pos:
        new_matched_fields_by_position[position] = field
        new_unmatched_field_positions.remove(position)
        new_possible_field_indices_per_position = copy.deepcopy(possible_field_indices_per_position)
        for indices in new_possible_field_indices_per_position:
            indices.discard(field)
        result = smart_find_valid_field_order(new_possible_field_indices_per_position,
                                              new_matched_fields_by_position,
                                              new_unmatched_field_positions)
        if result is not None:
            return result
        del new_matched_fields_by_position[position]
        new_unmatched_field_positions.add(position)

    return None


def find_valid_field_order_smart(tickets: [[int]], ranges_with_names: [([range], str)]) -> [str]:
    all_field_names = list(map(lambda x: x[1], ranges_with_names))
    unmatched_field_positions = set(range(0, len(ranges_with_names)))
    possible_fields_per_position = []
    for position_in_ticket in range(0, len(ranges_with_names)):
        matching_fields = set(filter(lambda field: all(map(lambda ticket: matches_any_range(ticket[position_in_ticket], ranges_with_names[field][0]), tickets)), range(0, len(ranges_with_names))))
        possible_fields_per_position.append(matching_fields)

    result = smart_find_valid_field_order(possible_fields_per_position, {}, unmatched_field_positions)
    result_list = list(range(0, len(result)))
    for (index, val) in result.items():
        result_list[index] = all_field_names[val]
    return result_list


if __name__ == '__main__':
    inputs = open('input_day16.txt', 'r')
    lines = inputs.read()
    inputs.close()

    parts = lines.split('\n\n')
    fields = parts[0].split('\n')
    my_ticket = list(map(int, parts[1].split('\n')[1].split(',')))
    nearby_tickets = list(map(lambda x: list(map(int, x.split(','))), filter(lambda ln: len(ln) > 1, parts[2].split('\n')[1:])))

    ranges_with_names = parse_fields(fields)
    invalid_fields = []
    for ticket in nearby_tickets:
        for fld in ticket:
            valid = False
            for (ranges, _) in ranges_with_names:
                for rng in ranges:
                    if fld in rng:
                        valid = True
                        break
            if not valid:
                invalid_fields.append(fld)

    print('Part 1: {}'.format(sum(invalid_fields)))

    invalid_fields_set = set(invalid_fields)
    valid_tickets = list(filter(lambda t: not invalid_fields_set.intersection(set(t)), nearby_tickets))

    valid_fields = find_valid_field_order_smart(valid_tickets, ranges_with_names)

    my_field_product = 1
    for i in range(0, len(my_ticket)):
        field_name = valid_fields[i]
        if field_name.startswith('departure'):
            my_field_product *= my_ticket[i]

    print('Part 2: {}'.format(my_field_product))