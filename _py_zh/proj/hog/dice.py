"""模拟掷骰子的函数。

骰子函数不接受参数并返回 1 到 n（含）
之间的一个数，其中 n 是骰子的面数。

公平骰子以相等的概率产生每个可能的结果。已经定义了两个公平骰子
four_sided 和 six_sided，它们由
make_fair_dice 函数生成。

测试骰子是确定性的：
它们总是循环遍历作为参数传入的固定值序列。
测试骰子由 make_test_dice 函数生成。
"""

from random import randint

def make_fair_dice(sides):
    """返回一个骰子，它以相等的概率返回 1 到 SIDES。"""
    assert type(sides) == int and sides >= 1, 'Illegal value for sides'
    def dice():
        return randint(1,sides)
    return dice

four_sided = make_fair_dice(4)
six_sided = make_fair_dice(6)

def make_test_dice(*outcomes):
    """返回一个按确定性循环遍历 OUTCOMES 的骰子。

    >>> dice = make_test_dice(1, 2, 3)
    >>> dice()
    1
    >>> dice()
    2
    >>> dice()
    3
    >>> dice()
    1
    >>> dice()
    2

    这个函数使用了本课程尚未涉及的 Python
    语法/技巧。理解它的最好方式是阅读文档和示例。
    """
    assert len(outcomes) > 0, 'You must supply outcomes to make_test_dice'
    for o in outcomes:
        assert type(o) == int and o >= 1, 'Outcome is not a positive integer'
    index = len(outcomes) - 1
    def dice():
        nonlocal index
        index = (index + 1) % len(outcomes)
        return outcomes[index]
    return dice