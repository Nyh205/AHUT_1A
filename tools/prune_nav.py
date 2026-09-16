"""精简导航栏：删除与教学无关的校内链接。

在 translate_nav.py 之后运行。只改 <nav> 块内的 <li>，不碰正文与属性。
删除规则：
  1) href 命中 DEL_HREF 中任一关键字的 <li> 整行删除；
  2) 删除后内部变空的 dropdown 整块删除（如原来的 Links / Staff 两个菜单）。
"""
import io
import os
import re
import sys

# 与 translate_nav.py 同理：模块级直跑，重定向时需显式指定 UTF-8，否则日志乱码。
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "cs61a_offline")

# 命中即删的 href 关键字（校内后勤 / 校内身份信息）
DEL_HREF = [
    "edstem.org",             # Ed 讨论区
    "gradescope.com",         # 提交与评分平台
    "about-61a",              # 教学大纲（课程政策）
    "office-hours",           # 答疑时间
    "oh.cs61a.org",           # 答疑排队
    "contact-61a",            # 联系
    "campus-res",             # 校园资源
    "articles/advice",        # 学长学姐建议
    "instructor.html",        # 讲师
    "staff",                  # 教师团队（含 staff.html 与无后缀路径）
    "extensions",             # 申请延期
    "regrades",               # 申请重新评分
    "sections.cs61a.org",     # 添加/更换分组
    "bcourses.berkeley.edu",  # 课程录像
    "assignment-calendar",    # 作业日历
]

NAV_RE = re.compile(r'<nav class="navbar[^>]*>.*?</nav>', re.S)
# 单行形式的菜单项： <li><a href="...">文本</a></li>
LI_LINE_RE = re.compile(r'[ \t]*<li><a href="([^"]*)"[^>]*>[^\n]*?</a></li>[ \t]*\n?')
# 整个下拉菜单块（内部不再嵌套 ul）
DD_RE = re.compile(r'[ \t]*<li class="nav-item dropdown">.*?</ul>\s*</li>[ \t]*\n?', re.S)
DD_UL_RE = re.compile(r'<ul class="dropdown-menu"[^>]*>.*?</ul>', re.S)
ANY_LI_RE = re.compile(r'<li\b')


def should_del(href):
    return any(key in href for key in DEL_HREF)


def process_nav(nav):
    # 1) 删除指向校内后勤的菜单项
    nav = LI_LINE_RE.sub(
        lambda m: "" if should_del(m.group(1)) else m.group(0), nav)

    # 2) 删除已被清空的整个下拉菜单
    def _drop_empty(m):
        block = m.group(0)
        ul = DD_UL_RE.search(block)
        if ul and not ANY_LI_RE.search(ul.group(0)):
            return ""
        return block

    return DD_RE.sub(_drop_empty, nav)


changed = 0
total = 0

for root, dirs, files in os.walk(SITE):
    for name in files:
        if not name.endswith(".html"):
            continue
        path = os.path.join(root, name)
        with open(path, encoding="utf-8") as f:
            text = f.read()

        m = NAV_RE.search(text)
        if not m:
            continue
        total += 1

        nav = m.group(0)
        new_nav = process_nav(nav)
        if new_nav == nav:
            continue

        text = text[:m.start()] + new_nav + text[m.end():]
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        changed += 1

print(f"导航精简完成：共扫描 {total} 个含导航页面，改写 {changed} 个。")
