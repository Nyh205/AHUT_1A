"""
Implementations adapted from Prof. John DeNero's lecture video
https://www.youtube.com/watch?v=MG5lJNfMjFA&list=PLx38hZJ5RLZdEOl-AAfpul_-iySZzI4C3&index=10
"""

def count_partitions_original(n: int, m: int) -> int:
    """
    Original implementation from Lecture 06
    >>> count_partitions_original(6, 4)
    9
    """
    if n == 0:
        return 1
    elif n < 0:
        return 0
    elif m == 0:
        return 0
    else:
        with_m = count_partitions_original(n - m, m)
        without_m = count_partitions_original(n, m - 1)
        return with_m + without_m


def count_partitions_simplified(n: int, m: int) -> int:
    """
    Simplified version that combines the 2nd and 3rd original base cases,
    and moves the first base case into the `else` clause.
    >>> count_partitions_simplified(6, 4)
    9
    """
    if n < 0 or m == 0:
        return 0
    else:
        exact_match = 0
        if n == m:
            exact_match = 1
        with_m = count_partitions_simplified(n - m, m)
        without_m = count_partitions_simplified(n, m - 1)
        return exact_match + with_m + without_m


def list_partitions(n: int, m: int) -> list[list[int]]:
    """
    Instead of counting the total number of partitions,
    this function returns a list of all partitions,
    where each partition is a list.
    >>> for p in sorted(list_partitions(6, 4)):
    ...     print(p)
    [1, 1, 1, 1, 1, 1]
    [1, 1, 1, 1, 2]
    [1, 1, 1, 3]
    [1, 1, 2, 2]
    [1, 1, 4]
    [1, 2, 3]
    [2, 2, 2]
    [2, 4]
    [3, 3]
    """
    if n < 0 or m == 0:
        return []
    else:
        exact_match = []
        if n == m:
            exact_match = [[m]]
        with_m = [p + [m] for p in list_partitions(n - m, m)]
        without_m = list_partitions(n, m - 1)
        return exact_match + with_m + without_m


def list_partitions_str(n: int, m: int) -> list[str]:
    """
    Instead of returning a 2D list, return a list of strings
    representing each partition as a sum.
    >>> for p in sorted(list_partitions_str(6, 4)):
    ...     print(p)
    1 + 1 + 1 + 1 + 1 + 1
    1 + 1 + 1 + 1 + 2
    1 + 1 + 1 + 3
    1 + 1 + 2 + 2
    1 + 1 + 4
    1 + 2 + 3
    2 + 2 + 2
    2 + 4
    3 + 3
    """
    if n < 0 or m == 0:
        return []
    else:
        exact_match = []
        if n == m:
            exact_match = [str(m)]
        with_m = [f"{p} + {m}" for p in list_partitions_str(n - m, m)]
        without_m = list_partitions_str(n, m - 1)
        return exact_match + with_m + without_m


def yield_partitions(n: int, m: int):
    """
    Yield each partition, one at a time.
    >>> gen = yield_partitions(6, 4)
    >>> next(gen)
    '2 + 4'
    >>> next(gen)
    '1 + 1 + 4'
    >>> for p in sorted(yield_partitions(6, 4)):
    ...     print(p)
    1 + 1 + 1 + 1 + 1 + 1
    1 + 1 + 1 + 1 + 2
    1 + 1 + 1 + 3
    1 + 1 + 2 + 2
    1 + 1 + 4
    1 + 2 + 3
    2 + 2 + 2
    2 + 4
    3 + 3
    """
    if n > 0 and m > 0:
        if n == m:
            yield str(m)
        for p in yield_partitions(n - m, m):
            yield f"{p} + {m}"
        yield from yield_partitions(n, m - 1)


"""
python3 -i 10-partitions.py

>>> s = list(yield_partitions(60, 50))  # takes a few seconds...
>>> len(s)  # ... because a lot of computation was done!
966370
>>> gen = yield_partitions(60, 50)  # lazy evaluation is faster!
>>> next(gen)
'10 + 50'
>>> next(gen)
'1 + 9 + 50'
>>> # unlike the original implementation, we can see the first few values without computing the rest
>>> for _ in range(10):
...     print(next(gen))
...
2 + 8 + 50
1 + 1 + 8 + 50
3 + 7 + 50
1 + 2 + 7 + 50
1 + 1 + 1 + 7 + 50
4 + 6 + 50
1 + 3 + 6 + 50
2 + 2 + 6 + 50
1 + 1 + 2 + 6 + 50
1 + 1 + 1 + 1 + 6 + 50
"""
