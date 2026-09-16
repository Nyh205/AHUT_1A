"""从起始代码包里挖出「该翻译的文字」并放回去。

起始代码在 zip 里（42 个不重复的包）。要翻的是 docstring 的正文和 # 注释，
一个字都不能碰的包括：

  * 所有 >>> doctest 行及紧随的期望输出 —— ok 的评分依据；
  * ______ 占位符、"*** YOUR CODE HERE ***"；
  * `# BEGIN/END PROBLEM` 标记、编码声明、shebang、工具指令注释；
  * 代码本身、字符串字面量、assert 消息。

做法：用 ast 精确定位每个 docstring 字面量，用 tokenize 精确定位每个 # 注释，
只在这两种 token 的行列区间里做替换。docstring 里逐行分类，连着几行正文合成
一段（英文是折行的，逐行翻会把句子切断），译完按原缩进重新折行。

    用 tools/py_todo.py 出批次，用 tools/py_apply.py 写回去并重新打包。
"""
import ast
import io
import os
import re
import tokenize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "cs61a_offline")

# 基础设施 / 图形界面 / 第三方：学生不读这些，翻了只是徒增风险
SKIP_NAMES = {
    "sqlite_shell.py", "construct_check.py",
    "svg.py", "svg_test.py", "common_server.py",
    "canvas.py", "turtle.py", "turtle_class.py", "pillow_canvas.py",
    "forwarding_canvas.py", "logging_canvas.py", "color_names.py",
    "default_graphics.py", "model.py",
    "multiplayer.py", "score.py", "leaderboard_integrity.py",
    "__init__.py", "gui.py", "hog_ui.py", "cats_gui.py",
}

# 这些注释是给工具看的，不是给人读的，原样保留
KEEP_RE = re.compile(
    r"^\s*#\s*(?:!|-\*-|coding[:=]|type:|noqa|pylint|fmt:|yapf|isort|"
    r"BEGIN\b|END\b)", re.I)

# 含这些片段的行碰到就会破坏 doctest / ok 评分，一律不翻
GUARD = ("______", "*** YOUR CODE HERE ***", ">>>", "ok -q", "ok --")

DOC_MIN = 4          # 短于这个字数的正文不值得翻
WRAP = 74            # 折行目标列宽（含缩进）
ASCII_RUN = re.compile(r"[A-Za-z0-9_@#$%&*+=<>{}\[\]()/\\.,:;'\"-]+|.", re.S)

# docstring 里「E.g., <返回值示例>」这种行，后半段是学生代码必须**逐字返回**的
# 字符串 —— 同一个 docstring 的 doctest 里就写着它。把示例也翻成中文，学生照着
# 写出中文串就过不了 doctest：那不叫翻译，叫改题。所以只译引导词，示例原样留。
EXAMPLE_RE = re.compile(r"^(E\.g\.,|eg\.,|For example,|Example:|Eg\.)\s*")
EXAMPLE_ZH = {"E.g.,": "例如，", "Eg.": "例如，", "eg.,": "例如，",
              "For example,": "例如，", "Example:": "示例："}


def _skeleton(s):
    """抹掉数字、压掉空白 —— 只留「消息长什么样」。

    `Current candy stock: 3` 和 doctest 里的 `'Current candy stock: 2'` 是同一
    条消息的两个实例，只有数字不同。逐字比对配不上，抹掉数字才对得上。
    """
    return " ".join(re.sub(r"\d+", "", s).split())


def _expected_outputs(ilines, kinds):
    """本 docstring 里 doctest 期望输出的「骨架」集合。"""
    out = set()
    for ln, kind in zip(ilines, kinds):
        if kind != "d":
            continue
        s = ln.strip()
        if not s or s.startswith(">>>") or s.startswith("..."):
            continue
        if any(g in s for g in GUARD):
            continue
        out.add(_skeleton(s.strip("'\"")))
    out.discard("")
    return out


def _is_sample(sk, expected):
    """sk 是不是若干条期望输出的拼接。

    类 docstring 里写着 `'Nothing left to vend. Please restock.'` 和
    `'Please add $3 more funds.'` 两条，而方法 docstring 的例子把两条并成了
    一句 —— 所以要允许多段拼接，不能只做整串相等。
    """
    if not sk:
        return False
    n = len(sk)
    reach = [False] * (n + 1)
    reach[0] = True
    for i in range(n):
        if not reach[i]:
            continue
        for e in expected:
            if e and sk.startswith(e, i):
                j = i + len(e)
                reach[j] = True
                if j < n and sk[j] == " ":    # 段间允许一个空格
                    reach[j + 1] = True
    return reach[n]


def targets(dedup=True):
    """[(zip 绝对路径, 包内路径)] —— 去掉基础设施和内容重复的包。

    dedup 只对「出批次」有意义：内容一模一样的包没必要翻两遍。写回时必须
    dedup=False，否则同内容包里的另一份会留在英文。
    """
    import glob
    import hashlib
    import zipfile
    seen, out = set(), []
    for z in sorted(glob.glob(os.path.join(SITE, "*", "**", "*.zip"),
                              recursive=True)):
        rel = os.path.relpath(z, SITE).replace(os.sep, "/")
        if rel.startswith("exam/"):
            continue
        with open(z, "rb") as f:
            digest = hashlib.md5(f.read()).hexdigest()
        if dedup and digest in seen:
            continue
        seen.add(digest)
        with zipfile.ZipFile(z) as f:
            for n in f.namelist():
                if not n.endswith(".py"):
                    continue
                if any(p in n for p in ("editor/", "libs/", "tests/", "/ok/")):
                    continue
                if os.path.basename(n) in SKIP_NAMES:
                    continue
                out.append((z, n))
    return sorted(out)


def _doc_nodes(tree):
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if not isinstance(body, list) or not body:
            continue
        first = body[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) \
                and isinstance(first.value.value, str):
            yield first.value


def _classify(lines):
    """docstring 内文逐行分类：'' 空行 / 'd' doctest 或期望输出 / 'p' 正文。"""
    kinds, in_doc = [], False
    for ln in lines:
        s = ln.strip()
        if s.startswith(">>>"):
            in_doc = True
            kinds.append("d")
        elif not s:
            in_doc = False
            kinds.append("")
        elif in_doc or any(g in ln for g in GUARD):
            kinds.append("d")
        else:
            kinds.append("p")
    return kinds


def _doc_inner(src, node):
    """一个 docstring 的内文行，以及首行起始列。切不出引号就返回 None。"""
    rows = src.split("\n")
    r0, c0, r1, c1 = node.lineno, node.col_offset, node.end_lineno, node.end_col_offset
    if r0 == r1:
        raw = rows[r0 - 1][c0:c1]
    else:
        raw = "\n".join([rows[r0 - 1][c0:]] + rows[r0:r1 - 1]
                        + [rows[r1 - 1][:c1]])
    m = re.match(r'^[A-Za-z]*("""|\'\'\'|"|\')', raw)
    if not m:
        return None
    quote = m.group(1)
    inner = raw[m.end():]
    if inner.endswith(quote):
        inner = inner[:-len(quote)]
    return inner.split("\n"), c0 + m.end(), c0, r0


def _doc_segments(src, node, expected):
    """把一个 docstring 拆成若干可译段落。"""
    got = _doc_inner(src, node)
    if got is None:
        return []
    ilines, head_col, c0, r0 = got

    kinds = _classify(ilines)
    segs, i = [], 0
    while i < len(ilines):
        if kinds[i] != "p":
            i += 1
            continue
        j = i
        while j + 1 < len(ilines) and kinds[j + 1] == "p":
            j += 1
        spans = []
        for k in range(i, j + 1):
            if k == 0:
                spans.append((r0, head_col, head_col + len(ilines[0])))
            else:
                spans.append((r0 + k, 0, len(ilines[k])))
        joined = " ".join(ilines[k].strip() for k in range(i, j + 1))
        # 「E.g., X」且 X 是本文件某条期望输出的实例（或几条的拼接）→ 只译引导词。
        # 比的是全文件的期望输出，不是本 docstring 的：例子在方法 docstring 里，
        # doctest 通常挂在类 docstring 上。
        # 例子可能折行（`E.g., …restock.` / 续行 `Please add $3 more funds.`），
        # 所以不能在单行段落上才判 —— joined 里两行已经接成一句了。
        pin = None
        m = EXAMPLE_RE.match(joined)
        if m and _is_sample(_skeleton(joined[m.end():].strip("'\"")), expected):
            pin = m.group(0)
        if len(joined) >= DOC_MIN and not any(g in joined for g in GUARD):
            # 段落首行的行首缩进：首行贴着引号时没有缩进，用代码缩进续行
            if i == 0:
                first_prefix, cont = "", " " * c0
            else:
                first_prefix = " " * (len(ilines[i]) - len(ilines[i].lstrip()))
                cont = first_prefix
            seg = {"kind": "doc", "r0": spans[0][0], "r1": spans[-1][0],
                   "en": joined, "rows": spans,
                   "first": first_prefix, "cont": cont}
            if pin:
                seg["prefix"] = pin
            segs.append(seg)
        i = j + 1
    return segs


def _com_segments(src):
    """把连续的 # 注释行合成一段。"""
    rows = src.split("\n")
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return []
    segs, run = [], []
    for t in toks:
        if t.type != tokenize.COMMENT:
            continue
        line = rows[t.start[0] - 1]
        if KEEP_RE.match(line[t.start[1]:]):
            continue
        # 只有「整行都是注释」才和上一行并成一段。行尾注释前面是代码，
        # 两行代码的尾巴合成一段会把代码本身吃掉。
        bare = not line[:t.start[1]].strip()
        if run and not (bare and run[-1][3]
                        and t.start[0] == run[-1][0] + 1):
            _flush_com(run, rows, segs)
            run = []
        run.append((t.start[0], t.start[1], len(line), bare))
    _flush_com(run, rows, segs)
    return segs


def _flush_com(run, rows, segs):
    if not run:
        return
    body = [rows[r - 1][c:e].lstrip("#").strip() for r, c, e, _ in run]
    joined = " ".join(b for b in body if b)
    if len(joined) >= DOC_MIN and not any(g in joined for g in GUARD):
        indent = run[0][1]
        segs.append({"kind": "com", "r0": run[0][0], "r1": run[-1][0],
                     "en": joined, "rows": [x[:3] for x in run],
                     "first": " " * indent + "# ",
                     "cont": " " * indent + "# "})


def scan(src):
    """一个 .py 的所有可译段落，按位置排序。"""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    nodes = list(_doc_nodes(tree))
    # 先扫一遍收齐全文件的期望输出骨架，再拆段落 —— 「E.g., X」的判定要用到它
    expected = set()
    for node in nodes:
        got = _doc_inner(src, node)
        if got is not None:
            expected |= _expected_outputs(got[0], _classify(got[0]))
    segs = []
    for node in nodes:
        segs += _doc_segments(src, node, expected)
    segs += _com_segments(src)
    segs.sort(key=lambda s: (s["r0"], s["rows"][0][1]))
    return segs


BREAK = " ，。；：、）】》,;:)]}"


def spread(zh, n, pre0, cont):
    """把译文摊成恰好 n 行 —— 行数与原段落一致，文件形状不变。

    刻意不按列宽重新折行：`.py` 起始文件里大量行尾注释本身就长得离谱
    （前缀就 88 个字符），按宽度折只会在代码后面制造出一堆没有 # 的续行。
    行数对齐既省掉所有行号平移，也不改变文件的观感。
    """
    if n <= 1:
        return [pre0 + zh]
    unit = max(1, -(-len(zh) // n))
    pieces, rest = [], zh
    for k in range(n - 1):
        cut = min(len(rest), unit)
        for d in range(0, 10):              # 就近找个断点，别把词切两半
            hit = None
            for c in (cut + d, cut - d):
                if 0 < c < len(rest) and rest[c - 1] in BREAK:
                    hit = c
                    break
            if hit is not None:
                cut = hit
                break
        pieces.append(rest[:cut].rstrip())
        rest = rest[cut:].lstrip()
    pieces.append(rest)
    return [pre0 + pieces[0]] + [cont + p for p in pieces[1:]]


def apply_edits(src, edits):
    """edits: [(seg, 译文)]，从后往前替换，其余字节一个不动。

    段落占的是文件里的连续若干整行（首行可能从引号或代码之后开始，末行可能
    到引号之前结束）。替换时首行接住原文前缀（缩进、引号、# 号），末行接住
    收尾引号，中间的行数与原文一一对应。
    """
    rows = src.split("\n")
    for seg, zh in sorted(edits, key=lambda e: -e[0]["r0"]):
        start, end = seg["r0"] - 1, seg["r1"] - 1
        fc1 = seg["rows"][0][1]
        lc2 = seg["rows"][-1][2]
        pre0 = seg["first"] if fc1 == 0 \
            else rows[start][:fc1] + seg["first"].lstrip()
        out = spread(zh, end - start + 1, pre0, seg["cont"])
        out[-1] += rows[end][lc2:]          # 收尾引号 / 行尾残余
        rows[start:end + 1] = out
    return "\n".join(rows)
