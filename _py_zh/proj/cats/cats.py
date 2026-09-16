"""打字测试实现"""

from utils import (
    lower,
    split,
    remove_punctuation,
    lines_from_file,
    count,
    deep_convert_to_tuple,
)
from ucb import main, interact, trace
from datetime import datetime
import random


# 阶段
# 1
# #


def pick(paragraphs: list[str], select, k: int) -> str:
    """返回 PARAGRAPHS 中第 K 个使 SELECT 函数返回
    True 的段落。如果这样的段落少于 K 个，返回空字符串。

    参数：paragraphs：
    表示段落的字符串列表 select：
    对其标准得到满足的段落返回 True
    的函数 k：一个整数，表示要返回哪个段落

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    # END PROBLEM 1


def about(keywords: list[str]):
    """返回一个函数，它接收一个段落并返回该段落是否包含
    keywords 中的某个词。

    参数：keywords：
    关键词的列表

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in keywords]), "keywords should be lowercase."

    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    # END PROBLEM 2


def accuracy(entered: str, source: str) -> float:
    """返回 ENTERED 与 SOURCE
    中对应单词相比的准确率（正确输入的单词所占百分比）。

    参数：entered：
    一个可能包含拼写错误的字符串
    source：一个没有错误的模板字符串

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    entered_words = split(entered)
    source_words = split(source)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    # END PROBLEM 3


def wpm(entered: str, elapsed: int) -> float:
    """返回 ENTERED 字符串的每分钟词数（WPM）。

    参数：entered：
    输入的字符串 elapsed：
    以秒为单位的时间量

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, "Elapsed time must be positive"
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    # END PROBLEM 4


# 阶段
# 4（EC）
# #


def memo(f):
    """一个通用的记忆化装饰器。"""
    cache = {}

    def memoized(*args):
        immutable_args = deep_convert_to_tuple(args)  # 把 *args 转换为元组表示
        if immutable_args not in cache:
            result = f(*immutable_args)
            cache[immutable_args] = result
            return result
        return cache[immutable_args]

    return memoized


def memo_diff(diff_function):
    """一个记忆化函数。"""
    cache = {}

    def memoized(entered, source, limit):
        # BEGIN PROBLEM EC
        "*** YOUR CODE HERE ***"
        # END PROBLEM EC

    return memoized


# 阶段
# 2
# #


def autocorrect(entered_word: str, word_list: list[str], diff_function, limit: int) -> str:
    """返回 WORD_LIST 中根据 DIFF_FUNCTION
    与 ENTERED_WORD 差异最小的元素。如果有多个单词并列差异最小，
    返回在 WORD_LIST 中最靠前的那个。如果最小的差异大于
    LIMIT，则返回 ENTERED_WORD。

    参数：entered_word：
    一个可能包含拼写错误的单词字符串
    word_list：表示源单词的字符串列表
    diff_function：
    量化两个单词之间差异的函数 limit：一个数字

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    # END PROBLEM 5


def furry_fixes(entered: str, source: str, limit: int) -> int:
    """一个用于自动更正的 diff 函数，它确定需要替换
    ENTERED 中的多少个字母才能得到 SOURCE，
    然后把这个值加上它们长度的差值并返回结果。

    参数：entered：起始单词
    source：表示期望目标词的字符串
    limit：
    一个表示必须改变的字符数上限的数字

    >>> big_limit = 10
    >>> furry_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> furry_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> furry_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> furry_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> furry_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    assert False, 'Remove this line'
    # END PROBLEM 6


def minimum_mewtations(entered: str, source: str, limit: int) -> int:
    """一个用于自动更正的 diff 函数，它计算从 ENTERED 到 SOURCE 的编辑距离。
    这个函数接收字符串 ENTERED、字符串 SOURCE 和一个数字 LIMIT。

    参数：entered：起始单词
    source：表示期望目标词的字符串
    limit：
    一个表示编辑次数上限的数字

    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    assert False, 'Remove this line'
    if ___________: # 基本情况应放在这里，你可以根据需要添加更多基本情况。
        # BEGIN
        "*** YOUR CODE HERE ***"
        # END
    # 递归情况应放在这下面
    if ___________: # 可以随意删除或添加其它情况
        # BEGIN
        "*** YOUR CODE HERE ***"
        # END
    else:
        add = ... # 填写这几行
        remove = ...
        substitute = ...
        # BEGIN
        "*** YOUR CODE HERE ***"
        # END


# 忽略下面这一行
minimum_mewtations = count(minimum_mewtations)


def final_diff(entered: str, source: str, limit: int) -> int:
    """一个 diff 函数，接收字符串 ENTERED、字符串 SOURCE
    和一个数字 LIMIT。如果你实现这个函数，它就会被使用。"""
    assert False, "Remove this line to use your final_diff function."


FINAL_DIFF_LIMIT = 6  # 用你的 LIMIT 替换这里


# 阶段
# 3
# #


def report_progress(entered: list[str], source: list[str], user_id: int, upload) -> float:
    """把你的 id 和目前进度的报告上传到多人服务器。
    返回目前的进度。

    参数：entered：目前输入的单词的列表
    source：打字源中单词的列表
    user_id：一个表示当前用户
    id 的数字 upload：
    用于把进度上传到多人服务器的函数

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> entered = ['how', 'are', 'you']
    >>> source = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(entered, source, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], source, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    # END PROBLEM 8


def time_per_word(words: list[str], timestamps_per_player: list[list[int]]) -> dict:
    """返回一个字典 {'words': words, 'times':
    times}，其中 times 是一个列表的列表，
    存储每位玩家输入 words 中每个单词所花的时间。

    参数：words：单词的列表，
    按输入顺序排列。timestamps
    _per_player：时间戳的列表的列表，
    包含每位玩家开始打字的时间，
    其后是每位玩家打完每个单词的时间。

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> result = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> result['words']
    ['collar', 'plush', 'blush', 'repute']
    >>> result['times']
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    ts_by_player = timestamps_per_player  # 一个更短的名字（为了方便）
    # BEGIN PROBLEM 9
    times = []  # 你可以删除这一行
    # END PROBLEM 9
    return {'words': words, 'times': times}


def fastest_words(words_and_times: dict) -> list[list[str]]:
    """返回一个列表的列表，指出每位玩家输入最快的单词。
    如果出现平局，索引较小的玩家被认为是输入最快的那个。

    参数：words_and_times：一个字典
    {'words': words, 'times':
    times}，其中 words 是已输入单词的列表，
    times 是每位玩家输入每个单词所花时间的列表的列表。

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words({'words': ['Just', 'have', 'fun'], 'times': [p0, p1]})
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    check_words_and_times(words_and_times)  # 验证输入格式是否正确
    words, times = words_and_times['words'], words_and_times['times']
    pl_idxs = range(len(times))  # 为每位玩家包含一个 *索引*
    w_idxs = range(len(words))    # 为每个单词包含一个 *索引*
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    # END PROBLEM 10


def check_words_and_times(words_and_times):
    """检查 words_and_times 是一个 {'words': words, 'times':
    times} 字典，其中 times 的每个元素都是与 words 长度相同的数字列表。
    """
    assert 'words' in words_and_times and 'times' in words_and_times and len(words_and_times) == 2
    words, times = words_and_times['words'], words_and_times['times']
    assert all([type(w) == str for w in words]), "words should be a list of strings"
    assert all([type(t) == list for t in times]), "times should be a list of lists"
    assert all([isinstance(i, (int, float)) for t in times for i in t]), "times lists should contain numbers"
    assert all([len(t) == len(words) for t in times]), "There should be one word per time."


def get_time(times, player_num, word_index):
    """给定由 time_per_word 返回的时间的列表的列表，返回
    player_num 输入 word_index 处的单词所花的时间。"""
    num_players = len(times)
    num_words = len(times[0])
    assert word_index < len(times[0]), f"word_index {word_index} outside of 0 to {num_words-1}"
    assert player_num < len(times), f"player_num {player_num} outside of 0 to {num_players-1}"
    return times[player_num][word_index]


enable_multiplayer = False  # 准备好开始比赛时改为 True。

# 命令行界面
# #
# 


def run_typing_test(topics):
    """在命令行上测量打字速度和准确率。"""
    paragraphs = lines_from_file("data/sample_paragraphs.txt")
    random.shuffle(paragraphs)
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print("No more paragraphs about", topics, "are available.")
            return
        print("Type the following paragraph and then press enter/return.")
        print("If you only type part of it, you will be scored only on that part.\n")
        print(source)
        print()

        start = datetime.now()
        entered = input()
        if not entered:
            print("Goodbye.")
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print("Words per minute:", wpm(entered, elapsed))
        print("Accuracy:        ", accuracy(entered, source))

        print("\nPress enter/return for the next paragraph or type q to quit.")
        if input().strip() == "q":
            return
        i += 1


@main
def run(*args):
    """读取命令行参数并调用相应的函数。"""
    import argparse

    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument("topic", help="Topic word", nargs="*")
    parser.add_argument("-t", help="Run typing test", action="store_true")

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)