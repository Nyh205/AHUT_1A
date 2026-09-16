# Lab02 工具

UPPERCASE_SHIFT = 65
LOWERCASE_SHIFT = 97
ALPHA_SHIFT = 26

def letter_to_num(letter):
    """把所有字母转换为 0-51 的数字，其中小写字母映射到
    0-25，大写字母映射到 26-51
    >>> letter_to_num('a')
    0
    >>> letter_to_num('z')
    25
    >>> letter_to_num('A')
    26
    >>> letter_to_num('Z')
    51
    """
    if letter.isupper():
        return ord(letter)-UPPERCASE_SHIFT + ALPHA_SHIFT
    return ord(letter)-LOWERCASE_SHIFT

def num_to_letter(num):
    """把 0-51 的数字转换为字母
    >>> num_to_letter(0)
    'a'
    >>> num_to_letter(25)
    'z'
    >>> num_to_letter(26)
    'A'
    >>> num_to_letter(51)
    'Z'
    """
    try:
        num = int(num)
    except ValueError:
        return ' '
    num = num % 52
    if num > 25:
        return chr(num - ALPHA_SHIFT + UPPERCASE_SHIFT)
    return chr(num + LOWERCASE_SHIFT)

def mirror_letter(letter):
    """返回字母表中另一侧
    同一位置上的字母。

    >>> mirror_letter('a')
    'z'
    >>> mirror_letter('z')
    'a'
    >>> mirror_letter('B')
    'Y'
    >>> mirror_letter('C')
    'X'
    """
    if letter.isupper():
        return chr(155 - ord(letter))
    return chr(219 - ord(letter))


def looper(f, delimiter=''):
    """返回一个把函数 f 应用到可迭代对象的每个元素上的函数。"""
    return lambda iterable: delimiter.join([str(f(i)) for i in iterable])



def composite_identity(f, g):
    """
    返回一个带有一个参数 x 的函数，如果 f(g(x)
    ) 等于 g(f(x)) 就返回 True。你可以假设
    g(x) 的结果是 f 的有效输入，反之亦然。

    >>> add_one = lambda x: x + 1        # adds one to x
    >>> square = lambda x: x**2          # squares x [returns x^2]
    >>> b1 = composite_identity(square, add_one)
    >>> b1(0)                            # (0 + 1) ** 2 == 0 ** 2 + 1
    True
    >>> b1(4)                            # (4 + 1) ** 2 != 4 ** 2 + 1
    False
    """
    "*** YOUR CODE HERE ***"


def sum_digits(y):
    """返回非负整数 y 的数字之和。"""
    total = 0
    while y > 0:
        total, y = total + y % 10, y // 10
    return total

def is_prime(n):
    """返回正整数 n 是否为质数。"""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True

def count_cond(condition):
    """返回一个带有一个参数 N 的函数，它统计从 1 到
    n 中所有满足双参数谓词函数 Condition
    的数，其中传给 Condition 的第一个参数是
    n，第二个参数是从 1 到 n 的那个数。

    >>> count_fives = count_cond(lambda n, i: sum_digits(n * i) == 5)
    >>> count_fives(10)   # 50 (10 * 5)
    1
    >>> count_fives(50)   # 50 (50 * 1), 500 (50 * 10), 1400 (50 * 28), 2300 (50 * 46)
    4

    >>> is_i_prime = lambda n, i: is_prime(i) # need to pass 2-argument function into count_cond
    >>> count_primes = count_cond(is_i_prime)
    >>> count_primes(2)    # 2
    1
    >>> count_primes(3)    # 2, 3
    2
    >>> count_primes(4)    # 2, 3
    2
    >>> count_primes(5)    # 2, 3, 5
    3
    >>> count_primes(20)   # 2, 3, 5, 7, 11, 13, 17, 19
    8
    """
    "*** YOUR CODE HERE ***"


from operator import add, sub

def caesar_generator(num, op):
    """返回一个单参数的凯撒密码函数。该函数应当使用操作
    op（add 或 sub），按整数数量
    num 来“旋转”一个字母。

    你可以使用提供的 letter_to_num 和
    num_to_letter 函数，它们会把所有小写字母 a-z
    映射到 0-25，把所有大写字母 A-Z 映射到 26-51。

    >>> letter_to_num('a')
    0
    >>> letter_to_num('c')
    2
    >>> num_to_letter(3)
    'd'

    >>> caesar2 = caesar_generator(2, add)
    >>> caesar2('a')
    'c'
    >>> brutus3 = caesar_generator(3, sub)
    >>> brutus3('d')
    'a'
    """
    "*** YOUR CODE HERE ***"
    return ______


def is_palindrome(n):
    """
    填入空白处 _____，
    以检查一个数是否为回文数。

    >>> is_palindrome(12321)
    True
    >>> is_palindrome(42)
    False
    >>> is_palindrome(2015)
    False
    >>> is_palindrome(55)
    True
    """
    x, y = n, 0
    f = lambda: _____
    while x > 0:
        x, y = _____, f()
    return y == n

