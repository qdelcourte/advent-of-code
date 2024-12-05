# https://adventofcode.com/2023/day/19
# --- Day 19: Aplenty ---

import operator
from functools import reduce
from operator import lt, gt

TEST_INPUT = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""


def parse(data):
    lines = data.splitlines()

    ratings = []
    workflows = {}

    is_input = False
    for line in lines:
        if line == '':
            is_input = True
            continue
        if is_input:
            ratings.append({
                part[0]: int(part[2:len(part)])
                for part in line[1:len(line) - 1].split(',')
            })
        else:
            workflow_name, workflow = line.split('{')
            workflows[workflow_name] = []
            workflow_parts = workflow[0:len(workflow)-1].split(',')
            final = workflow_parts.pop()
            for i, p in enumerate(workflow_parts):
                cond, re = p.split(':')
                workflows[workflow_name].append((cond[0], gt if cond[1] == '>' else lt, int(cond[2:]), re, final if i == len(workflow_parts)-1 else None))

    return workflows, ratings


def part_1(data):
    workflows, ratings = parse(data)
    total = 0
    for rating in ratings:
        done = False
        workflow_name = 'in'
        while not done:
            for var, func, value, ret, _final in workflows[workflow_name]:
                if func(rating[var], value):
                    workflow_name = ret
                    break
                else:
                    if _final:
                        workflow_name = _final
                    else:
                        continue

            if workflow_name in ['A', 'R']:
                done = True
            if workflow_name == 'A':
                total += sum(rating.values())

    return total


def part_2(data):
    workflows, _ = parse(data)

    combinations_ranges = dict(zip(list('xmas'), [(1, 4000)]*4))
    queue = [('in', list(combinations_ranges.values()))]

    total = []
    while queue:
        workflow_name, parts = queue.pop()
        # print('===', workflow_name, '====', parts)
        if workflow_name == 'R':
            continue
        if workflow_name == 'A':
            total.append(parts)
            continue

        parts_dup = parts.copy()
        exclude_ranges = parts.copy()
        exclude_range_workflow = None
        for var, func, value, ret, _final in workflows[workflow_name]:
            # print(var, func, value, ret, _final)
            r = parts_dup['xmas'.index(var)]
            # print(r)
            if func == gt:
                if r[0] > value:
                    new_range = r
                    parts_dup['xmas'.index(var)] = new_range
                    new_workflow = ret
                    # print('gt', new_range, parts_dup, new_workflow)
                    queue.append((new_workflow, parts_dup.copy()))
                    # print('parts', reduce(operator.mul, [(n - m) + 1 for m, n in parts_dup]))
                elif r[1] > value > r[0]:
                    new_range = (value+1, r[1])
                    parts_dup['xmas'.index(var)] = new_range
                    new_workflow = ret
                    # print('gt', new_range, parts_dup, new_workflow)
                    queue.append((new_workflow, parts_dup.copy()))
                    # print('parts', reduce(operator.mul, [(n - m) + 1 for m, n in parts_dup]))
                    if _final:
                        new_range = (r[0], value)
                        exclude_ranges['xmas'.index(var)] = new_range
                        parts_dup['xmas'.index(var)] = new_range
                        exclude_range_workflow = _final
                        # print('lt', new_range, exclude_ranges, new_workflow)
                        # queue.append((new_workflow, exclude_ranges))
                    else:
                        parts_dup['xmas'.index(var)] = (r[0], value)
                        exclude_ranges['xmas'.index(var)] = (r[0], value)
            elif func == lt:
                if r[1] < value:
                    new_range = r
                    parts_dup['xmas'.index(var)] = new_range
                    new_workflow = ret
                    # print('lt1', new_range, parts_dup, new_workflow)
                    queue.append((new_workflow, parts_dup.copy()))
                    # print('parts', reduce(operator.mul, [(n - m) + 1 for m, n in parts_dup]))
                elif r[0] < value < r[1]:
                    new_range = (r[0], value-1)
                    parts_dup['xmas'.index(var)] = new_range
                    new_workflow = ret
                    # print('lt2', new_range, parts_dup, new_workflow)
                    queue.append((new_workflow, parts_dup.copy()))
                    # print('parts', reduce(operator.mul, [(n - m) + 1 for m, n in parts_dup]))
                    if _final:
                        new_range = (value, r[1])
                        parts_dup['xmas'.index(var)] = new_range
                        exclude_ranges['xmas'.index(var)] = new_range
                        exclude_range_workflow = _final
                        # print('lt', new_range, parts_dup, new_workflow)
                        # queue.append((new_workflow, parts_dup))
                    else:
                        parts_dup['xmas'.index(var)] = (value, r[1])
                        exclude_ranges['xmas'.index(var)] = (value, r[1])

        if exclude_ranges and exclude_range_workflow:
            queue.append((exclude_range_workflow, exclude_ranges.copy()))
            # print('exclude ranges', exclude_ranges, exclude_range_workflow)
            # print('exclude parts', reduce(operator.mul, [(n - m) + 1 for m, n in exclude_ranges]))

    result = sum([reduce(operator.mul, [(n - m)+1 for m, n in t]) for t in total])
    print(result)

    return result


if __name__ == '__main__':
    t1 = part_1(TEST_INPUT)
    assert t1 == 19114, t1
    print(f"test 1: {t1}")
    data = open('./input.txt', 'r').read()
    r1 = part_1(data)
    assert r1 == 399284, r1
    print(f"#1: {r1}")
    t2 = part_2(TEST_INPUT)
    assert t2 == 167409079868000, t2
    print(f"test 2: {t2}")
    r2 = part_2(data)
    assert r2 == 121964982771486, r2
    print(f"#2: {r2}")
