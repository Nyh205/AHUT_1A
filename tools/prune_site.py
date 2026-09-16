"""站点级清理：整页删除、头部元数据里的校内痕迹，以及页脚与正文里的死链。

translate_nav.py / prune_nav.py 只动顶部导航，localize_pages.py 只动 68 个
教学页的正文 —— 这些地方谁都不管：

  * 旧版重复页与整页英文的校园页（见 DROP_PAGES），共 8 个页面；
  * <meta name="author"> 写着课程负责人姓名（106 页是 Rebecca Dang，
    2 页是 John DeNero / Kay Ousterhout）；
  * 首页 <p> 里注释掉的同一署名（见 INSTRUCTOR_NOTE_RE）；
  * <meta name="keywords"> 里夹着 Berkeley、EECS；
  * 页脚第一列的 Weekly Schedule / Office Hours / Staff 指向校内页面，
    其中 weekly 在镜像里根本不存在；第三列 Policies 的三个链接一律指向
    同样缺失的 articles/about；
  * 删掉页面后，正文里指向它们的链接会变死链，由 unwrap_dead_links() 拆成
    纯文字（页脚里那几条不归它管，前面已经整条删掉了）；
  * 首页教学日历的「日期」列（见 prune_calendar_dates）—— 那排的是 Berkeley
    2026 暑期自己的日程，对本土教学没有意义。

页脚只出现在 40 个外围页面（站根、articles/、exam/、resources/ 等），
68 个核心教学页没有页脚，所以这一节的影响面很窄。

只做删除、拆链接与属性改值，不新增内容；跑第二遍找不到任何目标，天然幂等。

注意：核心教学页里出现的 Berkeley 一律不动 —— 那些是正文内容、题目数据或
doctest 里的字符串（如 lab04 的 make_city('Berkeley', ...)），删了就是破坏课程。

运行：`python tools/prune_site.py`
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "cs61a_offline")

# 两类要整页删掉的东西：
#
# 1) 旧版重复页：早期镜像把它们抓在 lab/lab00.html（比 lab/lab00/index.html 浅
#    一层），正文与 index.html 版逐字相同 —— 逐行比对下来，差异只有相对路径
#    深度（`../` 的个数，以及指向同目录资源的 `lab00/` 前缀），可见文字一模一样。
#    全站零入链，但正文还是英文，留着会被部署、被搜索引擎收录，搜到就是英文版。
#
# 2) 整页英文的校园页：讲师介绍、助教名单、联系方式、校园资源、与课程组联系。
#    68 个核心教学页一个都不链它们（导航下拉那两条由 prune_nav.py 删掉，页脚里
#    那几条由本脚本的页脚规则删掉），但文件还在 cs61a_offline/ 里，照样会被
#    部署、被搜索引擎收录。正文全是与教学无关的校内事务，按「彻底去除校内痕迹」
#    整页删除。删完原先指向它们的链接会变死链，由 unwrap_dead_links() 收尾。
#
# 英文原件都留在 _backup_en/，需要时可恢复（恢复后本脚本会再删一次）。
DROP_PAGES = [
    "lab/lab00.html",
    "lab/lab09.html",
    "proj/scheme.html",
    "instructor.html",
    "staff.html",
    "contact/index.html",
    "articles/campus-res/index.html",
    "articles/contact-61a/index.html",
]

AUTHOR_RE = re.compile(r'[ \t]*<meta[^>]*\bname="author"[^>]*>[ \t]*\n?')
KEYWORDS_RE = re.compile(
    r'(<meta[^>]*\bname="keywords"[^>]*\bcontent\s*=\s*")([^"]*)(")')
# 保留通用描述，只去掉校内字样
CAMPUS_TERMS = {"berkeley", "eecs"}

FOOTER_RE = re.compile(r"<footer\b.*?</footer>", re.S)
# 指向校内页面的条目：weekly（课程日程）、office-hours、staff.html
FOOTER_LI_RE = re.compile(
    r'[ \t]*<li><a\s[^>]*href="[^"]*(?:weekly|office-hours|staff\.html)[^"]*"'
    r'[^>]*>.*?</a></li>[ \t]*\n?')
# Policies 整列：三个链接全部指向缺失的 articles/about。
# 列内没有嵌套 div，所以非贪婪收到第一个 </div> 正好是它自己的闭合。
FOOTER_COL_RE = re.compile(
    r'[ \t]*<div class="col col-sm-4">\s*<h3><a\s[^>]*href="[^"]*articles/about"'
    r'[^>]*>.*?</div>[ \t]*\n?', re.S)
# 删完条目后第一列只剩空 <ul>，一并收掉（限定在页脚里做，免得动到别处）
EMPTY_UL_RE = re.compile(
    r'[ \t]*<ul class="nav nav-pills nav-stacked">\s*</ul>[ \t]*\n?')

# 首页 <p> 里注释掉的讲师署名，夹在「2026 年暑期：」和上课时间之间。它写在英文
# 原版里，早先只删了 <head> 的 <meta name="author">，这处同名的残留漏掉了。
# 全站只此一处。注释内容不含 '>'，所以 [^>]*? 不会跨过相邻注释的边界。
INSTRUCTOR_NOTE_RE = re.compile(r"[ \t]*<!--[^>]*?Instructor:[^>]*?-->[ \t]*\n?")

# 首页教学日历的「日期」列。单元格形如
#   <td><a id="calendar_6_22" class="calendar-date-anchor"></a>Mon<br>6/22</td>
# 表头是 <th>Date</th>（本脚本跑在 translate_text 之前，所以那会儿还是英文；
# 要是哪天顺序变了，中文的也认）。
#
# 整列一起删，表格仍是矩形：周次列有 rowspan（一周四行只写一个周次），日期列
# 则每行都有，各删一个不影响对齐。周次（1、2、3…）对教学排课有用，保留。
#
# 那两个 id 锚点全站没有别处引用，JS 也不碰这张表（assets/js/calendar.js 是
# FullCalendar 的答疑时间表，首页根本没引入它），删了不影响什么。
DATE_TH_RE = re.compile(r"[ \t]*<th>(?:Date|日期)</th>[ \t]*\n?")
DATE_TD_RE = re.compile(
    r'[ \t]*<td>\s*<a\s[^>]*class="calendar-date-anchor"[^>]*>\s*</a>.*?</td>'
    r"[ \t]*\n?", re.S)

# 指向被删页面的链接：把 <a ...>文字</a> 拆回「文字」，句子照样读得通，又不留
# 死链。按文件名认，忽略相对路径深度（`staff.html` 与 `../../staff.html` 都算）。
DEAD_LINK_RE = re.compile(
    r'<a\s[^>]*href="[^"]*(?:staff\.html|instructor\.html'
    r'|contact/index\.html|articles/campus-res|articles/contact-61a)[^"]*"'
    r'[^>]*>(.*?)</a>', re.S)


def unwrap_dead_links(s):
    """拆掉指向已删页面的链接，返回 (新文本, 次数)。"""
    return DEAD_LINK_RE.subn(r"\1", s)


def prune_footer(s):
    """删页脚里的校内链接与死链列，返回 (新文本, 次数)。"""
    n = 0

    def _f(m):
        nonlocal n
        f = m.group(0)
        for rx in (FOOTER_LI_RE, FOOTER_COL_RE, EMPTY_UL_RE):
            f, k = rx.subn("", f)
            n += k
        return f

    return FOOTER_RE.sub(_f, s), n


def prune_calendar_dates(s):
    """删掉首页教学日历的「日期」列（表头 + 每行那一格），返回 (新文本, 次数)。"""
    s, a = DATE_TH_RE.subn("", s)
    s, b = DATE_TD_RE.subn("", s)
    return s, a + b


def prune_keywords(s):
    """从 keywords 里摘掉 Berkeley / EECS，其余不动。"""
    n = 0

    def _f(m):
        nonlocal n
        terms = [t.strip() for t in m.group(2).split(",")]
        kept = [t for t in terms if t.lower() not in CAMPUS_TERMS]
        if len(kept) == len(terms):
            return m.group(0)
        n += 1
        return m.group(1) + ", ".join(kept) + m.group(3)

    return KEYWORDS_RE.sub(_f, s), n


def drop_pages():
    """删掉旧版重复页，返回删除个数。"""
    n = 0
    for rel in DROP_PAGES:
        p = os.path.join(SITE, rel)
        if os.path.exists(p):
            os.remove(p)
            n += 1
    return n


def main():
    dropped = drop_pages()
    scan = changed = 0
    st = {"作者": 0, "署名注释": 0, "关键词": 0, "页脚": 0, "拆死链": 0, "日历日期列": 0}
    for root, _, files in os.walk(SITE):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as f:
                s0 = f.read()
            scan += 1
            s = s0
            s, k = AUTHOR_RE.subn("", s)
            st["作者"] += k
            s, k = INSTRUCTOR_NOTE_RE.subn("", s)
            st["署名注释"] += k
            s, k = prune_keywords(s)
            st["关键词"] += k
            s, k = prune_footer(s)
            st["页脚"] += k
            # 必须排在页脚规则之后：页脚里那几条 <li> 已被整条删掉，
            # 这一步只收拾正文里剩下的内联链接。
            s, k = unwrap_dead_links(s)
            st["拆死链"] += k
            s, k = prune_calendar_dates(s)
            st["日历日期列"] += k
            if s != s0:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(s)
                changed += 1
    print("站点清理完成：扫描 %d 个页面，改写 %d 个。" % (scan, changed))
    print("  整页删除：%d" % dropped)
    print("  删除作者元数据：%d" % st["作者"])
    print("  删除署名注释：%d" % st["署名注释"])
    print("  清理关键词：%d" % st["关键词"])
    print("  删除页脚条目：%d" % st["页脚"])
    print("  拆分死链：%d" % st["拆死链"])
    print("  删除日历日期列：%d（表头 + 单元格）" % st["日历日期列"])


if __name__ == "__main__":
    main()
