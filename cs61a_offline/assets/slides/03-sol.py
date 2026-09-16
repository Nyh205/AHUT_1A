def combination(n, initial, combiner, term):
    """
    Returns the result of combining the numbers from 1 to `n` (inclusive)
    repeatedly with the `combiner` and `term` functions. `combiner` is a function that takes
    two arguments and returns a single value, while `term` is a function that takes one argument
    and returns a single value. `initial` is the initial value to start the combination.

    >>> from operator import add, mul
    >>> combination(1, 0, add, lambda x: x + 1)  # (0) + (1+1)
    2
    >>> combination(5, 0, add, lambda x: x + 1)  # (0) + (1+1) + (2+1) + (3+1) + (4+1) + (5+1)
    20
    >>> combination(5, 1, mul, lambda x: x + 1)  # (1) * (1+1) * (2+1) * (3+1) * (4+1) * (5+1)
    720
    >>> combination(5, 0, add, lambda x: x * x)  # (0) + 1*1 + 2*2 + 3*3 + 4*4 + 5*5
    55
    >>> combination(5, 1, mul, lambda x: x * x)  # (1) * 1*1 * 2*2 * 3*3 * 4*4 * 5*5
    14400
    """
    i = 1
    total = initial
    while i <= n:
        total = combiner(total, term(i))
        i += 1
    return total


def multiply_triple(x):
    """
    Using only functions with a single argument,
    implement multiply_triple so that you can use it to
    return the product of 3 numbers x, y, and z.

    >>> multiply_triple(1)(2)(3)
    6
    >>> multiply_triple(2)(3)(4)
    24
    >>> multiply_triple(10)(5)(7)
    350
    """
    def outer(y):
        def inner(z):
            return x * y * z
        return inner
    return outer

    # ALTERNATE SOLUTION
    return lambda y: lambda z: x * y * z
