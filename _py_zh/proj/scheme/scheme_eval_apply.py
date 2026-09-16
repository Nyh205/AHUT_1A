import sys

from link import *
from scheme_utils import *
from scheme_reader import read_line
from scheme_builtins import create_global_frame
from ucb import main, trace

# 求值/应用
# #
# 

def scheme_eval(expr, env, _=None): # 可选的第三个参数会被忽略
    """在框架 ENV 中求值 Scheme 表达式 EXPR。

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Link('+', Link(2, Link(2)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # 求值原子
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # 所有非原子表达式都是列表（组合）
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest

    from scheme_forms import SPECIAL_FORMS # 在此导入以避免模块加载时出现循环
    if scheme_symbolp(first) and first in SPECIAL_FORMS:
        return SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"
        # END PROBLEM 3

def scheme_apply(procedure, args, env):
    """在当前环境，即框架 ENV 中，将 Scheme 过程
    PROCEDURE 应用于参数值 ARGS（一个 Scheme 列表）。"""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            "*** YOUR CODE HERE ***"
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        "*** YOUR CODE HERE ***"
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env):
    """在框架 ENV（当前环境）中求值 Scheme 列表
    EXPRESSIONS 中的每个表达式，并返回最后一个的值。

    >>> eval_all(read_line("(1)"), Frame(None))
    1
    >>> eval_all(read_line("(1 2)"), Frame(None))
    2
    """
    # BEGIN PROBLEM 6
    return scheme_eval(expressions.first, env) # 用你自己的代码行替换这里
    # END PROBLEM 6

# 额外挑战：
# 尾递归
# #

class Unevaluated:
    """一个表达式以及要在其中求值该表达式的环境。"""

    def __init__(self, expr, env):
        """要在框架 ENV 中求值的表达式 EXPR。"""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """在 env 中将 procedure 应用于 args；确保结果不是 Unevaluated。"""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """返回 eval 函数的正确尾递归版本。"""
    def optimized_eval(expr, env, tail=False):
        """在框架 ENV 中求值 Scheme 表达式 EXPR。如果 TAIL
        为真，则返回一个包含待进一步求值表达式的 Unevaluated。
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 2
        "*** YOUR CODE HERE ***"
        # END OPTIONAL PROBLEM 2
    return optimized_eval














# 取消注释下面
# 这行以应用尾调用优化
# #

# scheme_eval = optimize_tail_calls(scheme_eval)
