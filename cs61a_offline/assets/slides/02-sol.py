def add_all_even_div_three(n):
    """
    Return the sum of all even numbers from 1 to n that are divisible by 3.

    >>> add_all_even_div_three(10) # 6
    6
    >>> add_all_even_div_three(20) # 6 + 12 + 18
    36
    >>> add_all_even_div_three(30) # 6 + 12 + 18 + 24 + 30
    90
    """
    i = 1
    total = 0
    while i <= n:
        if i % 2 == 0 and i % 3 == 0:
            total += i
        i += 1
    return total


def fizzbuzz(n):
    """
    Print the numbers from 1 to n, replacing:
    - multiples of 3 with "fizz"
    - multiples of 5 with "buzz", and
    - multiples of both with "fizzbuzz".

    >>> fizzbuzz(1)
    1
    >>> fizzbuzz(3)
    1
    2
    fizz
    >>> fizzbuzz(5)
    1
    2
    fizz
    4
    buzz
    >>> fizzbuzz(15)
    1
    2
    fizz
    4
    buzz
    fizz
    7
    8
    fizz
    buzz
    11
    fizz
    13
    14
    fizzbuzz
    """
    i = 1
    while i <= n:
        if i % 3 == 0 and i % 5 == 0:
            print("fizzbuzz")
        elif i % 3 == 0:
            print("fizz")
        elif i % 5 == 0:
            print("buzz")
        else:
            print(i)
        i += 1


def sum_digits(y):
    """Sum all the digits of y.

    >>> sum_digits(10) # 1 + 0 = 1
    1
    >>> sum_digits(4224) # 4 + 2 + 2 + 4 = 12
    12
    >>> sum_digits(1234567890)
    45
    >>> a = sum_digits(123) # make sure that you are using return rather than print
    >>> a
    6
    """
    total = 0
    while y > 0:
        digit = y % 10
        total += digit
        y //= 10
    return total
