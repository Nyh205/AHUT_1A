"""UCB 模块包含 UC Berkeley 项目专用的函数。"""


import code
import functools
import inspect
import re
import signal
import sys


def main(fn):
    """用命令行参数调用 fn。用作装饰器。

    main 装饰器标记启动程序的函数。例如，

    @main def
    my_run_function()
    : # 函数体

    用它来代替典型的 __name__ == "__main__" 判断。
    """
    if inspect.stack()[1][0].f_locals['__name__'] == '__main__':
        args = sys.argv[1:] # 从命令行中丢弃脚本名
        fn(*args) # 调用 main 函数
    return fn

_PREFIX = ''
def trace(fn):
    """一个装饰器，在每次函数被调用时打印函数名、
    它的参数和它的返回值。例如，

    @trace def
    compute_something(x,
    y): # 函数体
    """
    @functools.wraps(fn)
    def wrapped(*args, **kwds):
        global _PREFIX
        reprs = [repr(e) for e in args]
        reprs += [repr(k) + '=' + repr(v) for k, v in kwds.items()]
        log('{0}({1})'.format(fn.__name__, ', '.join(reprs)) + ':')
        _PREFIX += '    '
        try:
            result = fn(*args, **kwds)
            _PREFIX = _PREFIX[:-4]
        except Exception as e:
            log(fn.__name__ + ' exited via exception')
            _PREFIX = _PREFIX[:-4]
            raise
        # 这里，打印出返回值。
        log('{0}({1}) -> {2}'.format(fn.__name__, ', '.join(reprs), result))
        return result
    return wrapped


def log(message):
    """打印一条缩进的消息（与 trace 一起使用）。"""
    print(_PREFIX + re.sub('\n', '\n' + _PREFIX, str(message)))


def log_current_line():
    """打印关于当前代码行的信息。"""
    frame = inspect.stack()[1]
    log('Current line: File "{f[1]}", line {f[2]}, in {f[3]}'.format(f=frame))


def interact(msg=None):
    """在当前环境中启动一个交互式解释器会话。

    在 Unix 上：<Control>-D
    退出交互式会话并返回正常执行。在
    Windows 上：<Control>-Z
    <Enter>
    退出交互式会话并返回正常执行。
    """
    # 在当前命名空间中求值命令
    frame = inspect.currentframe().f_back
    namespace = frame.f_globals.copy()
    namespace.update(frame.f_locals)

    # 中断时退出
    def handler(signum, frame):
        print()
        exit(0)
    signal.signal(signal.SIGINT, handler)

    if not msg:
        _, filename, line, _, _, _ = inspect.stack()[1]
        msg = 'Interacting at File "{0}", line {1} \n'.format(filename, line)
        msg += '    Unix:    <Control>-D continues the program; \n'
        msg += '    Windows: <Control>-Z <Enter> continues the program; \n'
        msg += '    exit() or <Control>-C exits the program'

    code.interact(msg, None, namespace)