"""把正文切成「可翻译文本段」，用于统计与生成术语表。

为什么不能直接对整页做字符串替换：
  1) 正文里夹着 <code>x</code> 之类行内标签，写成一句英文的模板在原文里
     是断开的（"For a tree <code>t</code>:"），直接搜原文搜不到；
  2) <pre> / <script> 里的内容必须逐字保留，不能被替换碰到。

做法：把正文列（<main> 里、侧边栏之前）切成 token，
  - 块级标签（p/div/li/h1.../<br>）当成**硬分隔**，段与段之间不会互相串味；
  - 行内标签（code/a/strong/em/...）当成**透明**，它两侧的文字连成一段，
    但标签本身按位置记下来，替换命中时按需保留或丢弃。
于是每段得到一个「扁平文本」（扁平文本 == 人眼看到的句子），可以直接拿来做
翻译词表的 key。词表的值可以带 HTML（例如把 <code>ok</code> 写回去）。

运行：`python tools/segments.py`  写出 _runs.txt（次数\t段文本）
"""
import io
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "cs61a_offline")
DIRS = ["lab", "hw", "disc", "proj"]
# 站根下也参与翻译的单页（首页）。它没有侧边栏，content_region 会一路取到
# </main>，切段规则与正文页完全一致。
ROOT_PAGES = ["index.html"]

TAG_RE = re.compile(r"<[^>]*>")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
# 不参与翻译的容器
VERBATIM = {"pre", "script", "style"}
# 透明标签：只是给文字加样式，不该切断句子
INLINE = {
    "code", "a", "strong", "em", "b", "i", "span", "var", "tt", "sup", "sub",
    "kbd", "cite", "abbr", "small", "big", "u", "s", "q", "dfn", "mark",
    "samp", "time", "label", "nobr", "font", "ins", "del", "bdi", "bdo", "wbr",
}


def tokenize(region):
    """把一段 HTML 切成 (kind, payload)；kind ∈ {block, inline, text, verbatim}。

    verbatim（pre/script/style）内容整块作为一个 text token，但标记为不可翻译。
    """
    toks = []
    pos = 0
    stack = []          # 正在打开的 verbatim 容器
    # 注释整体当成一个块：既不渲染、也不该出现在待译文本里。
    # 注意注释里可能含 '>'，所以要把注释和标签一起排序、按下标去重。
    spans = []
    comments = list(COMMENT_RE.finditer(region))
    ci = 0
    for m in TAG_RE.finditer(region):
        while ci < len(comments) and comments[ci].start() < m.start():
            spans.append(comments[ci])
            ci += 1
        spans.append(m)
    spans.extend(comments[ci:])
    # 同一起点优先取长的：`<!-- <a ...> -->` 里注释和 <a> 都从 '<' 开始，
    # 必须先认出整个注释，否则注释会被拆成可见文本。
    spans.sort(key=lambda x: (x.start(), -(x.end() - x.start())))

    for m in spans:
        if m.start() < pos:
            continue                       # 落在上一个 token 里面（如注释内的标签）
        if m.start() > pos:
            toks.append(("verbatim" if stack else "text",
                         region[pos:m.start()]))
        raw = m.group(0)
        pos = m.end()
        if raw.startswith("<!--"):
            toks.append(("block", raw))
            continue
        name = re.match(r"</?\s*([A-Za-z0-9]+)", raw)
        name = name.group(1).lower() if name else ""
        closing = raw.startswith("</")
        selfclose = raw.endswith("/>") or name in ("br", "hr", "img", "input",
                                                   "meta", "link", "col")
        if stack:
            # verbatim 内部：原样吞掉，直到对应闭合标签
            toks.append(("verbatim", raw))
            if closing and name == stack[-1]:
                stack.pop()
            continue
        if name in VERBATIM and not closing and not selfclose:
            toks.append(("verbatim", raw))
            stack.append(name)
            continue
        if name in INLINE and not selfclose:
            toks.append(("inline", raw))
            continue
        toks.append(("block", raw))
    if pos < len(region):
        toks.append(("verbatim" if stack else "text", region[pos:]))
    return toks


def content_region(s):
    """正文列：<main> 开头 到 侧边栏 <div class='col-md-3 之前。"""
    a = s.find("<main")
    if a < 0:
        return None
    b = s.find("<div class='col-md-3", a)
    if b < 0:
        b = s.find('<div class="col-md-3', a)
    if b < 0:
        b = s.find("</main>", a)
    if b < 0:
        return None
    return s[a:b]


def tag_name(raw):
    m = re.match(r"</?\s*([A-Za-z0-9]+)", raw)
    return m.group(1).lower() if m else ""


def _anchor_end(toks, i, hi):
    """从 toks[i]（<a ...> 开标签）找到配对的 </a> 下标；找不到返回 None。"""
    depth = 0
    for j in range(i, hi):
        kind, payload = toks[j]
        if kind != "inline":
            continue
        name = tag_name(payload)
        if name != "a":
            continue
        if payload.startswith("</"):
            depth -= 1
            if depth == 0:
                return j
        else:
            depth += 1
    return None


def build_run(toks, lo, hi):
    """把一个 run 的 token 变成 (flat_text, items, anchors)。

    flat_text 是人眼看到的句子。超链接 <a>…</a> 整体抽成一个占位符 {0}、{1}…
    —— 译文的句子常常要重排，逐字保留标签是不可能的；让占位符跟着译文走，
    链接就永远不会丢。

    items 里每项是 (kind, flat_start, flat_end, payload)：
      't' 普通文字（payload = token 下标）
      'z' 零宽行内标签（payload = token 下标）
      'A' 超链接（payload = anchors 下标）
    """
    flat = []
    items = []
    anchors = []
    n = 0
    i = lo
    while i < hi:
        kind, payload = toks[i]
        if kind == "text":
            items.append(("t", n, n + len(payload), i))
            flat.append(payload)
            n += len(payload)
            i += 1
            continue
        if tag_name(payload) == "a" and not payload.startswith("</"):
            j = _anchor_end(toks, i, hi)
            if j is not None:
                k = len(anchors)
                anchors.append("".join(toks[x][1] for x in range(i, j + 1)))
                mark = "{%d}" % k
                items.append(("A", n, n + len(mark), k))
                flat.append(mark)
                n += len(mark)
                i = j + 1
                continue
        items.append(("z", n, n, i))
        i += 1
    return "".join(flat), items, anchors


def runs_of(region):
    """返回 [(flat_text, items, anchors, tok_lo, tok_hi)]。

    后两项是这个 run 覆盖的 token 区间，替换脚本靠它把译文放回原位。
    """
    toks = tokenize(region)
    runs = []
    lo = None
    for i, (kind, _) in enumerate(toks):
        if kind in ("block", "verbatim"):
            if lo is not None:
                runs.append(build_run(toks, lo, i) + (lo, i))
                lo = None
        elif lo is None:
            lo = i
    if lo is not None:
        runs.append(build_run(toks, lo, len(toks)) + (lo, len(toks)))
    return runs


def pages():
    out = []
    for d in DIRS:
        for root, _, files in os.walk(os.path.join(SITE, d)):
            if "index.html" in files:
                out.append(os.path.join(root, "index.html"))
    for p in ROOT_PAGES:
        f = os.path.join(SITE, p)
        if os.path.exists(f):
            out.append(f)
    return sorted(set(out))


def main():
    cnt = Counter()
    bad = 0
    for p in pages():
        region = content_region(open(p, encoding="utf-8").read())
        if region is None:
            continue
        # 先做一次无损往返校验：token 拼回去必须与原文逐字相同
        if "".join(x[1] for x in tokenize(region)) != region:
            bad += 1
            print("  ! token 往返不一致：", p)
        for flat, _, _, _, _ in runs_of(region):
            t = flat.strip()
            if t:
                cnt[t] += 1
    if bad:
        print("往返校验失败 %d 个页面" % bad)
    # 用 JSONL 而不是 TSV：段落里本来就有换行，TSV 会把一段切成好几行
    with open(os.path.join(ROOT, "_runs.jsonl"), "w", encoding="utf-8",
              newline="\n") as f:
        for t, n in cnt.most_common():
            f.write(json.dumps({"n": n, "t": t}, ensure_ascii=False) + "\n")
    print("文本段：%d 个不同，%d 次出现" % (len(cnt), sum(cnt.values())))
    dist = Counter(n for n in cnt.values())
    print("次数分布：", sorted(dist.items())[:12], "... 最大", max(cnt.values()))
    for th in (2, 3, 4, 6):
        sel = [(t, n) for t, n in cnt.items() if n >= th]
        print("  >=%d: %d 段 / %d 次" % (th, len(sel), sum(n for _, n in sel)))


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
