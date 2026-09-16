def inventory_pickup(inventory: list, items: list, capacity: int) -> list:
    """Simulate picking up every item in items and add them, one at a time, to the inventory IN PLACE.
    The function should return the mutated inventory.
    
    >>> inv = [1, 2, 1, 3, 1]
    >>> inv_test = inventory_pickup(inv, [1, 4], 10)
    >>> inv_test
    [2, 3, 1, 4]

    >>> inv2 = [11, 12, 13]
    >>> inv2_test = inventory_pickup(inv2, inv2, 7)
    >>> inv2_test
    [11, 12, 13]
    
    >>> inv3 = [1, 2, 1, 3, 1]
    >>> check_mutation = inv3
    >>> inv3_test = inventory_pickup(inv3, inv3, 3)
    >>> inv3_test
    [2, 3, 1]
    >>> check_mutation is inv3_test
    True
    
    >>> inv4 = [1, 2, 3, 4]
    >>> inv4_test = inventory_pickup(inv4, [5, 6, 7, 8, 9, 10], 10)
    >>> inv4_test
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    >>> inv5 = [1, 2, 3, 4]
    >>> inv5_test = inventory_pickup(inv5, [5, 6, 7, 8], 6)
    >>> inv5_test
    [3, 4, 5, 6, 7, 8]
    
    >>> inv6 = ['hello', 'world']
    >>> inv6_test = inventory_pickup(inv6, ['hi', 'hello'], 4)
    >>> inv6_test
    ['world', 'hi', 'hello']
    """
    "*** YOUR CODE HERE ***"


def berry_finder(t):
    """Returns True if t contains a node with the value 'berry' and 
    False otherwise.

    >>> scrat = tree('berry')
    >>> berry_finder(scrat)
    True
    >>> sproul = tree('roots', [tree('branch1', [tree('leaf'), tree('berry')]), tree('branch2')])
    >>> berry_finder(sproul)
    True
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> berry_finder(numbers)
    False
    >>> t = tree(1, [tree('berry',[tree('not berry')])])
    >>> berry_finder(t)
    True
    """
    "*** YOUR CODE HERE ***"


def size_of_tree(t):
    """Return the number of entries in the tree.
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    >>> size_of_tree(numbers)
    7
    """
    "*** YOUR CODE HERE ***"


def make_path(t, p):
    """Return a tree with all of the nodes of t and a path with labels p.

    >>> t2 = tree(5, [tree(6), tree(7)])
    >>> t1 = tree(3, [tree(4), t2])
    >>> make_path(t1, [3, 5, 7]) == t1
    True
    >>> print_tree(make_path(t1, [3, 8, 9, 1]))
    3
      4
      5
        6
        7
      8
        9
          1
    >>> print_tree(make_path(t1, [3, 4, 8, 9]))
    3
      4
        8
          9
      5
        6
        7
    >>> print_tree(make_path(tree(2, [tree(1), t1]), [2, 3, 5, 6, 8]))
    2
      1
      3
        4
        5
          6
            8
          7
    """
    assert p[0] == label(t), 'It is not possible to make this path'
    if len(p) == 1:
        return ____
    new_branches = []
    found_p1 = False
    for b in branches(t):
        if ____:
            "*** YOUR CODE HERE ***"
        else:
            new_branches.append(b)
    if not found_p1:
        new_branches.append(make_path(____, ____))
    return tree(____, new_branches)


def merge(incr_a, incr_b):
    """Yield the elements of strictly increasing iterables incr_a and incr_b, removing
    repeats. Assume that incr_a and incr_b have no repeats. incr_a or incr_b may or may not
    be infinite sequences.

    >>> m = merge([0, 2, 4, 6, 8, 10, 12, 14], [0, 3, 6, 9, 12, 15])
    >>> type(m)
    <class 'generator'>
    >>> list(m)
    [0, 2, 3, 4, 6, 8, 9, 10, 12, 14, 15]
    >>> def big(n):
    ...    k = 0
    ...    while True: yield k; k += n
    >>> m = merge(big(2), big(3))
    >>> [next(m) for _ in range(11)]
    [0, 2, 3, 4, 6, 8, 9, 10, 12, 14, 15]
    """
    iter_a, iter_b = iter(incr_a), iter(incr_b)
    next_a, next_b = next(iter_a, None), next(iter_b, None)
    "*** YOUR CODE HERE ***"


def yield_paths(t, target):
    """
    Yields all possible paths from the root of t to a node with the label
    target as a list.

    >>> t1 = tree(1, [tree(2, [tree(3), tree(4, [tree(6)]), tree(5)]), tree(5)])
    >>> print_tree(t1)
    1
      2
        3
        4
          6
        5
      5
    >>> next(yield_paths(t1, 6))
    [1, 2, 4, 6]
    >>> path_to_5 = yield_paths(t1, 5)
    >>> sorted(list(path_to_5))
    [[1, 2, 5], [1, 5]]

    >>> t2 = tree(0, [tree(2, [t1])])
    >>> print_tree(t2)
    0
      2
        1
          2
            3
            4
              6
            5
          5
    >>> path_to_2 = yield_paths(t2, 2)
    >>> sorted(list(path_to_2))
    [[0, 2], [0, 2, 1, 2]]
    """
    if label(t) == target:
        yield ____
    for b in branches(t):
        for ____ in ____:
            yield ____


passphrase = 'REPLACE_THIS_WITH_PASSPHRASE'

def midsem_survey(p):
    """
    You do not need to understand this code.
    >>> midsem_survey(passphrase)
    '2bf925d47c03503d3ebe5a6fc12d479b8d12f14c0494b43deba963a0'
    """
    import hashlib
    return hashlib.sha224(p.encode('utf-8')).hexdigest()



# Tree Data Abstraction

def tree(label, branches=[]):
    """Construct a tree with the given label value and a list of branches."""
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)

def label(tree):
    """Return the label value of a tree."""
    return tree[0]

def branches(tree):
    """Return the list of branches of the given tree."""
    return tree[1:]

def is_tree(tree):
    """Returns True if the given tree is a tree, and False otherwise."""
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    """Returns True if the given tree's list of branches is empty, and False
    otherwise.
    """
    return not branches(tree)

def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

def copy_tree(t):
    """Returns a copy of t. Only for testing purposes.

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(label(t), [copy_tree(b) for b in branches(t)])

