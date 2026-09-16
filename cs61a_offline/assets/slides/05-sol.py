def sum_digits(n: int) -> int:
    """
    Returns the sum of the digits of a non-negative integer n.

    >>> sum_digits(0)
    0
    >>> sum_digits(5)
    5
    >>> sum_digits(123)
    6
    >>> sum_digits(3094153)
    25
    """
    # alternative base cases
    # if n == 0:
    # if n <= 9:
    if n < 10:
        return n
    else:
        last = n % 10
        all_but_last = n // 10
        return sum_digits(all_but_last) + last

def luhn_sum(n: int) -> int:
    """
    >>> luhn_sum(5)
    5
    >>> luhn_sum(52)  # (5*2) + 2 --> (1+0) + 2 --> 3
    3
    >>> luhn_sum(138743)  # from lecture slides
    30
    >>> luhn_sum(17893729974)  # https://en.wikipedia.org/wiki/Luhn_algorithm#Example_for_computing_check_digit
    60
    """
    if n < 10:
        return n
    else:
        last = n % 10
        all_but_last = n // 10
        return last + luhn_sum_double(all_but_last)

def luhn_sum_double(n: int) -> int:
    last = n % 10
    all_but_last = n // 10
    luhn_digit = sum_digits(last * 2)
    if n < 10:
        return luhn_digit
    else:
        return luhn_digit + luhn_sum(all_but_last)
