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
    # YOUR CODE HERE


# Uncomment this when you're ready to work on it
# (In VS Code you can do this by highlighting all the lines below and pressing Cmd/Ctrl + forward slash)
# def luhn_sum(n: int) -> int:
#     """
#     >>> luhn_sum(5)
#     5
#     >>> luhn_sum(52)  # (5*2) + 2 --> (1+0) + 2 --> 3
#     3
#     >>> luhn_sum(138743)  # from lecture slides
#     30
#     >>> luhn_sum(17893729974)  # https://en.wikipedia.org/wiki/Luhn_algorithm#Example_for_computing_check_digit
#     60
#     """
#     if n < 10:
#         return ________
#     else:
#         last = ________
#         all_but_last = ________
#         return ________ + ________(________)

# def luhn_sum_double(n: int) -> int:
#     last = ________
#     all_but_last = ________
#     luhn_digit = ________(________)
#     if n < 10:
#         return ________
#     else:
#         return ________ + ________(________)
