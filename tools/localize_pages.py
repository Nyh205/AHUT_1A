"""阶段 A：去除 lab/hw/disc/proj 页面中的校内后勤内容。

只删「与教学无关」的东西，不动任何教学正文、代码块、答案槽与链接。

整节删除的做法（这里最容易出错，务必理解）：
  1) 只按**小节标题 id** 定位，绝不按「标题 → 下个标题」的跨度切割 ——
     否则夹在中间、藏在 <div class="solution"> 里的复习内容会被一起吞掉。
  2) 标题后面只吃「块级元素序列」（p/pre/ul/ol/blockquote/h3/script/br），
     一遇到 </div> 或下一个标题就停，因此不会把外层结构切开。
  3) 被吃掉的结构尾巴（页面级的 <script> 切换处理器、收尾的 </div>）在
     回调里原样补回；只有「复制按钮」的脚本（含 copy-code-）随内容一起删。

其余规则：
  4) 整节改写：Check Your Score Locally —— 保留本地查分命令，去掉 Gradescope。
  5) 段级删除：Gradescope 提交说明、同伴提交、加分/截止日期、禁用 AI 的政策句。
  6) 小节标题：Lab Checkoff Questions → 概念自测（保留题目，去掉点名流程）。
  7) HTML 注释清理：注释含校内关键词（Gradescope / berkeley.edu / pensieve /
     出勤 / 助教点名 / 截止日期等）的整块删除。注释本就不渲染，删除不影响
     页面外观，只去掉源码里的校内痕迹。若注释里开了 <div> 却没在注释内闭合
     （源站确实存在这种畸形写法），把它后面多出来的 </div> 一并吃掉以保持平衡。

运行：在仓库根目录执行 `python tools/localize_pages.py`
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "cs61a_offline")
DIRS = ["lab", "hw", "disc", "proj"]

# ---------------------------------------------------------------- 基础片段

# 块级元素：用「锚定 + 游标推进」线性扫描，不用带嵌套量词的正则
# （`(?:<p...>|\s*)*` 这类写法会在大页面上触发指数级回溯，直接把脚本卡死）
ELEM_RE = re.compile(
    r'\s*(?:<(p|pre|ul|ol|blockquote|h3|h4|script)\b[^>]*>.*?</\1>|<br\s*/?>)',
    re.S)

# 正文列的收尾：若干 </div> 直到 <div class='col-md-3 ...>，中间的 <script> 属于结构
TAIL_RE = re.compile(
    r"\s*(?:<script\b.*?</script>\s*)*(?:</div>\s*)*(?=<div class=['\"]col-md-3)",
    re.S)

SCRIPT_RE = re.compile(r"<script\b.*?</script>", re.S)
# 任何小节标题，用作「吃到这里为止」的边界
HEAD_ANY_RE = re.compile(r"<h[12] id=")

# Check Your Score Locally → 只保留本地查分
SCORE_NEW = """<h2 id="check-your-score-locally">本地查看得分</h2>

<p>你可以在本地查看本次作业每道题的得分，运行：</p>

<pre><code>python3 ok &#x2d;&#x2d;score</code></pre>
"""


def eat_blocks(s, pos):
    """从 pos 起连续吃掉块级元素，返回停下来的位置。"""
    while True:
        m = ELEM_RE.match(s, pos)
        if not m:
            return pos
        pos = m.end()


def scan_to_boundary(s, pos):
    """往后找最近的「下一个标题」或「正文列收尾」的位置。"""
    cands = []
    h = HEAD_ANY_RE.search(s, pos)
    if h:
        cands.append(h.start())
    t = TAIL_RE.search(s, pos)
    if t:
        cands.append(t.start())
    return min(cands) if cands else len(s)


def cut_section(s, head_re, replacement="", greedy=False):
    """删除匹配 head_re 的小节，返回 (新文本, 命中次数)。

    小节正文 = 标题之后连续的块级元素；一旦碰上 </div> 或下一个标题就停，
    所以不会切开外层结构。若正文正好是页面最后一段，则把它到正文列收尾
    之间的结构（页面级 <script>、收尾 </div>）原样保留。

    greedy=True 用于正文里嵌套着 <ul> 的小节 —— 块级元素匹配会在第一个
    内层 </ul> 处提前收手，留下半截列表。此模式改为一路吃到下一个标题为止。
    """
    out = []
    pos = 0
    count = 0
    while True:
        m = head_re.search(s, pos)
        if not m:
            break
        end = eat_blocks(s, m.end())
        if greedy:
            end = scan_to_boundary(s, end)
        keep = ""
        tm = TAIL_RE.match(s, end)
        if tm:
            tail = s[end:tm.end()]
            keep = "".join(x for x in SCRIPT_RE.findall(tail)
                           if "copy-code-" not in x)
            keep += "\n" + "</div>\n" * tail.count("</div>")
            end = tm.end()
        out.append(s[pos:m.start()])
        out.append(replacement + keep)
        pos = end
        count += 1
    out.append(s[pos:])
    return "".join(out), count


def section(hid, replacement="", tag=r"h[12]", greedy=False):
    rx = re.compile(r'<%s id="%s">[^<]*</%s>' % (tag, hid, tag))
    return (rx, replacement, greedy)


# ---------------------------------------------------------------- 规则表

SECTION_RULES = [
    # 出勤 / 提交作业 / 学期问卷：整节删除
    section("attendance"),
    section("submit-assignment"),
    section("submit(-2)?", tag=r"h[123]"),
    section("survey"),
    section("surveys", greedy=True),
    section("the-course-website", greedy=True),
    section("submitting-the-assignment"),
    # 查分小节 → 只保留本地查分命令
    section("check-your-score-locally", SCORE_NEW),
]

# 整块删除（这些块本身就自成一体，不涉及外层结构，直接删即可）
RAW_SECTIONS = [
    # Getting Started Videos：需用校内邮箱登录，无法观看，连外壳一起删
    re.compile(r'(?:<div class="solution toggle-\d+">\s*)?'
               r'<h2 id="getting-started-videos"[^>]*>.*?</div>', re.S),
    re.compile(r"[ \t]*<button id='toggle-\d+'[^>]*>\s*Getting Started Videos.*?"
               r"</button>[ \t]*\n?", re.S),
    re.compile(r"<!--[^>]*Getting Started Videos.*?-->", re.S),
]

# 段级删除（DOTALL）
DROP_PATTERNS = [
    r"<p\b[^>]*>\s*Submit this assignment by uploading.*?</p>",
    r"<p\b[^>]*>\s*Correctly completing all questions is worth.*?</p>",
    r"<p\b[^>]*>\s*You can add a partner to your Gradescope submission.*?</p>",
    r"<p\b[^>]*>\s*You do not need to modify or turn in any other files.*?</p>",
    r"<p\b[^>]*>\s*Once you are satisfied, submit.*?</p>",
    r"(?m)^Once you are satisfied, submit.*?$",
    r"<p\b[^>]*>\s*The project is worth.*?</p>",
    r"<p\b[^>]*>\s*You can get 1 EC point.*?</p>",
    r"<p\b[^>]*>\s*You may not use artificial intelligence tools.*?</p>",
    r"<p\b[^>]*>\s*<strong>This lab is required for all students\..*?</p>",
    r"<p\b[^>]*>\s*You need to submit the lab problems in addition to attending.*?</p>",
    r"<p\b[^>]*>\s*If you miss lab for a good reason.*?</p>",
    r"<p\b[^>]*>\s*If you miss discussion for a good reason.*?</p>",
    r"<p\b[^>]*>\s*Your TA will come around during discussion.*?</p>",
    r"<p\b[^>]*>\s*This survey counts towards.*?</p>",
    r"<p\b[^>]*>\s*As part of this assignment, fill out the.*?</p>",
    r"<p\b[^>]*>\s*Once you finish the survey.*?</p>",
    r"<p\b[^>]*>\s*<strong>This does NOT submit the assignment!</strong>.*?</p>",
    # 作业页顶部的截止时间与 Gradescope 提交说明
    r"<p\b[^>]*>\s*<(?:em|i)>Due by.*?</(?:em|i)></p>",
    r"<p\b[^>]*>\s*<strong>Submission:</strong>.*?</p>",
    r"<p\b[^>]*>\s*<strong>Important:</strong>\s*You only need to submit to\s*<em>Gradescope</em>.*?</p>",
    r"<p\b[^>]*>\s*Now that you have completed your first assignment.*?</p>",
    # 项目检查点：保留本地 ok 自测，删掉提交说明
    r"<p\b[^>]*>\s*Then, submit .*?Gradescope.*?</p>",
    r"<p\b[^>]*>\s*Upload <strong>only that.*?</p>",
    r"<blockquote><p>During Office Hours and Project Parties.*?</blockquote>",
]
DROP_RES = [re.compile(p, re.S) for p in DROP_PATTERNS]

# 侧边栏：被删小节对应的目录项。
# 删了正文小节却留着目录项，点进去会落空（hw03 的 Q7 就是漏网的一个）——
# 目录项和它指向的 <h*> 必须成对地删。
SIDEBAR_DROP = ["#attendance", "#submit-assignment", "#survey", "#surveys",
                "#submit", "#submit-2", "#the-course-website",
                "#submitting-the-assignment", "#submit-with-gradescope",
                "#getting-started-videos", "#logistics",
                "#q7-mid-semester-feedback"]
SIDEBAR_LI_RE = re.compile(r'[ \t]*<li><a href="([^"]+)"[^>]*>[^\n]*?</a></li>[ \t]*\n?')
# 删完目录项后会留下空壳 <ul></ul>：Bootstrap 会给它上下外边距，白顶出一块
# 空白。反复清到不动为止，嵌套的空壳也一并收掉。
SIDEBAR_EMPTY_UL_RE = re.compile(r'[ \t]*<ul>\s*</ul>[ \t]*\n?')

# 标题 / 目录改写
REWRITES = [
    ('<h2 id="lab-checkoff-questions">Lab Checkoff Questions</h2>',
     '<h2 id="lab-checkoff-questions">概念自测</h2>'),
    ('<a href="#lab-checkoff-questions">Lab Checkoff Questions</a>',
     '<a href="#lab-checkoff-questions">概念自测</a>'),
    ('<a href="#check-your-score-locally">Check Your Score Locally</a>',
     '<a href="#check-your-score-locally">本地查看得分</a>'),
    # 项目检查点：保留本地自测，标题改为中性名称
    ('<h3 id="checkpoint-submission">Checkpoint Submission</h3>',
     '<h3 id="checkpoint-submission">检查点自测</h3>'),
    ('<h2 id="checkpoint-submission">Checkpoint Submission</h2>',
     '<h2 id="checkpoint-submission">检查点自测</h2>'),
    ('<h3 id="submit-your-phase-1-amp-2-checkpoint">Submit your Phase 1 &amp; 2 checkpoint</h3>',
     '<h3 id="submit-your-phase-1-amp-2-checkpoint">检查点自测</h3>'),
    # 侧边栏那一份也要跟着改，否则同一页里标题写「检查点自测」、目录还写
    # "Submit your Phase 1 & 2 checkpoint"（scheme 页就是这样）
    ('<a href="#submit-your-phase-1-amp-2-checkpoint">Submit your Phase 1 &amp; 2 checkpoint</a>',
     '<a href="#submit-your-phase-1-amp-2-checkpoint">检查点自测</a>'),
]

# 含这些词的 HTML 注释整块删除（注释不渲染，删了不影响外观）
CAMPUS_KW = [
    "gradescope", "berkeley.edu", "pensieve", "attendance", "attendanc",
    "your ta ", "your ta.", "ta will", "check you in", "deadline",
    "late day", "late days", "extension", "regrade", "cs61a@",
    "office hours", "staff", "bcourses", "edstem", "ed discussion",
    "submitting the assignment", "submit the assignment",
    "checkpoint", "extra credit", "ec point", "partner",
]
COMMENT_RE = re.compile(r"<!--(?:(?!-->).)*?-->", re.S)
CLOSE_COMMENT_RE = re.compile(r"\s*<!--\s*</div>\s*-->")


def strip_bad_comments(s):
    """删掉含校内痕迹的注释；注释里开了 <div> 却未闭合时，补吃后面的 </div>。"""
    out = []
    pos = 0
    removed = 0
    for m in COMMENT_RE.finditer(s):
        body = m.group(0)
        if not any(k in body.lower() for k in CAMPUS_KW):
            continue
        out.append(s[pos:m.start()])
        pos = m.end()
        removed += 1
        # 注释内多开的 <div>：把紧随其后的 <!-- </div> --> 之类一并吃掉
        dangling = len(re.findall(r"<div\b", body)) - body.count("</div>")
        for _ in range(max(0, dangling)):
            nxt = CLOSE_COMMENT_RE.match(s, pos)
            if not nxt:
                break
            out.append(s[pos:nxt.start()])
            pos = nxt.end()
    out.append(s[pos:])
    s = "".join(out)
    # 清理因删注释而落单的收尾标签
    s = re.sub(r"(?m)^[ \t]*</p></blockquote>[ \t]*\n?", "", s)
    s = re.sub(r"(?m)^[ \t]*</blockquote></p>[ \t]*\n?", "", s)
    return s, removed


def _section_end(s, start):
    """start 是 <section …> 的起点，返回配对 </section> 之后的位置；未闭合返回 -1。"""
    depth = 0
    for t in re.finditer(r"</?section\b", s[start:]):
        if t.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return start + t.end() + 1        # t.end() 停在 '>' 之前
        else:
            depth += 1
    return -1


def drop_section(s, sid):
    """删掉 id=sid 的整个 <section>…</section>（含嵌套），连同前面的空白。

    首页的公告区是个 <section>，里面套着 27 个 <div class="announcement">，
    日历区同理。按「开标签 → 配对闭标签」扫描来切，不用非贪婪正则 ——
    正则会在第一个 </section> 处收手，把外层结构劈坏。
    """
    open_re = re.compile(r"<section\b[^>]*\bid=[\"']%s[\"'][^>]*>" % re.escape(sid))
    n = 0
    while True:
        m = open_re.search(s)
        if not m:
            break
        end = _section_end(s, m.start())
        if end < 0:                    # 没闭合就不动，宁可留英文
            break
        a = m.start()
        while a > 0 and s[a - 1] in " \t\n":
            a -= 1
        s = s[:a] + s[end:]
        n += 1
    return s, n


# 首页（站根 index.html）专属规则：
#   删除 —— 27 段「Announcements: <日期>」校内公告、
#           Current Assignments（含内联脚本填作业按钮的空壳）、
#           日历里挂在作业/实验后面的「Due / Checkpt / Early Due」日期徽章、
#           日历里全部 27 个 Askademia 播放列表按钮；
#   保留 —— Calendar 教学日历（讲座标题、阅读、实验与讨论、作业与项目全部译成中文
#           并保留链接）、h1 课程名。
LOCALIZE_HOME = True
HOME_DROP_SECTIONS = ["announcements", "assignments"]
HOME_DROP_RE = [
    # Current Assignments 的小节标题（它那个 <section> 是空的，由内联脚本填按钮）
    r'[ \t]*<h2 class="frontpage-header">Current Assignments</h2>[ \t]*\n?',
    # 日历里的日期徽章。三种文案（Due / Checkpt / Early Due）共用同一个
    # <div class="badge due"> 外壳，且内部不含嵌套 div，所以非贪婪收到第一个
    # </div> 正好是它自己的闭合。作业/实验的名字与链接在徽章之外，不受影响。
    r'[ \t]*<div class="badge due">.*?</div>[ \t]*\n?',
    # 日历每行的 Askademia 按钮（外部 askademia.org 播放列表）。整个 <li> 连同
    # 后面的换行一起删，不留空行；同一行里的「视频 / 幻灯片」按钮在另一个 <li>，
    # 不受影响。只按 href 认，免得误伤正文里出现的 Askademia 字样。
    r'[ \t]*<li><a [^>]*askademia[^>]*>.*?</a></li>[ \t]*\n?',
]
HOME_DROP_RES = [re.compile(p, re.S) for p in HOME_DROP_RE]

# 讲座标题里的客座讲师署名，如「24. AI Coding Tools (ft. Amy Li)」。
# 「(ft. …)」里是人名（校内人员），按「彻底去除校内痕迹」去掉整个括号；
# 前面的讲座标题照常翻译。
HOME_FT_RE = re.compile(r"\s*\(ft\.[^)]*\)")

# 首页改写。Current Assignments 区是空壳，作业按钮由内联脚本的数组渲染出来，
# 那段数据在 <script> 里 —— translate_text 从不进 <script>，所以按钮上的
# 英文只能在这里改。「Scheme」是项目名，按惯例保留。
HOME_REWRITES = [
    ('"name": "HW 07: Finale"', '"name": "作业 07：终章"'),
]


def localize_home(path):
    """首页：只做删除，译文交给 translate_text.py 的术语表。"""
    with open(path, encoding="utf-8") as f:
        s0 = f.read()
    s = s0
    st = {}
    n = 0
    for sid in HOME_DROP_SECTIONS:
        s, k = drop_section(s, sid)
        n += k
    st["整节"] = n
    n = 0
    for rx in HOME_DROP_RES:
        s, k = rx.subn("", s)
        n += k
    st["删元素"] = n
    n = 0
    for old, new in HOME_REWRITES:
        k = s.count(old)
        s = s.replace(old, new)
        n += k
    st["改写"] = n
    # 只删日历区里的客座署名，正文别处万一出现「(ft. …)」不动
    a = s.find('<section id="calendar"')
    if a > 0:
        b = s.find("</section>", a)
        head, cal, tail = s[:a], s[a:b], s[b:]
        cal, k = HOME_FT_RE.subn("", cal)
        s = head + cal + tail
        st["删署名"] = k
    if s != s0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
    return st


def localize(path):
    with open(path, encoding="utf-8") as f:
        s0 = f.read()
    s = s0
    st = {}

    s, st["注释"] = strip_bad_comments(s)

    n = 0
    for head_re, rep, greedy in SECTION_RULES:
        s, k = cut_section(s, head_re, rep, greedy)
        n += k
    for rx in RAW_SECTIONS:
        s, k = rx.subn("", s)
        n += k
    st["整节"] = n

    n = 0
    for rx in DROP_RES:
        s, k = rx.subn("", s)
        n += k
    st["删段"] = n

    n = 0
    for old, new in REWRITES:
        k = s.count(old)
        s = s.replace(old, new)
        n += k
    st["改写"] = n

    nav_start = s.find("<div class='col-md-3")
    n = 0
    if nav_start > 0:
        head, nav = s[:nav_start], s[nav_start:]

        def _drop(m):
            nonlocal n
            if m.group(1) in SIDEBAR_DROP:
                n += 1
                return ""
            return m.group(0)

        nav = SIDEBAR_LI_RE.sub(_drop, nav)
        while True:                       # 嵌套空壳要删几轮才干净
            nav2 = SIDEBAR_EMPTY_UL_RE.sub("", nav)
            if nav2 == nav:
                break
            nav = nav2
        s = head + nav
    st["删目录"] = n

    if s != s0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
    return st


def main():
    pages = []
    for d in DIRS:
        for root, _, files in os.walk(os.path.join(SITE, d)):
            if "index.html" in files:
                pages.append(os.path.join(root, "index.html"))
    pages = sorted(set(pages))

    totals = {}
    changed = 0
    # 首页走单独一套规则（删公告区与日历区，规则见 localize_home）
    home = os.path.join(SITE, "index.html")
    if LOCALIZE_HOME and os.path.exists(home):
        st = localize_home(home)
        changed += bool(sum(st.values()))
        for k, v in st.items():
            key = "首页·" + k
            totals[key] = totals.get(key, 0) + v

    for p in pages:
        st = localize(p)
        if sum(st.values()):
            changed += 1
        for k, v in st.items():
            totals[k] = totals.get(k, 0) + v

    print("清理完成：共 %d 个页面，改写 %d 个。" % (len(pages), changed))
    for k, v in totals.items():
        print("  %s：%d" % (k, v))


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
