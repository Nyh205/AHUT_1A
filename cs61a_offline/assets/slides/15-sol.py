class Tree:
    """A tree has a label and a list of branches.

    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> t.label
    3
    >>> t.branches[0].label
    2
    >>> t.branches[1].is_leaf()
    True
    """
    def __init__(self, label, branches=[]):
        self.label = label
        for branch in branches:
            assert isinstance(branch, Tree)
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(repr(self.label), branch_str)

    def __str__(self):
        return '\n'.join(self.indented())

    def indented(self):
        lines = []
        for b in self.branches:
            for line in b.indented():
                lines.append('  ' + line)
        return [str(self.label)] + lines

    # NOTE: This method is new and custom for practice problem 2
    # It is not normally part of the Tree class
    def __iter__(self):
        return TreeIterator(self)


def height(t: Tree) -> int:
    """
    Returns the height of a Tree `t`
    (recall that the height of a tree is the depth of the lowest leaf)

    >>> t = Tree(1)
    >>> height(t)
    0
    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> height(t)
    2
    >>> t = Tree(1, [Tree(2, [Tree(3, [Tree(4), Tree(5)])]), Tree(6)])
    >>> height(t)
    3
    """
    if t.is_leaf():
        return 0
    return 1 + max([height(b) for b in t.branches])


class TreeIterator:
    """
    An iterator that returns the elements of a Tree `t`
    when performing a level-order traversal (aka breadth-first search).

    >>> t = Tree(1)
    >>> t_iter = iter(t)
    >>> next(t_iter)
    1
    >>> next(t_iter)
    Traceback (most recent call last):
      ...
    StopIteration

    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> t_iter = iter(t)
    >>> list(t_iter)
    [3, 2, 4, 5]

    >>> t = Tree(1, [Tree(2, [Tree(3, [Tree(4), Tree(5)])]), Tree(6)])
    >>> t_iter = iter(t)
    >>> list(t_iter)
    [1, 2, 6, 3, 4, 5]
    """
    def __init__(self, t: Tree):
        self.queue = [t]

    def __iter__(self):
        return self

    def __next__(self):
        if self.queue:
            curr_node = self.queue.pop(0)
            for b in curr_node.branches:
                self.queue.append(b)
            return curr_node.label
        else:
            raise StopIteration


def reveal_winner(t: Tree):
    """
    >>> t = Tree("W", [
    ...     Tree("W", [Tree("W", [Tree("W"), Tree("L")]),
    ...                Tree("L", [Tree("W"), Tree("L")])]),
    ...     Tree("L", [Tree("L", [Tree("W"), Tree("L")]),
    ...                Tree("W", [Tree("L"), Tree("W")])])
    ... ])
    >>> gen = reveal_winner(t)

    >>> print(next(gen))
    W
      W
        W
          W
        L
          W
      L
        L
          W
        W
          W

    >>> print(next(gen))
    W
      W
        W
          W
      L
        W
          W

    >>> print(next(gen))
    W
      W
        W
          W

    >>> next(gen)
    Traceback (most recent call last):
      ...
    StopIteration
    """

    def prune_lowest_losers(t: Tree):
        """
        Return (new_tree, changed), where:

        (1) new_tree is the pruned version of t,
            or None if t is removed
        (2) changed is True if t itself or a lowest losing subtree was pruned,
            and False otherwise
        """
        # BASE CASE: If the current tree is a leaf representing a loss, do we prune it or not?
        # Also remember that we should always return None or a new Tree!
        if t.is_leaf():
            if t.label == "L":
                return None, True
            return Tree(t.label), False

        # RECURSIVE CASE (i): For a non-leaf tree, we recursively prune each branch. Guiding questions:
        # What does it mean if a recursive call returns `None` for `new_tree`?
        #     In that case, should the new branch be included in `new_branches`?
        # What does it mean if a recursive call returned `False` for `changed`?
        new_branches = []
        changed = False

        for b in t.branches:
            new_b, child_changed = prune_lowest_losers(b)
            if new_b is not None:
                new_branches.append(new_b)
            changed = changed or child_changed

        # RECURSIVE CASE (ii): At this point, we should have a copy of the branches of t
        # but recursively pruned. Now we need to consider the root label itself.
        # Remember that we want to remove the LOWEST LOSING subtree. Even if no pruning
        # happened in the current tree's children/descendants, when do we prune the current tree?
        if t.label == "L" and not changed:
            return None, True

        # RECURSIVE CASE (iii): If the condition in (ii) doesn't happen, what are the
        # 2 values that need to be returned? Again, remember we always return None or a new Tree.
        return Tree(t.label, new_branches), changed

    current = t
    changed = True
    while changed:
        current, changed = prune_lowest_losers(current)
        if changed:
            # Remember that `prune_lowest_lowers`, our recursive helper function,
            # returns the result of one pruning step at a time. Therefore, which variable holds
            # the most recently pruned tree?
            yield current
