SOURCE_FILE = __file__


def num_eights(num: int) -> int:
    """返回 8 作为 num 的数字出现的次数。

    >>> num_eights(3)
    0
    >>> num_eights(8)
    1
    >>> num_eights(88888888)
    8
    >>> num_eights(2638)
    1
    >>> num_eights(86380)
    2
    >>> num_eights(12345)
    0
    >>> num_eights(8782089)
    3
    >>> from construct_check import check
    >>> # ban all assignment statements
    >>> check(SOURCE_FILE, 'num_eights',
    ...       ['Assign', 'AnnAssign', 'AugAssign', 'NamedExpr', 'For', 'While'])
    True
    """
    if num % 10 == 8:
        return 1 + num_eights(num // 10)
    elif num < 10:
        return 0
    else:
        return num_eights(num // 10)


def digit_distance(num: int) -> int:
    """确定 num 的数字距离。

    >>> digit_distance(3)
    0
    >>> digit_distance(777) # 0 + 0
    0
    >>> digit_distance(314) # 2 + 3
    5
    >>> digit_distance(31415926535) # 2 + 3 + 3 + 4 + ... + 2
    32
    >>> digit_distance(3464660003)  # 1 + 2 + 2 + 2 + ... + 3
    16
    >>> from construct_check import check
    >>> # ban all loops
    >>> check(SOURCE_FILE, 'digit_distance',
    ...       ['For', 'While'])
    True
    """
    if num < 10:
        return 0
    return abs(num % 10 - (num // 10) % 10) + digit_distance(num // 10)

# 另一种解法 1
def digit_distance_alt(num):
    def helper(prev, num):
        if num == 0:
            return 0
        dist = abs(prev - num % 10)
        return dist + helper(num % 10, num // 10)
    return helper(num % 10, num // 10)

# 另一种解法 2
def digit_distance_alt_2(num):
    def helper(dist, prev, num):
        if num == 0:
            return dist
        dist += abs(prev - num % 10)
        prev = num % 10
        num //= 10
        return helper(dist, prev, num)
    return helper(0, num % 10, num // 10)


def interleaved_sum(num: int, f_odd, f_even) -> int:
    """计算和 f_odd(1) + f_even(2)
    + f_odd(3) + ...，直到 num。

    >>> identity = lambda x: x
    >>> square = lambda x: x * x
    >>> triple = lambda x: x * 3
    >>> interleaved_sum(5, identity, square) # 1   + 2*2 + 3   + 4*4 + 5
    29
    >>> interleaved_sum(5, square, identity) # 1*1 + 2   + 3*3 + 4   + 5*5
    41
    >>> interleaved_sum(4, triple, square)   # 1*3 + 2*2 + 3*3 + 4*4
    32
    >>> interleaved_sum(4, square, triple)   # 1*1 + 2*3 + 3*3 + 4*3
    28
    >>> from construct_check import check
    >>> check(SOURCE_FILE, 'interleaved_sum', ['While', 'For', 'Mod']) # ban loops and %
    True
    >>> check(SOURCE_FILE, 'interleaved_sum', ['BitAnd', 'BitOr', 'BitXor']) # ban bitwise operators, don't worry about these if you don't know what they are
    True
    """
    def sum_from(k):
        if k > num:
            return 0
        elif k == num:
            return f_odd(k)
        else:
            return f_odd(k) + f_even(k+1) + sum_from(k + 2)
    return sum_from(1)


def next_smaller_dollar(bill: int) -> int:
    """按顺序返回下一个更小的纸币。"""
    if bill == 100:
        return 50
    if bill == 50:
        return 20
    if bill == 20:
        return 10
    elif bill == 10:
        return 5
    elif bill == 5:
        return 1

def count_dollars(sum_needed: int) -> int:
    """返回找零的方式数。

    >>> count_dollars(15)  # 15 $1 bills, 10 $1 & 1 $5 bills, ... 1 $5 & 1 $10 bills
    6
    >>> count_dollars(10)  # 10 $1 bills, 5 $1 & 1 $5 bills, 2 $5 bills, 10 $1 bills
    4
    >>> count_dollars(20)  # 20 $1 bills, 15 $1 & $5 bills, ... 1 $20 bill
    10
    >>> count_dollars(45)  # How many ways to make change for 45 dollars?
    44
    >>> count_dollars(100) # How many ways to make change for 100 dollars?
    344
    >>> count_dollars(200) # How many ways to make change for 200 dollars?
    3274
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(SOURCE_FILE, 'count_dollars', ['While', 'For'])
    True
    """
    def constrained_count(sum_needed, largest_bill):
        if sum_needed == 0:
            return 1
        if sum_needed < 0:
            return 0
        if largest_bill == None:
            return 0
        without_dollar_bill = constrained_count(sum_needed, next_smaller_dollar(largest_bill))
        with_dollar_bill = constrained_count(sum_needed - largest_bill, largest_bill)
        return without_dollar_bill + with_dollar_bill
    return constrained_count(sum_needed, 100)


def shuffle(s: list) -> list:
    """返回一个打乱后的列表，它把 s 的两半交错排列。

    >>> shuffle(range(6))
    [0, 3, 1, 4, 2, 5]
    >>> letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    >>> shuffle(letters)
    ['a', 'e', 'b', 'f', 'c', 'g', 'd', 'h']
    >>> shuffle(shuffle(letters))
    ['a', 'c', 'e', 'g', 'b', 'd', 'f', 'h']
    >>> letters  # Original list should not be modified
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    """
    assert len(s) % 2 == 0, 'len(seq) must be even'
    half = len(s) // 2
    shuffled = []
    for i in range(half):
        shuffled.append(s[i])
        shuffled.append(s[half + i])
    return shuffled


def deep_map(f, s: list) -> list:
    """把嵌套列表 s 中的所有非列表元素 x 替换为 f(x)。

    >>> six = [1, 2, [3, [4], 5], 6]
    >>> deep_map(lambda x: x * x, six)
    >>> six
    [1, 4, [9, [16], 25], 36]
    >>> # Check that you're not making new lists
    >>> s = [3, [1, [4, [1]]]]
    >>> s1 = s[1]
    >>> s2 = s1[1]
    >>> s3 = s2[1]
    >>> deep_map(lambda x: x + 1, s)
    >>> s
    [4, [2, [5, [2]]]]
    >>> s1 is s[1]
    True
    >>> s2 is s1[1]
    True
    >>> s3 is s2[1]
    True
    """
    for i in range(len(s)):
        if type(s[i]) == list:
            deep_map(f, s[i])
        else:
            s[i] = f(s[i])


def next_larger_dollar(bill: int) -> int:
    """按顺序返回下一个更大的纸币。"""
    if bill == 1:
        return 5
    elif bill == 5:
        return 10
    elif bill == 10:
        return 20
    elif bill == 20:
        return 50
    elif bill == 50:
        return 100

def count_dollars_upward(sum_needed: int) -> int:
    """返回使用纸币找零的方式数。

    >>> count_dollars_upward(15)  # 15 $1 bills, 10 $1 & 1 $5 bills, ... 1 $5 & 1 $10 bills
    6
    >>> count_dollars_upward(10)  # 10 $1 bills, 5 $1 & 1 $5 bills, 2 $5 bills, 10 $1 bills
    4
    >>> count_dollars_upward(20)  # 20 $1 bills, 15 $1 & $5 bills, ... 1 $20 bill
    10
    >>> count_dollars_upward(45)  # How many ways to make change for 45 dollars?
    44
    >>> count_dollars_upward(100) # How many ways to make change for 100 dollars?
    344
    >>> count_dollars_upward(200) # How many ways to make change for 200 dollars?
    3274
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(SOURCE_FILE, 'count_dollars_upward', ['While', 'For'])
    True
    """
    def constrained_count(sum_needed, smallest_bill):
        if sum_needed == 0:
            return 1
        if sum_needed < 0:
            return 0
        if smallest_bill == None:
            return 0
        without_dollar_bill = constrained_count(sum_needed, next_larger_dollar(smallest_bill))
        with_dollar_bill = constrained_count(sum_needed - smallest_bill, smallest_bill)
        return without_dollar_bill + with_dollar_bill
    return constrained_count(sum_needed, 1)

