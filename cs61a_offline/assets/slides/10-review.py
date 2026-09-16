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


def print_treeA(tree):
    print(label(tree))
    for b in branches(tree):
        print_treeA(b)

def print_treeB(tree):
    for b in branches(tree):
        print(label(tree))
        print_treeB(b)

def print_treeC(tree):
    for b in branches(tree):
        print_treeC(b)
    print(label(tree))

