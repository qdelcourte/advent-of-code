import os
import random

def read_from_main(execution_file: str, filename: str):
    return os.path.join(os.path.dirname(execution_file), filename)

def read_input_from_main(execution_file: str, split_lines: bool = True):
    b = open(read_from_main(execution_file, "input.txt"), 'r').read()
    return b.splitlines() if split_lines else b

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

def flatten(list_of_lists):
    return [x for xs in list_of_lists for x in xs]

class Colors:
    red = lambda s: "\033[91m{}\033[00m".format(s)
    green = lambda s: "\033[92m{}\033[00m".format(s)
    yellow = lambda s: "\033[93m{}\033[00m".format(s)
    light_purple = lambda s: "\033[94m{}\033[00m".format(s)
    purple = lambda s: "\033[95m{}\033[00m".format(s)
    cyan = lambda s: "\033[96m{}\033[00m".format(s)
    light_gray = lambda s: "\033[97m{}\033[00m".format(s)
    black = lambda s: "\033[90m{}\033[00m".format(s)  # Corrected from 98 to 90 (standard ANSI)

    @classmethod
    def list(cls):
        return [
            attr for attr_name, attr in cls.__dict__.items()
            if callable(attr) and not attr_name.startswith("__")
        ]

    @classmethod
    def random(cls, text):
        """
        Applies a randomly selected color function to the given text.

        Parameters
        ----------
        text : str
            The text to which the randomly chosen color function will be applied.

        Returns
        -------
        str
            The input text formatted with a randomly selected color function

        Example
        -------
        >>> Colors.random("Hello")
        '\033[94mHello\033[00m'   # text displayed in a random color
        """
        return random.choice(cls.list())(text)

    @classmethod
    def enumerate(cls, iterable, start=0):
        """
        Enumerates over `iterable`, pairing each element with a color function from
        the class's color list, cycling through the colors.

        Yields
        ------
        tuple
            (color_function, index, item)

        Example
        -------
        >>> for color_func, idx, val in Colors.enumerate(["a", "b", "c"]):
        ...     print(color_func(val))
        [RED]a[/RED]
        [GREEN]b[/GREEN]
        [RED]c[/RED]
        """
        colors = cls.list()
        n = len(colors)
        for i, item in enumerate(iterable, start):
            yield colors[i % n], i, item
