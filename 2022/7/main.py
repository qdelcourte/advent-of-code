# https://adventofcode.com/2022/day/7
#--- Day 7: No Space Left On Device ---

TEST_INPUT = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

def compile_folder_structure(history):
    dirs = {}
    current_command = None
    current_path = []
    for line in history:
        if line.startswith('$ cd'):
            _, current_command, folder_path = line.split()
            if folder_path == '..':
                current_path.pop()
            else:
                if tuple(current_path) in dirs:
                    dirs[tuple(current_path)]['folders'].append(tuple(current_path + [folder_path]))
                current_path.append(folder_path)
                dirs.setdefault(tuple(current_path), {}).setdefault('folders', [])
        elif line.startswith('$ ls'):
            current_command = 'ls'
        elif current_command == 'ls':
            if line.startswith('dir'):
                dirs.setdefault(tuple(current_path + [line.split()[1]]), {})
            else:
                size, filename = line.split()
                node = dirs.setdefault(tuple(current_path), {})
                node.setdefault('files', []).append({"size": int(size), "filename": filename})
                node['total'] = node.get('total', 0) + int(size)

    return dirs

def compile_totals(dirs, folder = tuple('/'), tabbed = 1, debug=False):
    if debug:
        print(f"{(tabbed-1)*'  '}-", folder[-1], '(dir)', dirs[folder].get('total', 0))

    c = {}
    subfolders_total = sum(
        (c.update(compile_totals(dirs, sub, tabbed + 1)) or c[sub])
        for sub in dirs[folder].get('folders', [])
    )
    c[folder] = subfolders_total + dirs[folder].get('total', 0)

    if debug:
        for file in dirs[folder].get('files', []):
            print(f"{tabbed*'  '}-", file['name'], f"(file, size={file['size']})")
        print(f"{(tabbed-1)*'  '} total {folder} =", c[folder])

    return c

def solve(history):
    compiled_totals = compile_totals(compile_folder_structure(history))
    return sum(filter(lambda x: x <= 100000, compiled_totals.values()))

def solve2(history):
    compiled_totals = compile_totals(compile_folder_structure(history))

    total_disk_space = 70000000
    need_unused_space = 30000000
    total_outermost_dir = compiled_totals[tuple('/')]
    actual_unused_space = total_disk_space - total_outermost_dir
    target_free_space = need_unused_space - actual_unused_space

    return next(filter(lambda x: x >= target_free_space, sorted(compiled_totals.values())))

if __name__  == '__main__':
    test_input = TEST_INPUT.splitlines()
    r1 = solve(test_input)
    assert r1 == 95437, r1
    data = open('./input.txt').read().splitlines()
    r1 = solve(data)
    assert r1 == 1644735, r1
    r2 = solve2(test_input)
    assert r2 == 24933642, r2
    r2 = solve2(data)
    assert r2 == 1300850, r2
