def palindrome(s) -> bool:
    """
    Return `True` if a sequence `s` is the same forward and backward
    (e.g. if `s` is a palindrome), or `False` otherwise.

    Challenge: Implement this 2 ways:
    1. Using `reversed`
    2. Using `zip` and `reversed`

    >>> palindrome([3, 1, 4, 1, 5])
    False
    >>> palindrome([3, 1, 4, 1, 3])
    True
    >>> palindrome('seveneves')
    True
    >>> palindrome('seven eves')
    False
    """
    return list(reversed(s)) == list(s)

    # ALTERNATE SOLUTION
    return all([a == b for a, b in zip(s, reversed(s))])

def min_abs_indices(s) -> list[int]:
    """
    Returns a list of all indices of elements in s
    whose absolute value is equal to the minimum absolute value of s.

    Challenge: Implement this 2 ways:
    1. With a list comprehension
    2. Without a list comprehension (e.g. only use built-in functions for iteration)

    >>> min_abs_indices([-4, -3, -2, 3, 2, 4])
    [2, 4]
    >>> min_abs_indices([1, 2, 3, 4, 5])
    [0]
    """
    min_abs = min(map(abs, s))
    return [i for i in range(len(s)) if abs(s[i]) == min_abs]

    # ALTERNATE SOLUTION
    min_abs = min(map(abs, s))
    f = lambda i: abs(s[i]) == min_abs
    return list(filter(f, range(len(s))))


# Tree ADT
def tree(root_label, branches=[]):
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [root_label] + list(branches)

def label(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    return not branches(tree)


def yield_paths(t, total):
    """
    Yield each path from the root node to any other node in the tree
    that adds up to the target total.
    >>> t = tree(3, [tree(-1), tree(1, [tree(2, [tree(1)]), tree(3)]), tree(1, [tree(-1)])])
    >>> list(yield_paths(t, 3))  # path does not have to go to a leaf
    [[3], [3, 1, -1]]
    >>> list(yield_paths(t, 4))
    [[3, 1], [3, 1]]
    >>> list(yield_paths(t, 5))
    []
    >>> list(yield_paths(t, 6))
    [[3, 1, 2]]
    >>> list(yield_paths(t, 7))
    [[3, 1, 2, 1], [3, 1, 3]]
    """
    if label(t) == total:
        yield [label(t)]

    for b in branches(t):
        for path in yield_paths(b, total - label(t)):
            yield [label(t)] + path
