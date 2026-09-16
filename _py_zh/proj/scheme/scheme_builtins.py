"""这个模块实现了 Scheme 语言的内置过程。"""

import math
import numbers
import operator
import sys

from link import Link, nil, repl_str
from scheme_reader import *
from scheme_classes import *
from scheme_utils import *


# 内置过程
# #
# 

# 一个由三元组 (NAME, PYTHON-FUNCTION, INTERNAL-NAME)
# 组成的列表。由 builtin 添加，并在 create_global_frame 中使用。
BUILTINS = []

def builtin(*names, need_env=False):
    """一个注解，用于将 Python 函数转换为 BuiltinProcedure。"""
    def add(py_func):
        for name in names:
            BUILTINS.append((name, py_func, names[0], need_env))
        return py_func
    return add

builtin("procedure?")(scheme_procedurep)
builtin("list?")(scheme_listp)
builtin("atom?")(scheme_atomp)
builtin("boolean?")(scheme_booleanp)
builtin("number?")(scheme_numberp)
builtin("symbol?")(scheme_symbolp)
builtin("string?")(scheme_stringp)
builtin("null?")(scheme_nullp)

@builtin("not")
def scheme_not(x):
    return not is_scheme_true(x)

@builtin("equal?")
def scheme_equalp(x, y):
    if scheme_pairp(x) and scheme_pairp(y):
        return scheme_equalp(x.first, y.first) and scheme_equalp(x.rest, y.rest)
    elif scheme_numberp(x) and scheme_numberp(y):
        return x == y
    else:
        return type(x) == type(y) and x == y


@builtin("eq?")
def scheme_eqp(x, y):
    if scheme_numberp(x) and scheme_numberp(y):
        return x == y
    elif scheme_symbolp(x) and scheme_symbolp(y):
        return x == y
    else:
        return x is y

@builtin("pair?")
def scheme_pairp(x):
    return type(x).__name__ == 'Link'

@builtin("scheme-valid-cdr?")
def scheme_valid_cdrp(x):
    return scheme_pairp(x) or scheme_nullp(x) or scheme_promisep(x)

# 流
@builtin("promise?")
def scheme_promisep(x):
    return type(x).__name__ == 'Promise'

@builtin("force")
def scheme_force(x):
    validate_type(x, scheme_promisep, 0, 'promise')
    return x.evaluate()

@builtin("cdr-stream")
def scheme_cdr_stream(x):
    validate_type(x, lambda x: scheme_pairp(x) and scheme_promisep(x.rest), 0, 'cdr-stream')
    return scheme_force(x.rest)

@builtin("length")
def scheme_length(x):
    validate_type(x, scheme_listp, 0, 'length')
    return len_link(x)

@builtin("cons")
def scheme_cons(x, y):
    return Link(x, y)

@builtin("car")
def scheme_car(x):
    validate_type(x, scheme_pairp, 0, 'car')
    return x.first

@builtin("cdr")
def scheme_cdr(x):
    validate_type(x, scheme_pairp, 0, 'cdr')
    return x.rest

# 修改附加内容
@builtin("set-car!")
def scheme_set_car(x, y):
    validate_type(x, scheme_pairp, 0, 'set-car!')
    x.first = y

@builtin("set-cdr!")
def scheme_set_cdr(x, y):
    validate_type(x, scheme_pairp, 0, 'set-cdr!')
    validate_type(y, scheme_valid_cdrp, 1, 'set-cdr!')
    x.rest = y

@builtin("list")
def scheme_list(*vals):
    result = nil
    for e in reversed(vals):
        result = Link(e, result)
    return result

@builtin("append")
def scheme_append(*vals):
    if len(vals) == 0:
        return nil
    result = vals[-1]
    for i in range(len(vals)-2, -1, -1):
        v = vals[i]
        if v is not nil:
            validate_type(v, scheme_pairp, i, 'append')
            r = p = Link(v.first, result)
            v = v.rest
            while scheme_pairp(v):
                p.rest = Link(v.first, result)
                p = p.rest
                v = v.rest
            result = r
    return result

@builtin("integer?")
def scheme_integerp(x):
    return scheme_numberp(x) and (isinstance(x, numbers.Integral) or int(x) == x)

def _check_nums(*vals):
    """检查 VALS 中的所有参数都是数字。"""
    for i, v in enumerate(vals):
        if not scheme_numberp(v):
            msg = "operand {0} ({1}) is not a number"
            raise SchemeError(msg.format(i, v))

def _arith(fn, init, vals):
    """对 VALS 的数值执行 FN 操作，当 VALS 为空时以
    INIT 作为值。将结果作为 Scheme 值返回。"""
    _check_nums(*vals)
    s = init
    for val in vals:
        s = fn(s, val)
    s = _ensure_int(s)
    return s

def _ensure_int(x):
    if int(x) == x:
        x = int(x)
    return x

@builtin("+")
def scheme_add(*vals):
    return _arith(operator.add, 0, vals)

@builtin("-")
def scheme_sub(val0, *vals):
    _check_nums(val0, *vals) # 修复差一错误
    if len(vals) == 0:
        return _ensure_int(-val0)
    return _arith(operator.sub, val0, vals)

@builtin("*")
def scheme_mul(*vals):
    return _arith(operator.mul, 1, vals)

@builtin("/")
def scheme_div(val0, *vals):
    _check_nums(val0, *vals) # 修复差一错误
    try:
        if len(vals) == 0:
            return _ensure_int(operator.truediv(1, val0))
        return _arith(operator.truediv, val0, vals)
    except ZeroDivisionError as err:
        raise SchemeError(err)

@builtin("expt")
def scheme_expt(val0, val1):
    _check_nums(val0, val1)
    return pow(val0, val1)

@builtin("abs")
def scheme_abs(val0):
    return abs(val0)

@builtin("quotient")
def scheme_quo(val0, val1):
    _check_nums(val0, val1)
    try:
        return -(-val0 // val1) if (val0 < 0) ^ (val1 < 0) else val0 // val1
    except ZeroDivisionError as err:
        raise SchemeError(err)

@builtin("modulo")
def scheme_modulo(val0, val1):
    _check_nums(val0, val1)
    try:
        return val0 % val1
    except ZeroDivisionError as err:
        raise SchemeError(err)

@builtin("remainder")
def scheme_remainder(val0, val1):
    _check_nums(val0, val1)
    try:
        result = val0 % val1
    except ZeroDivisionError as err:
        raise SchemeError(err)
    while result < 0 and val0 > 0 or result > 0 and val0 < 0:
        result -= val1
    return result

def number_fn(module, name, fallback=None):
    """一个 Scheme 内置过程，用于调用名为
    MODULE.FN 的数值 Python 函数。"""
    py_fn = getattr(module, name) if fallback is None else getattr(module, name, fallback)
    def scheme_fn(*vals):
        _check_nums(*vals)
        return py_fn(*vals)
    return scheme_fn

# 将 math 模块中的数值函数添加为 Scheme 的内置过程
for _name in ["acos", "acosh", "asin", "asinh", "atan", "atan2", "atanh",
              "ceil", "copysign", "cos", "cosh", "degrees", "floor", "log",
              "log10", "log1p", "radians", "sin", "sinh", "sqrt",
              "tan", "tanh", "trunc"]:
    builtin(_name)(number_fn(math, _name))
builtin("log2")(number_fn(math, "log2", lambda x: math.log(x, 2)))  # Python 2 兼容性

def _numcomp(op, x, y):
    _check_nums(x, y)
    return op(x, y)

@builtin("=")
def scheme_eq(x, y):
    return _numcomp(operator.eq, x, y)

@builtin("<")
def scheme_lt(x, y):
    return _numcomp(operator.lt, x, y)

@builtin(">")
def scheme_gt(x, y):
    return _numcomp(operator.gt, x, y)

@builtin("<=")
def scheme_le(x, y):
    return _numcomp(operator.le, x, y)

@builtin(">=")
def scheme_ge(x, y):
    return _numcomp(operator.ge, x, y)

@builtin("even?")
def scheme_evenp(x):
    _check_nums(x)
    return x % 2 == 0

@builtin("odd?")
def scheme_oddp(x):
    _check_nums(x)
    return x % 2 == 1

@builtin("zero?")
def scheme_zerop(x):
    _check_nums(x)
    return x == 0

# 其他
# 操作
# 

@builtin("display")
def scheme_display(*vals):
    vals = [repl_str(val[1:-1] if scheme_stringp(val) else val) for val in vals]
    print(*vals, end="")

@builtin("print")
def scheme_print(*vals):
    vals = [repl_str(val) for val in vals]
    print(*vals)

@builtin("displayln")
def scheme_displayln(*vals):
    scheme_display(*vals)
    scheme_newline()

@builtin("newline")
def scheme_newline():
    print()
    sys.stdout.flush()

@builtin("error")
def scheme_error(msg=None):
    msg = "" if msg is None else repl_str(msg)
    raise SchemeError(msg)

@builtin("exit")
def scheme_exit():
    raise EOFError

@builtin("map", need_env=True)
def scheme_map(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'map')
    validate_type(s, scheme_listp, 1, 'map')
    from scheme_eval_apply import complete_apply
    return map_link(lambda x: complete_apply(fn, Link(x, nil), env), s)

@builtin("filter", need_env=True)
def scheme_filter(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'filter')
    validate_type(s, scheme_listp, 1, 'filter')
    from scheme_eval_apply import complete_apply
    head, current = nil, nil
    while s is not nil:
        item, s = s.first, s.rest
        if complete_apply(fn, Link(item, nil), env):
            if head is nil:
                head = Link(item, nil)
                current = head
            else:
                current.rest = Link(item, nil)
                current = current.rest
    return head

@builtin("reduce", need_env=True)
def scheme_reduce(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'reduce')
    validate_type(s, lambda x: x is not nil, 1, 'reduce')
    validate_type(s, scheme_listp, 1, 'reduce')
    from scheme_eval_apply import complete_apply
    value, s = s.first, s.rest
    while s is not nil:
        value = complete_apply(fn, scheme_list(value, s.first), env)
        s = s.rest
    return value

@builtin("load", need_env=True)
def scheme_load(*args):
    """加载一个 Scheme 源文件。ARGS 的形式应为 (SYM, ENV)
    或 (SYM, QUIET, ENV)。名为 SYM 的文件被加载到
    Frame ENV 中，详细程度由 QUIET 决定（默认为 true）。"""
    if not (2 <= len(args) <= 3):
        expressions = args[:-1]
        raise SchemeError('"load" given incorrect number of arguments: '
                          '{0}'.format(len(expressions)))
    sym = args[0]
    quiet = args[1] if len(args) > 2 else True
    env = args[-1]
    if (scheme_stringp(sym)):
        sym = eval(sym)
    validate_type(sym, scheme_symbolp, 0, 'load')
    with scheme_open(sym) as infile:
        lines = infile.readlines()
    args = (lines, None) if quiet else (lines,)
    def next_line():
        return buffer_lines(*args)

    from scheme import read_eval_print_loop
    read_eval_print_loop(next_line, env, quiet=quiet, report_errors=True)

@builtin("load-all", need_env=True)
def scheme_load_all(directory, env):
    """
    按字母顺序加载给定目录中的所有 .scm
    文件。仅在 tests/ 代码中使用。
    """
    assert scheme_stringp(directory)
    directory = directory[1:-1]
    import os
    for x in sorted(os.listdir(".")):
        if not x.endswith(".scm"):
            continue
        scheme_load(x, env)

def scheme_open(filename):
    """如果 FILENAME 或 FILENAME.scm 是有效文件的名称，
    则返回一个打开该文件的 Python 文件对象。否则，抛出错误。"""
    try:
        return open(filename)
    except IOError as exc:
        if filename.endswith('.scm'):
            raise SchemeError(str(exc))
    try:
        return open(filename + '.scm')
    except IOError as exc:
        raise SchemeError(str(exc))


# 海龟绘
# 图（非
# 标准）

turtle = CANVAS = None

def _title():
    import turtle as _nativeturtle
    _nativeturtle.title("Scheme Turtles")

def attempt_install_tk_turtle():
    try:
        from abstract_turtle import turtle
    except ImportError:
        raise SchemeError("Could not find abstract_turtle. This should never happen in student-facing situations. If you are a student, please file a bug on Piazza.")
    return turtle

def attempt_create_tk_canvas():
    try:
        import tkinter as _
    except:
        raise SchemeError("\n".join([
            "Could not import tkinter, so the tk-turtle will not work.",
            "Either install python with tkinter support or run in pillow-turtle mode"
        ]))
    from abstract_turtle import TkCanvas
    return TkCanvas(1000, 1000, init_hook=_title)

def attempt_create_pillow_canvas():
    try:
        import PIL as _
        import numpy as _
    except:
        raise SchemeError("\n".join([
            "Could not import abstract_turtle[pillow_canvas]'s dependencies.",
            "To install these packages, run",
            "    python3 -m pip install 'abstract_turtle[pillow_canvas]'",
            "You can also run in tk-turtle mode by removing the flag `--pillow-turtle`"
        ]))
    from abstract_turtle import PillowCanvas
    return PillowCanvas(1000, 1000)

def _tscheme_prep():
    global turtle, CANVAS
    if turtle is not None:
        return
    _turtle = attempt_install_tk_turtle()
    if builtins.TK_TURTLE:
        try:
            _CANVAS = attempt_create_tk_canvas()
        except SchemeError as e:
            print(e, file=sys.stderr)
            print("Attempting pillow canvas mode", file=sys.stderr)
            _CANVAS = attempt_create_pillow_canvas()
    else:
        _CANVAS = attempt_create_pillow_canvas()
    turtle, CANVAS = _turtle, _CANVAS
    turtle.set_canvas(CANVAS)
    turtle.mode("logo")


@builtin("forward", "fd")
def tscheme_forward(n):
    """沿当前朝向将海龟向前移动 N 个单位。"""
    _check_nums(n)
    _tscheme_prep()
    turtle.forward(n)

@builtin("backward", "back", "bk")
def tscheme_backward(n):
    """沿当前朝向将海龟向后移动
    N 个单位，不改变方向。"""
    _check_nums(n)
    _tscheme_prep()
    turtle.backward(n)

@builtin("left", "lt")
def tscheme_left(n):
    """将海龟的朝向逆时针旋转 N 度。"""
    _check_nums(n)
    _tscheme_prep()
    turtle.left(n)

@builtin("right", "rt")
def tscheme_right(n):
    """将海龟的朝向顺时针旋转 N 度。"""
    _check_nums(n)
    _tscheme_prep()
    turtle.right(n)

@builtin("circle")
def tscheme_circle(r, extent=None):
    """绘制一个圆心在海龟左侧 R 个单位处的圆（即，
    如果 N 为负则在右侧。如果 EXTENT
    不是 None，则只绘制圆的 EXTENT 度。
    如果 R 为负则按顺时针方向绘制，否则按逆时针方向绘制，
    结束时海龟朝向沿弧线的方向。"""
    if extent is None:
        _check_nums(r)
    else:
        _check_nums(r, extent)
    _tscheme_prep()
    turtle.circle(r, extent and extent)

@builtin("setposition", "setpos", "goto")
def tscheme_setposition(x, y):
    """将海龟的位置设置为 (X,Y)，朝向不变。"""
    _check_nums(x, y)
    _tscheme_prep()
    turtle.setposition(x, y)

@builtin("setheading", "seth")
def tscheme_setheading(h):
    """将海龟的朝向设置为从北方（向上）顺时针 H 度。"""
    _check_nums(h)
    _tscheme_prep()
    turtle.setheading(h)

@builtin("penup", "pu")
def tscheme_penup():
    """抬起画笔，使海龟不绘制。"""
    _tscheme_prep()
    turtle.penup()

@builtin("pendown", "pd")
def tscheme_pendown():
    """放下画笔，使海龟开始绘制。"""
    _tscheme_prep()
    turtle.pendown()

@builtin("showturtle", "st")
def tscheme_showturtle():
    """使海龟可见。"""
    _tscheme_prep()
    turtle.showturtle()

@builtin("hideturtle", "ht")
def tscheme_hideturtle():
    """使海龟可见。"""
    _tscheme_prep()
    turtle.hideturtle()

@builtin("clear")
def tscheme_clear():
    """清空绘图，保持海龟不变。"""
    _tscheme_prep()
    turtle.clear()

@builtin("color")
def tscheme_color(c):
    """将颜色设为 C，一个诸如 "red" 或
    "#ffc0c0" 的字符串（表示十六进制的红、绿、蓝值。"""
    _tscheme_prep()
    validate_type(c, scheme_stringp, 0, "color")
    turtle.color(eval(c))

@builtin("rgb")
def tscheme_rgb(red, green, blue):
    """根据取值为 0 到 1 的 RED、GREEN 和 BLUE 返回一种颜色。"""
    colors = (red, green, blue)
    for x in colors:
        if x < 0 or x > 1:
            raise SchemeError("Illegal color intensity in " + repl_str(colors))
    scaled = tuple(int(x*255) for x in colors)
    return '"#%02x%02x%02x"' % scaled

@builtin("begin_fill")
def tscheme_begin_fill():
    """开始一系列移动，勾勒出待填充形状的轮廓。"""
    _tscheme_prep()
    turtle.begin_fill()

@builtin("end_fill")
def tscheme_end_fill():
    """填充自上次 begin_fill 以来绘制的形状。"""
    _tscheme_prep()
    turtle.end_fill()

@builtin("bgcolor")
def tscheme_bgcolor(c):
    _tscheme_prep()
    validate_type(c, scheme_stringp, 0, "bgcolor")
    turtle.bgcolor(eval(c))

@builtin("exitonclick")
def tscheme_exitonclick():
    global turtle
    """Wait for a click on the turtle window, and then close it."""
    if turtle is None:
        return
    _tscheme_prep()
    if builtins.TK_TURTLE:
        print("Close or click on turtle window to complete exit")
    if builtins.TURTLE_SAVE_PATH is not None:
        _save(builtins.TURTLE_SAVE_PATH)
    turtle.exitonclick()
    turtle = None

@builtin("speed")
def tscheme_speed(s):
    """按照 S 所指明的值设置海龟的动画速度（一个
    0-10 的整数，其中 0 表示无动画（线条立即绘制）
    ，1-10 表示移动越来越快。"""
    validate_type(s, scheme_integerp, 0, "speed")
    _tscheme_prep()
    turtle.speed(s)

@builtin("pixel")
def tscheme_pixel(x, y, c):
    """在 (X, Y) 处用颜色 C 绘制一个填充的像素方块（默认为 1 像素）。"""
    validate_type(c, scheme_stringp, 0, "pixel")
    color = c[1:-1]
    _tscheme_prep()
    turtle.pixel(x, y, color)

@builtin("pixelsize")
def tscheme_pixelsize(size):
    """将像素大小改为 SIZE。"""
    _check_nums(size)
    _tscheme_prep()
    turtle.pixel_size(size)

@builtin("screen_width")
def tscheme_screen_width():
    """当前尺寸下的屏幕宽度，以像素为单位（默认为 1）。"""
    _tscheme_prep()
    return turtle.canvas_width()

@builtin("screen_height")
def tscheme_screen_height():
    """当前尺寸下的屏幕高度，以像素为单位（默认为 1）。"""
    _tscheme_prep()
    return turtle.canvas_height()

def _save(path):
    if not builtins.TK_TURTLE:
        path = path + ".png"
        CANVAS.export().save(path, "png")
    else:
        CANVAS.export(path + ".ps")

@builtin("save-to-file")
def tscheme_write_to_file(path):
    _tscheme_prep()
    validate_type(path, scheme_stringp, 0, "save-to-file")
    path = eval(path)
    _save(path)

@builtin("print-then-return")
def scheme_print_return(val1, val2):
    print(repl_str(val1))
    return val2

def add_builtins(frame, funcs_and_names):
    """将 FUNCS_AND_NAMES 中的绑定作为内置过程加入 FRAME
    这个环境框架。FUNCS_AND_NAMES 中的每一项形式为 (NAME,
    PYTHON-FUNCTION, INTERNAL-NAME)。"""
    for name, py_func, proc_name, need_env in funcs_and_names:
        frame.define(name, BuiltinProcedure(py_func, name=proc_name, need_env=need_env))

def create_global_frame():
    """创建一个由内置项（包括 eval 和 apply）填充的全局框架。"""
    env = Frame(None)
    env.define('undefined', None)
    add_builtins(env, BUILTINS)

    # 向全局框架添加 eval 和
    # apply 在此导入以避免循环依赖
    from scheme_eval_apply import scheme_eval, complete_apply
    env.define('eval', BuiltinProcedure(scheme_eval, True, 'eval'))
    env.define('apply', BuiltinProcedure(complete_apply, True, 'apply'))

    return env
