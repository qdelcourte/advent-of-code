# https://adventofcode.com/2023/day/12
# --- Day 12: Hot Springs ---

from functools import cache


# First version
# def get_combinations(regex, original_str, replacements_dict, current_combination=""):
#     if not original_str:
#         return bool(regex.match(current_combination))
#     else:
#         c = 0
#         first_char = original_str[0]
#         remaining_str = original_str[1:]
#         if first_char in replacements_dict:
#             for replacement in replacements_dict[first_char]:
#                 c += get_combinations(regex, remaining_str, replacements_dict,
#                                       current_combination + replacement)
#         else:
#             c += get_combinations(regex, remaining_str, replacements_dict,
#                                   current_combination + first_char)
#
#         return c


@cache
def get_combinations4(springs, groups, group_counter=0):
    if len(springs) == 0:
        return not groups and not group_counter

    c = 0
    symbols = ['.', '#'] if springs[0] == '?' else [springs[0]]
    for symbol in symbols:
        if symbol == '#':
            # Continue group
            c += get_combinations4(springs[1:], groups, group_counter+1)
        else:
            if group_counter:
                # Group valid ?
                if groups and groups[0] == group_counter:
                    c += get_combinations4(springs[1:], groups[1:])
            else:
                c += get_combinations4(springs[1:], groups)

    return c


TEST_INPUT = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def solve(lines):
    return sum(
        get_combinations4(springs + '.', tuple(map(int, groups.split(','))))
        for springs, groups in lines
    )


def test_1():
    return solve([line.split() for line in TEST_INPUT.splitlines()])


def part_1():
    return solve([line.split() for line in lines])


def test_2():
    return solve(map(lambda x: ('?'.join([x[0]]*5), ','.join([x[1]]*5)), [line.split() for line in TEST_INPUT.splitlines()]))


def part_2():
    return solve(map(lambda x: ('?'.join([x[0]]*5), ','.join([x[1]]*5)), [line.split() for line in lines]))


if __name__ == '__main__':
    t1 = test_1()
    assert t1 == 21, t1
    print(f"test 1: {t1}")
    lines = open('./input.txt', 'r').read().splitlines()
    r1 = part_1()
    assert r1 == 6827, r1
    print(f"#1: {r1}")
    t2 = test_2()
    assert t2 == 525152, t2
    print(f"test 2: {t2}")
    r2 = part_2()
    assert r2 == 1537505634471, r2
    print(f"#2: {r2}")
