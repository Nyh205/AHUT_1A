def sum_odd_squares_iterative(n: int) -> int:
    """
    Returns the sum of all the digits of non-negative integer n,
    except for digits in odd positions
    (starting with position 0 as the rightmost digit and moving left),
    square the digit. Implement this iteratively.

    >>> sum_odd_squares_iterative(5)
    5
    >>> sum_odd_squares_iterative(123) # 1 + (2*2) + 3 = 1 + 4 + 3 = 8
    8
    >>> sum_odd_squares_iterative(243580) # (2*2) + 4 + (3*3) + 5 + (8*8) + 0 = 4 + 4 + 9 + 5 + 64 + 0 = 86
    86
    """
    position = _____
    total = _____
    while _____:
        digit = _____
        if _____:
            total += _____
        else:
            total += _____
        n = _____
        position += _____
    return total


def sum_odd_squares_recursive(n: int) -> int:
    """
    Returns the sum of all the digits of non-negative integer n,
    except for digits in odd positions
    (starting with position 0 as the rightmost digit and moving left),
    square the digit. Implement this recursively.

    >>> sum_odd_squares_recursive(5)
    5
    >>> sum_odd_squares_recursive(123) # 1 + (2*2) + 3 = 1 + 4 + 3 = 8
    8
    >>> sum_odd_squares_recursive(243580) # (2*2) + 4 + (3*3) + 5 + (8*8) + 0 = 4 + 4 + 9 + 5 + 64 + 0 = 86
    86
    """
    def helper(n: int, is_odd: bool) -> int:
        if _____:
            return _____
        elif is_odd:
            return _____ + helper(_____, _____)
        else:
            return _____ + helper(_____, _____)
    return helper(_____, _____)


def count_stairs(n: int) -> int:
    """You are walking up n stairs and you may either take 1 step or 2 steps as you go.
    How many different ways can you reach the top?

    >>> count_stairs(3) # take 2 then 1; 1 then 2; OR 1, 1, 1
    3
    >>> count_stairs(2) # take 2 steps OR take 1 step twice
    2
    >>> count_stairs(4)
    5
    """
    # YOUR CODE HERE


def mario_number(level: int) -> int:
    """
    >>> mario_number(10101) # jump, jump
    1
    >>> mario_number(11101) # Left to right: step, step, jump OR jump, jump
    2
    >>> mario_number(100101)
    0
    """
    # YOUR CODE HERE
