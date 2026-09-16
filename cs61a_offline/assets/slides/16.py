class Link:
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '('
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + ')'


def filter_link(f, lnk: Link) -> Link:
    """
    Return a Link that contains only the elements of `x` inside `lnk`
    for which `f(x)` is a truthy value.

    >>> is_odd = lambda x: x % 2 == 1
    >>> lnk = Link(1, Link(2, Link(3, Link(4, Link(5)))))
    >>> filter_link(is_odd, lnk)
    Link(1, Link(3, Link(5)))
    >>> lnk  # no mutation!
    Link(1, Link(2, Link(3, Link(4, Link(5)))))

    >>> short = lambda x: len(x) <= 3
    >>> lnk = Link('bottle', Link('cat', Link('dog', Link('gateway', Link('a')))))
    >>> filter_link(short, lnk)
    Link('cat', Link('dog', Link('a')))
    >>> lnk  # no mutation!
    Link('bottle', Link('cat', Link('dog', Link('gateway', Link('a')))))
    """
    # YOUR CODE HERE

def insert(lnk: Link, index: int, value):
    """
    Mutate `lnk` to insert `value` at `index`.
    Assume that 0 < `index` <= the length of `lnk`.

    >>> lnk = Link('cat', Link('dog', Link('a')))
    >>> insert(lnk, 1, 'fish')
    >>> lnk
    Link('cat', Link('fish', Link('dog', Link('a'))))

    >>> lnk = Link(1, Link(2, Link(3, Link(4, Link(5)))))
    >>> insert(lnk, 3, 'yay')
    >>> lnk
    Link(1, Link(2, Link(3, Link('yay', Link(4, Link(5))))))

    >>> lnk = Link(1, Link(2, Link(3, Link(4, Link(5)))))
    >>> insert(lnk, 5, 6)
    >>> lnk
    Link(1, Link(2, Link(3, Link(4, Link(5, Link(6))))))
    """
    # YOUR CODE HERE
