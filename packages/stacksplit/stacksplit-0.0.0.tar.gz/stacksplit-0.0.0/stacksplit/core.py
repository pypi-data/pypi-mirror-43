"""Core functionallity for stacksplit module"""


def split(num, parts, smallest=1):
    """Generate all combinations of splitting <num> coins into <parts> stacks
     with minimum size of <smallest>.
    i.e. generate all combinations where the LENGTH of each tuple is <parts>,
     its SUM is <num> and its smallest element is <smallest>.

    Parameters: <num>: int, <parts>: int >= 1, <smallest>: int

    Example: Split a stack with 10 coins into 2 non-empty stacks:
    >>> import stacksplit
    >>> [i for i in stacksplit.split(10,2)]
    [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5)]

    Example: Split a stack of 5 coins into 3 empty or non-empty stacks:
    >>> import stacksplit
    >>> [i for i in stacksplit.split(5,3,0)]
    [(0, 0, 5), (0, 1, 4), (0, 2, 3), (1, 1, 3), (1, 2, 2)]
    """

    def _split(num, parts, smallest):
        """This function does the actual splitting.
        Designed with speed in mind. 'parts' must be > 1."""
        for i in range(smallest, num // parts + 1):
            if parts == 2:
                yield (i, num - i)
            else:
                for t in _split(num - i, parts - 1, i):
                    yield ((i,) + t)

    if parts < 1:
        raise ValueError("'parts' must be a positive non-zero integer.")
    elif parts == 1:
        # check for edge case: parts == 1 (only if smallest allows it)
        if smallest <= num:
            yield (num,)
    else:
        yield from _split(num, parts, smallest)
