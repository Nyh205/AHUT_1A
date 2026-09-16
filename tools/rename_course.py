"""把站内显示的课程名从 CS 61A 换成 AHUT_1A（课程界面 + 正文提及）。

只改「给人看的文字」，绝不碰代码：

  * <pre> / <code> / <script> / <style> / <textarea> 整块跳过 —— 那里面有 doctest
    （如 hw04 的 `>>> course = 'CS 61A!'`、lab06 的 `>>> a.compose('CS 61A Rocks!', 'Bob')`）
    和程序输出样例，改了 ok 评分就废；
  * HTML 注释整块跳过 —— 反正是看不见的文字，而页面里还留着被注释掉的
    `<script>`，动它没有好处；
  * 标签属性区分对待：给人看的（meta description 的 content、图片 alt 等）照改，
    机器读的网址（href / src / action …，见 UNSAFE_ATTRS）一律不动。当前全站
    没有一处 CS 61A 落在网址属性里，脚本会盯着这个前提，一旦出现就报出来。

实际覆盖到的位置：<title> 后缀、导航栏品牌、<h1>、页脚标题、
<meta name="description">，以及正文里的提及。全站 421 处 = 注释与代码区 10（跳过）
+ 属性值 100 + 可见文字 311。

**必须在 translate_text.py 之后跑**：词表里有多条 key 含 "CS 61A"（例如
"CS 61A: Structure and Interpretation of Computer Programs"），提前改名会让这些
词条失配、整段漏翻。所以它是流水线的最后一道 HTML 工序，而不是清理工序。

起始代码包（zip）不归它管，里面那 14 处也全是代码与 doctest，本就不该改。

幂等：换出来的 AHUT_1A 不再匹配 CS 61A，跑第二遍一处也找不到。

运行：`python tools/rename_course.py`
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "cs61a_offline")

NEW = "AHUT_1A"
PAT = re.compile(r"CS\s*61A")

# 三类别名，**一趟**从左到右扫完：
#   注释整块 | 代码区整块 | 单个标签
# 必须合成一趟。分成「先挖代码、再挖标签」两趟的话，`<!-- <script …></script> -->`
# 这种被注释掉的脚本会先留下一个占位符，紧接着被下一趟的 <[^>]*> 连同两边的
# `<!--` `-->` 一起当标签吞掉 —— 占位符被包了一层，还原时不会再重扫，于是
# 整块内容就烂在页面上。合成一趟后，最左优先的语义天然处理掉这两种嵌套。
PROTECT_RE = re.compile(
    r"<!--.*?-->"
    r"|<(pre|code|script|style|textarea)\b.*?</\1>"
    r"|<[^>]*>",
    re.S | re.I)

# 一个属性：name、name=、name="value"。分段捕获是为了只换值，别动原有空格
# （源文件里写的是 `content ="..."`，顺手normalize掉会制造无谓 diff）
ATTR_RE = re.compile(r'([\w-]+)(\s*=\s*")([^"]*)(")')

# 网址类属性：机器读的，不碰
UNSAFE_ATTRS = {
    "href", "src", "srcset", "action", "formaction", "poster", "cite",
    "longdesc", "data", "codebase", "manifest", "ping", "usemap",
}

# 占位符：HTML 里不会出现 \x00，所以拿它当哨兵不会撞车
HOLD_RE = re.compile(r"\x00(\d+)\x00")

# 网址属性里出现过 CS 61A 的话记在这里（当前应为空，非空即说明边界判断需要重审）
url_hits = []


def rename_tag(tag):
    """标签内的 CS 61A 只可能在给人看的属性里（meta description 的 content 等）。"""
    n = 0

    def _f(m):
        nonlocal n
        name, val = m.group(1), m.group(3)
        if not PAT.search(val):
            return m.group(0)
        if name.lower() in UNSAFE_ATTRS:
            url_hits.append((name, val[:80]))
            return m.group(0)
        val, k = PAT.subn(NEW, val)
        n += k
        return m.group(1) + m.group(2) + val + m.group(4)

    return ATTR_RE.sub(_f, tag), n


def rename(html):
    """返回 (新文本, 替换次数)。"""
    holds = []
    n = [0]

    def _hold(m):
        t = m.group(0)
        if t.startswith("<!--") or m.group(1):
            holds.append(t)                  # 注释、代码区：原样端走
        else:
            t, k = rename_tag(t)             # 标签：顺带改安全属性
            n[0] += k
            holds.append(t)
        return "\x00%d\x00" % (len(holds) - 1)

    s = PROTECT_RE.sub(_hold, html)
    k = len(PAT.findall(s))
    if k:
        n[0] += k
        s = PAT.sub(NEW, s)
    # 一趟还原：re.sub 不会回头重扫替换进去的内容，所以占位符不会互相串
    return HOLD_RE.sub(lambda m: holds[int(m.group(1))], s), n[0]


def main():
    scan = changed = total = 0
    for root, _, files in os.walk(SITE):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as f:
                s0 = f.read()
            scan += 1
            s, n = rename(s0)
            if n:
                total += n
                changed += 1
                with open(path, "w", encoding="utf-8") as f:
                    f.write(s)
    print("课程名替换完成：扫描 %d 个页面，改写 %d 个，共替换 %d 处（CS 61A -> %s）。"
          % (scan, changed, total, NEW))
    if url_hits:
        print("  警告：有 %d 处落在网址属性里，已跳过，请人工确认：" % len(url_hits))
        for name, val in url_hits:
            print("    %s=\"%s\"" % (name, val))


if __name__ == "__main__":
    main()
