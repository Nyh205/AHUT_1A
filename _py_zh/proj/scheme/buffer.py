"""buffer 模块协助遍历行和词元。"""

import math

class Buffer:
    """Buffer 提供了一种跨行访问词元序列的方式。

    它的构造函数接受一个迭代器，称为 "the
    source"，每次被查询时返回下一行词元作为列表，
    或返回 None 表示数据结束。

    Buffer 实际上会连接从其 source 返回的序列，
    然后通过其 pop_first() 方法一次提供一个元素，
    只在需要时才调用 source 获取更多元素序列。

    此外，Buffer 提供了一个 current
    方法，用于查看下一个将要提供的元素，而不越过它。

    __str__ 方法打印目前读取到的所有词元，
    直到当前行的末尾，并用 >> 标记当前词元。

    >>> buf = Buffer(iter([['(', '+'], [15], [12, ')']]))
    >>> buf.pop_first()
    '('
    >>> buf.pop_first()
    '+'
    >>> buf.current()
    15
    >>> buf.current()   # Calling current twice should not change buf
    15
    >>> buf.pop_first()
    15
    >>> buf.current()
    12
    >>> buf.pop_first()
    12
    >>> buf.pop_first()
    ')'
    >>> buf.pop_first()  # returns None
    """

    def __init__(self, source):
        """
        根据给定的 source 初始化一个 Buffer 实例。
        """
        self.index = 0
        self.source = source
        self.current_line = ()
        self.current()

    def pop_first(self):
        """从 self 中移除下一个元素并返回它。如果
        self 已耗尽它的 source，则返回 None。"""
        current = self.current()
        self.index += 1
        return current

    def current(self):
        """返回当前元素，如果不存在则返回 None。"""
        while not self.more_on_line():
            try:
                self.index = 0
                self.current_line = next(self.source)
            except StopIteration:
                self.current_line = ()
                return None
        return self.current_line[self.index]

    def more_on_line(self):
        return self.index < len(self.current_line)

    def end_of_line(self):
        return self.current() is None


# 尝试导入 readline 以支持交互式历史记录
try:
    import readline
except:
    pass

class InputReader:
    """InputReader 是一个可迭代对象，用于提示用户输入。"""
    def __init__(self, prompt):
        self.prompt = prompt

    def __iter__(self):
        while True:
            yield input(self.prompt)
            self.prompt = ' ' * len(self.prompt)

class LineReader:
    """LineReader 是一个可迭代对象，在提示后打印各行。"""
    def __init__(self, lines, prompt, comment=";"):
        self.lines = lines
        self.prompt = prompt
        self.comment = comment

    def __iter__(self):
        while self.lines:
            line = self.lines.pop(0).strip('\n')
            if (self.prompt is not None and line != "" and
                not line.lstrip().startswith(self.comment)):
                print(self.prompt + line)
                self.prompt = ' ' * len(self.prompt)
            yield line
        raise EOFError