def inventory_pickup(inventory: list, items: list, capacity: int) -> list:
    """模拟拾取 items 中的每一个物品，并把它们一次一个地就地添加到
    inventory 中。函数应当返回修改后的 inventory。
    
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
    """如果 t 包含一个值为 'berry'
    的节点则返回 True，否则返回 False。

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
    """返回树中条目的数量。
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
    """返回一棵树，它包含 t 的所有节点以及一条标签为 p 的路径。

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
    """产出严格递增的可迭代对象 incr_a 和 incr_b 的元素，
    并去除重复。假设 incr_a 和 incr_b 没有重复。
    incr_a 或 incr_b 可能是无限序列，也可能不是。

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
    以列表的形式产出从 t 的根到标签为
    target 的节点的所有可能路径。

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
    你不需要理解这段代码。
    >>> midsem_survey(passphrase)
    '2bf925d47c03503d3ebe5a6fc12d479b8d12f14c0494b43deba963a0'
    """
    import hashlib
    return hashlib.sha224(p.encode('utf-8')).hexdigest()



# 树数据抽象

def tree(label, branches=[]):
    """用给定的标签值和分支列表构造一棵树。"""
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)

def label(tree):
    """返回树的标签值。"""
    return tree[0]

def branches(tree):
    """返回给定树的分支列表。"""
    return tree[1:]

def is_tree(tree):
    """如果给定的树是一棵树则返回 True，否则返回 False。"""
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    """如果给定树的分支列表为空则返回
    True，否则返回 False。
    """
    return not branches(tree)

def print_tree(t, indent=0):
    """打印这棵树的表示，
    其中每个节点缩进的空格数为两个空格乘以其到根的深度。

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
    """返回 t 的副本。仅用于测试目的。

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(label(t), [copy_tree(b) for b in branches(t)])

