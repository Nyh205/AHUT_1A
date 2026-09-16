def flip_dict(dct: dict) -> dict:
    """
    Return a new dictionary that flips the key-value pairs of the input dictionary.
    Assume the original values are valid keys.

    If there are duplicate values in the original dictionary, the returned dictionary
    should have a list of corresponding original keys (see the doctests), preserving
    the original insertion order.

    >>> roman_numerals = {'I': 1, 'V': 5, 'X': 10}
    >>> flip_dict(roman_numerals)
    {1: 'I', 5: 'V', 10: 'X'}
    >>> contacts = {'Jane Doe': 'jane@example.com', 'Bob Jones': 'bob@example.com', 'Alice Williams': 'awilliams@berkeley.edu'}
    >>> flip_dict(contacts)
    {'jane@example.com': 'Jane Doe', 'bob@example.com': 'Bob Jones', 'awilliams@berkeley.edu': 'Alice Williams'}
    >>> lengths = {'cat': 3, 'hat': 3, 'bottle': 6, 'a': 1, 'mat': 3, 'an': 2, 'in': 2}
    >>> flip_dict(lengths)
    {3: ['cat', 'hat', 'mat'], 6: 'bottle', 1: 'a', 2: ['an', 'in']}
    """
    "YOUR CODE HERE"


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


def leaves(t):
    """
    Return a list of all the leaf labels of the tree `t`
    >>> leaves(tree(2))
    [2]
    >>> leaves(tree(3, [tree(1), tree(2)]))
    [1, 2]
    >>> leaves(tree(5, [tree(1, [tree(0)]), tree(3, [tree(4, [tree(6)])]), tree(2)]))
    [0, 6, 2]
    """
    if is_leaf(t):
        return __________________________
    else:
        return sum([__________________________], [])

def double(t):
    """
    Return a new tree ADT which is the result of
    doubling the labels of every node in the original tree `t`.
    >>> double(tree(1)) == tree(2)
    True
    >>> double(tree(3, [tree(1), tree(2)])) == tree(6, [tree(2), tree(4)])
    True
    """
    "YOUR CODE HERE"

def count_paths(t, total):
    """
    Return the number of paths from the root node to any other node in the tree
    that adds up to the target total.
    >>> t = tree(3, [tree(-1), tree(1, [tree(2, [tree(1)]), tree(3)]), tree(1, [tree(-1)])])
    >>> count_paths(t, 3)  # path does not have to go to a leaf
    2
    >>> count_paths(t, 4)
    2
    >>> count_paths(t, 5)
    0
    >>> count_paths(t, 6)
    1
    >>> count_paths(t, 7)
    2
    """
    if __________________:
        found = __________________
    else:
        found = __________________
    return found + sum(__________________)
