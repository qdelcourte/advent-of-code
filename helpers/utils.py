import os

def read_input_from_main(execution_file: str):
    return open(os.path.join(os.path.dirname(execution_file), "input.txt"), 'r').read().splitlines()

def pprint_matrix(m):
    """
    Pretty print matrix
    """
    for r in range(len(m)):  # rows
        for c in range(len(m[r])):  # columns
            print(m[r][c], " ", sep="", end="")
        print()
    print("-------------")

def str_to_matrix(data: str):
    return [list(map(int, line)) for line in data]

# Colors
red = lambda s: "\033[91m {}\033[00m".format(s)
green = lambda s: "\033[92m {}\033[00m".format(s)
yellow = lambda s: "\033[93m {}\033[00m".format(s)
light_purple = lambda s: "\033[94m {}\033[00m".format(s)
purple = lambda s: "\033[95m {}\033[00m".format(s)
cyan = lambda s: "\033[96m {}\033[00m".format(s)
light_gray = lambda s: "\033[97m {}\033[00m".format(s)
black = lambda s: "\033[90m {}\033[00m".format(s)  # Corrected from 98 to 90 (standard ANSI)
