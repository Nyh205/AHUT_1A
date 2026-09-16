from __future__ import annotations # 这让类型注解能够正常工作
from typing import Iterator  # “t: Iterator[int]” 表示 t 是一个产出整数的迭代器


SOURCE_FILE = __file__


def insert_items(s: list[int], before: int, after: int) -> list[int]:
    """在 s 中每个 before 出现之后插入 after，然后返回 s。

    >>> test_s = [1, 5, 8, 5, 2, 3]
    >>> new_s = insert_items(test_s, 5, 7)
    >>> new_s
    [1, 5, 7, 8, 5, 7, 2, 3]
    >>> test_s
    [1, 5, 7, 8, 5, 7, 2, 3]
    >>> new_s is test_s
    True
    >>> double_s = [1, 2, 1, 2, 3, 3]
    >>> double_s = insert_items(double_s, 3, 4)
    >>> double_s
    [1, 2, 1, 2, 3, 4, 3, 4]
    >>> large_s = [1, 4, 8]
    >>> large_s2 = insert_items(large_s, 4, 4)
    >>> large_s2
    [1, 4, 4, 8]
    >>> large_s3 = insert_items(large_s2, 4, 6)
    >>> large_s3
    [1, 4, 6, 4, 6, 8]
    >>> large_s3 is large_s
    True
    """
    index = 0
    while index < len(s):
        if s[index] == before:
            s.insert(index + 1, after)
            index += 1
        index += 1
    return s

    # 另一种解法（反向遍历）：
    i = len(s) - 1
    while i >= 0:
        if s[i] == before:
            s.insert(i + 1, after)
        i -= 1
    return s





def group_by(s: list[int], fn) -> dict[int, list[int]]:
    """返回一个由若干列表组成的字典，这些列表一起包含
    s 的元素。每个列表的键是 fn
    作用于该列表中任意一个值时所返回的值。

    >>> group_by([12, 23, 14, 45], lambda p: p // 10)
    {1: [12, 14], 2: [23], 4: [45]}
    >>> group_by(range(-3, 4), lambda x: x * x)
    {9: [-3, 3], 4: [-2, 2], 1: [-1, 1], 0: [0]}
    """
    grouped = {}
    for x in s:
        key = fn(x)
        if key in grouped:
            grouped[key].append(x)
        else:
            grouped[key] = [x]
    return grouped


from typing import Iterator  # “t: Iterator[int]” 表示 t 是一个产出整数的迭代器

def count_occurrences(t: Iterator[int], n: int, x: int) -> int:
    """返回 x 等于迭代器 t
    的前 n 个元素之一的次数。

    >>> s = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> count_occurrences(s, 10, 9)
    3
    >>> t = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> count_occurrences(t, 3, 10)
    2
    >>> u = iter([3, 2, 2, 2, 1, 2, 1, 4, 4, 5, 5, 5])
    >>> count_occurrences(u, 1, 3)  # Only iterate over 3
    1
    >>> count_occurrences(u, 3, 2)  # Only iterate over 2, 2, 2
    3
    >>> list(u)                     # Ensure that the iterator has advanced the right amount
    [1, 2, 1, 4, 4, 5, 5, 5]
    >>> v = iter([4, 1, 6, 6, 7, 7, 6, 6, 2, 2, 2, 5])
    >>> count_occurrences(v, 6, 6)
    2
    """
    count = 0
    for _ in range(n):
        if next(t) == x:
            count += 1
    return count


def perms(seq):
    """生成给定序列的所有排列。每个排列都是一个列表，
    其中的元素是 SEQ 中的元素按不同顺序排列的结果。
    这些排列可以按任意顺序产出。

    >>> p = perms([100])
    >>> type(p)
    <class 'generator'>
    >>> next(p)
    [100]
    >>> try: # Prints "No more permutations!" if calling next would cause an error
    ...     next(p)
    ... except StopIteration:
    ...     print('No more permutations!')
    No more permutations!
    >>> sorted(perms([1, 2, 3])) # Returns a sorted list containing elements of the generator
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> sorted(perms((10, 20, 30)))
    [[10, 20, 30], [10, 30, 20], [20, 10, 30], [20, 30, 10], [30, 10, 20], [30, 20, 10]]
    >>> sorted(perms("ab"))
    [['a', 'b'], ['b', 'a']]
    """
    if not seq:
        yield []
    else:
        for p in perms(seq[1:]):
            for i in range(len(seq)):
                yield p[:i] + [seq[0]] + p[i:]


from typing import Iterator  # “t: Iterator[int]” 表示 t 是一个产出整数的迭代器

def repeated(t: Iterator[int], k: int) -> int:
    """返回迭代器 t 中连续出现 k 次的第一个值，
    对 t 调用 next 的次数要尽可能少。

    >>> s = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> repeated(s, 2)
    9
    >>> t = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> repeated(t, 3)
    8
    >>> u = iter([3, 2, 2, 2, 1, 2, 1, 4, 4, 5, 5, 5])
    >>> repeated(u, 3)
    2
    >>> repeated(u, 3)
    5
    >>> v = iter([4, 1, 6, 6, 7, 7, 8, 8, 2, 2, 2, 5])
    >>> repeated(v, 3)
    2
    """
    assert k > 1
    count = 0
    last_item = None
    while True:
        item = next(t)
        if item == last_item:
            count += 1
        else:
            last_item = item
            count = 1
        if count == k:
            return item

