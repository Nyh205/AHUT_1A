# 你不需要理解这段代码中的任何内容！
import base64
ob = "CmRlZiBhZGRpdGlvbihleHByKToKICAgIGRpdmlkZW5kID0gZXhwci5maXJzdAogICAgZXhwciA9IGV4cHIucmVzdAogICAgd2hpbGUgZXhwciAhPSBuaWw6CiAgICAgICAgZGl2aXNvciA9IGV4cHIuZmlyc3QKICAgICAgICBkaXZpZGVuZCArPSBkaXZpc29yCiAgICAgICAgZXhwciA9IGV4cHIucmVzdAogICAgcmV0dXJuIGRpdmlkZW5kCgpkZWYgc3VidHJhY3Rpb24oZXhwcik6CiAgICBkaXZpZGVuZCA9IGV4cHIuZmlyc3QKICAgIGV4cHIgPSBleHByLnJlc3QKICAgIHdoaWxlIGV4cHIgIT0gbmlsOgogICAgICAgIGRpdmlzb3IgPSBleHByLmZpcnN0CiAgICAgICAgZGl2aWRlbmQgLT0gZGl2aXNvcgogICAgICAgIGV4cHIgPSBleHByLnJlc3QKICAgIHJldHVybiBkaXZpZGVuZAoKZGVmIG11bHRpcGxpY2F0aW9uKGV4cHIpOgogICAgZGl2aWRlbmQgPSBleHByLmZpcnN0CiAgICBleHByID0gZXhwci5yZXN0CiAgICB3aGlsZSBleHByICE9IG5pbDoKICAgICAgICBkaXZpc29yID0gZXhwci5maXJzdAogICAgICAgIGRpdmlkZW5kICo9IGRpdmlzb3IKICAgICAgICBleHByID0gZXhwci5yZXN0CiAgICByZXR1cm4gZGl2aWRlbmQKCmRlZiBkaXZpc2lvbihleHByKToKICAgIGRpdmlkZW5kID0gZXhwci5maXJzdAogICAgZXhwciA9IGV4cHIucmVzdAogICAgd2hpbGUgZXhwciAhPSBuaWw6CiAgICAgICAgZGl2aXNvciA9IGV4cHIuZmlyc3QKICAgICAgICBkaXZpZGVuZCAvPSBkaXZpc29yCiAgICAgICAgZXhwciA9IGV4cHIucmVzdAogICAgcmV0dXJuIGRpdmlkZW5kCg=="
exec(base64.b64decode(ob.encode("ascii")).decode("ascii"))
##############

def calc_eval(exp):
    """
    >>> calc_eval(Link("define", Link("a", Link(1, nil))))
    'a'
    >>> calc_eval("a")
    1
    >>> calc_eval(Link("+", Link(1, Link(2, nil))))
    3
    """
    if isinstance(exp, Link):
        operator = exp.first
        operands = exp.rest
        if operator == 'and': # and 表达式
            return eval_and(operands)
        elif operator == 'define': # define 表达式
            return eval_define(operands)
        else: # 调用表达式
            return calc_apply(calc_eval(operator), map_link(calc_eval, operands))
    elif exp in OPERATORS:   # 查找过程
        return OPERATORS[exp]
    elif isinstance(exp, int) or isinstance(exp, bool):   # 数字和布尔值
        return exp
    elif exp in bindings:   # 查找变量
        return bindings[exp]

def calc_apply(op, args):
    return op(args)

def floor_div(args):
    """
    >>> floor_div(Link(100, Link(10, nil)))
    10
    >>> floor_div(Link(5, Link(3, nil)))
    1
    >>> floor_div(Link(1, Link(1, nil)))
    1
    >>> floor_div(Link(5, Link(2, nil)))
    2
    >>> floor_div(Link(23, Link(2, Link(5, nil))))
    2
    >>> calc_eval(Link("//", Link(4, Link(2, nil))))
    2
    >>> calc_eval(Link("//", Link(100, Link(2, Link(2, Link(2, Link(2, Link(2, nil))))))))
    3
    >>> calc_eval(Link("//", Link(100, Link(Link("+", Link(2, Link(3, nil))), nil))))
    20
    """
    result = args.first
    divisors = args.rest
    while divisors != nil:
        divisor = divisors.first
        result //= divisor
        divisors = divisors.rest
    return result

scheme_t = True   # Scheme 的 #t
scheme_f = False  # Scheme 的 #f

def eval_and(expressions):
    """
    >>> calc_eval(Link("and", Link(1, nil)))
    1
    >>> calc_eval(Link("and", Link(False, Link("1", nil))))
    False
    >>> calc_eval(Link("and", Link(1, Link(Link("//", Link(5, Link(2, nil))), nil))))
    2
    >>> calc_eval(Link("and", Link(Link('+', Link(1, Link(1, nil))), Link(3, nil))))
    3
    >>> calc_eval(Link("and", Link(Link('-', Link(1, Link(0, nil))), Link(Link('/', Link(5, Link(2, nil))), nil))))
    2.5
    >>> calc_eval(Link("and", Link(0, Link(1, nil))))
    1
    >>> calc_eval(Link("and", nil))
    True
    """
    curr, val = expressions, True
    while curr is not nil:
        val = calc_eval(curr.first)
        if val is scheme_f:
            return scheme_f
        curr = curr.rest
    return val

OPERATORS = { "//": floor_div, "+": addition, "-": subtraction, "*": multiplication, "/": division }

class Link:
    """一个链表。
    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    (5 7 (8 9))
    >>> print(Link(9, 10))
    (9 . 10)
    >>> print(Link(s, 10))
    ((5 7 (8 9)) . 10)
    >>> print(Link.empty)
    ()
    >>> print(Link(Link.empty))
    (())
    """
    empty = ()

    def __init__(self, first, rest=empty):
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is Link.empty:
            rest_repr = ''
        else:
            rest_repr = ', ' + repr(self.rest)
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        s = '(' + repl_str(self.first)
        rest = self.rest
        while isinstance(rest, Link):
            s += ' ' + repl_str(rest.first)
            rest = rest.rest
        if rest is not Link.empty:
            s += ' . ' + repl_str(rest)
        return s + ')'

nil = Link.empty

def repl_str(val):
    """在 Scheme REPL 中显示该值。"""
    if val is True:
        return "#t"
    if val is False:
        return "#f"
    if val is None:
        return "undefined"
    if isinstance(val, str) and val and val[0] == "\"":
        return "\"" + repr(val[1:-1])[1:-1] + "\""
    return str(val)

def len_link(s):
    """返回链表的长度。
    >>> len_link(Link(1, Link(2, Link(3))))
    3
    >>> len_link(Link.empty)
    0
    """
    result = 0
    while isinstance(s, Link):
        result, s = result + 1, s.rest
    return result

def map_link(f, s):
    """对链表 s 映射函数 f。
    >>> square = lambda x: x * x
    >>> map_link(square, Link(1, Link(2, Link(3))))
    Link(1, Link(4, Link(9)))
    """
    if s is Link.empty:
        return s
    return Link(f(s.first), map_link(f, s.rest))

bindings = {}

def eval_define(expressions):
    """
    >>> eval_define(Link("a", Link(1, nil)))
    'a'
    """
    symbol, value = expressions.first, calc_eval(expressions.rest.first)
    bindings[symbol] = value
    return symbol

