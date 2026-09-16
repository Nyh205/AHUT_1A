
from link import *

class SchemeError(Exception):
    """表示 Scheme 程序中错误的异常。"""

# 环境
# #
# 

class Frame:
    """环境框架将 Scheme 符号绑定到 Scheme 值。"""

    def __init__(self, parent):
        """一个空框架，其父框架为 PARENT（可以为 None）。"""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    def define(self, symbol, value):
        """定义 Scheme 符号 SYMBOL 的值为 VALUE。"""
        # BEGIN PROBLEM 1
        "*** YOUR CODE HERE ***"
        # END PROBLEM 1

    def lookup(self, symbol):
        """返回绑定到 SYMBOL 的值。如果找不到 SYMBOL 则报错。"""
        # BEGIN PROBLEM 1
        "*** YOUR CODE HERE ***"
        # END PROBLEM 1
        raise SchemeError('unknown identifier: {0}'.format(symbol))


    def make_child_frame(self, formals, vals):
        """返回一个新的局部框架，其父框架为 SELF，其中 Scheme
        形式参数列表 FORMALS 中的符号绑定到 Scheme
        列表 VALS 中的 Scheme 值。FORMALS 和
        VALS 都用 Link 表示。如果给出的值过多或过少则报错。

        >>> env = Frame(None)
        >>> from scheme_reader import read_line
        >>> formals, expressions = read_line('(a b c)'), read_line('(1 2 3)')
        >>> env.make_child_frame(formals, expressions)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        if len_link(formals) != len_link(vals):
            raise SchemeError('Incorrect number of arguments to function call')
        # BEGIN PROBLEM 8
        "*** YOUR CODE HERE ***"
        # END PROBLEM 8

# 过程
# #
# 

class Procedure:
    """所有 Procedure 类的基类。"""

class BuiltinProcedure(Procedure):
    """一个定义为 Python 函数的 Scheme 过程。"""

    def __init__(self, py_func, need_env=False, name='builtin'):
        self.name = name
        self.py_func = py_func
        self.need_env = need_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

class LambdaProcedure(Procedure):
    """由 lambda 表达式或 define 形式定义的过程。"""

    def __init__(self, formals, body, env):
        """一个过程，其形式参数列表为 FORMALS（一个
        Scheme 列表），其体为 Scheme 列表
        BODY，其父环境以框架 ENV 为起点。"""
        assert isinstance(env, Frame), "env must be of type Frame"

        from scheme_utils import validate_type, scheme_listp
        validate_type(formals, scheme_listp, 0, 'LambdaProcedure')
        validate_type(body, scheme_listp, 1, 'LambdaProcedure')
        self.formals = formals
        self.body = body
        self.env = env

    def __str__(self):
        return str(Link('lambda', Link(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))

class MuProcedure(Procedure):
    """由 mu 表达式定义的过程，具有动态作用域。
     _________________
    < Scheme 很酷！ >
    -----------------
    \   ^__^
             \  (oo)\_______
                (__)\
                )\/\ ||----w
                | ||     ||
    """

    def __init__(self, formals, body):
        """一个过程，其形式参数列表为 FORMALS（一个
        Scheme 列表），定义体为 Scheme 列表 BODY。"""
        self.formals = formals
        self.body = body

    def __str__(self):
        return str(Link('mu', Link(self.formals, self.body)))

    def __repr__(self):
        return 'MuProcedure({0}, {1})'.format(
            repr(self.formals), repr(self.body))
