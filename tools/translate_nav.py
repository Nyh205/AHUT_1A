"""把每个 HTML 页面顶部共享导航栏里的英文标签替换为中文。

导航栏出现在 cs61a_offline 下 108 个 html 中，共有 5 个结构变体，但标签文本
是同一套英文。这里只替换 <nav> 块内的英文标签文本，不碰 href/src/id/class、
不碰页面正文。术语按方案术语表。

运行：在仓库根目录执行 `python tools/translate_nav.py`
"""
import io
import os
import re
import sys

# 脚本是模块级直跑（没有 __main__ 守卫），所以包装要放在最前面：输出被重定向
# 到文件时，Windows 默认按 GBK 编码，日志里的中文会变成乱码。
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "cs61a_offline")

# 顺序敏感：长的/包含关系的短语放前面，避免被短标签提前截断。
REPLACEMENTS = [
    ("Request an Extension", "申请延期"),
    ("Request a Regrade", "申请重新评分"),
    ("Office Hours Queue", "答疑排队"),
    ("Add/Change Sections", "添加/更换分组"),
    ("Lecture Recordings", "课程录像"),
    ("Past Exams & Websites", "历年真题与网站"),
    ("Advice from Students", "学长学姐建议"),
    ("Scheme Built-In Procedures", "Scheme 内置过程"),
    ("Scheme Specifications", "Scheme 规范"),
    ("Campus Resources", "校园资源"),
    ("Studying Guide", "学习指南"),
    ("Debugging Guide", "调试指南"),
    ("Composition Guide", "组合指南"),
    ("Type Hints", "类型标注"),
    ("MT1 Study Guide", "MT1 复习指南"),
    ("MT2 Study Guide", "MT2 复习指南"),
    ("Final Study Guide", "期末复习指南"),
    ("Assignment Calendar", "作业日历"),
    ("Office Hours", "答疑时间"),
    ("TAs & Tutors", "助教与辅导员"),
    ("Instructors", "讲师"),
    ("Lectures", "课程"),
    ("Syllabus", "教学大纲"),
    ("Contact", "联系"),
    ("Resources", "资源"),
    ("Guides", "指南"),
    ("Staff", "教师团队"),
    ("Textbook", "教材"),
    ("Code Editors", "代码编辑器"),
    ("Links", "链接"),
    # 以下为保留项：明确不改（此处仅作记录，不参与替换）
]

NAV_RE = re.compile(r'<nav class="navbar[^>]*>.*?</nav>', re.S)

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
        new_nav = nav
        for en, zh in REPLACEMENTS:
            new_nav = new_nav.replace(en, zh)
        if new_nav == nav:
            continue

        text = text[:m.start()] + new_nav + text[m.end():]
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        changed += 1

print(f"导航翻译完成：共扫描 {total} 个含导航页面，改写 {changed} 个。")
