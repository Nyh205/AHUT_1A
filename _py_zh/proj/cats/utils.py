"用于文件和字符串操作的实用函数"

import string
from math import sqrt

# 字符串实用函数
# #
# 

def lines_from_file(path):
    """返回一个字符串列表，文件中的每一行对应一个字符串。"""
    with open(path, 'r') as f:
        return [line.strip() for line in f.readlines()]

def remove_punctuation(s):
    """返回一个与 s 内容相同但去除了标点的字符串。

    >>> remove_punctuation("It's a lovely day, don't you think?")
    'Its a lovely day dont you think'
    >>> remove_punctuation("Its a lovely day dont you think")
    'Its a lovely day dont you think'
    """
    punctuation_remover = str.maketrans('', '', string.punctuation)
    return s.strip().translate(punctuation_remover)

def lower(s):
    """返回 s 的小写版本。

    >>> lower("HELLO")
    'hello'
    >>> lower("World")
    'world'
    >>> lower("hello WORLD")
    'hello world'
    """
    return s.lower()

def split(s):
    """返回 s 中包含的单词列表，单词是由空白字符（空格、
    制表符等）分隔的字符序列。

    >>> split("It's a lovely day, don't you think?")
    ["It's", 'a', 'lovely', 'day,', "don't", 'you', 'think?']
    """
    return s.split()

# 键盘布局函数
# #
# 

KEY_LAYOUT = [["1","2","3","4","5","6","7","8","9","0","-","="],
              ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p","[","]"],
              ["a", "s", "d", "f", "g", "h", "j", "k", "l",";","'"],
              ["z", "x", "c", "v", "b", "n", "m",",",".","/"],
              [" "]]

def distance(p1, p2):
    """返回两点之间的欧几里得距离

    两点 (x1, y1) 和 (x2, y2) 之间的欧几里得距离是
    (x1 - x2) ** 2 + (y1 - y2) ** 2 的平方根

    >>> distance((0, 1), (1, 1))
    1.0
    >>> distance((1, 1), (1, 1))
    0.0
    >>> round(distance((4, 0), (0, 4)), 3)
    5.657
    """
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_key_distances():
    """返回一个新的字典，将键对映射到距离。

    字典的每个键是两个字母字符串组成的元组，
    每个值是标准 QWERTY
    键盘上这两个字母之间的欧几里得距离，已归一化

    缩放比例是恒定的，因此距离是两倍的键对，
    其距离值也是两倍。

    >>> distances = get_key_distances()
    >>> distances["a", "a"]
    0.0
    >>> round(distances["a", "d"],3)
    1.367
    >>> round(distances["d", "a"],3)
    1.367
    """
    key_distance = {}

    def compute_pairwise_distances(i, j, d):
        for x in range(len(KEY_LAYOUT)):
            for y in range(len(KEY_LAYOUT[x])):
                l1 = KEY_LAYOUT[i][j]
                l2 = KEY_LAYOUT[x][y]
                d[l1, l2] = distance((i, j), (x, y))

    for i in range(len(KEY_LAYOUT)):
        for j in range(len(KEY_LAYOUT[i])):
            compute_pairwise_distances(i, j, key_distance)

    max_value = max(key_distance.values())
    return {key : value * 8 / max_value for key, value in key_distance.items()}

def count(f):
    """使用变量 call_count
    记录函数 f 被调用的次数

    >>> def factorial(n):
    ...     if n <= 1:
    ...         return 1
    ...     return n * factorial(n - 1)
    >>> factorial = count(factorial)
    >>> factorial(5)
    120
    >>> factorial.call_count
    5
    """
    def counted(*args):
        counted.call_count += 1
        return f(*args)
    counted.call_count = 0
    return counted

# 其他函数
# #
# 

def deep_convert_to_tuple(sequence):
    """深度地将元组转换为列表。
    >>> deep_convert_to_tuple(5)
    5
    >>> deep_convert_to_tuple([2, 'hi'])
    (2, 'hi')
    >>> deep_convert_to_tuple([['These', 'are', 'all'], ['tuples.']])
    (('These', 'are', 'all'), ('tuples.',))
    """
    if isinstance(sequence, list) or isinstance(sequence, tuple):
        return tuple(deep_convert_to_tuple(item) for item in sequence)
    else:
        return sequence