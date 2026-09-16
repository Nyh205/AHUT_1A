"""阶段 B：按术语表把正文里的英文替换成中文。

工作方式（安全第一）：
  * 只处理 <main>…</main>（正文列 + 侧边栏）与 <title>、<html lang>。
  * 正文按 tools/segments.py 的规则切成 token：块级标签是硬边界（句子不会
    跨段匹配），行内标签（code/strong…）透明，"For a tree <code>t</code>:"
    在人眼里就是一整句；<pre>/<script> 整块原样保留，谁都不许碰。
  * **超链接 <a …>…</a> 整体抽成占位符 {0}、{1}…**（见 segments.build_run）。
    译文的句序常常要重排，逐字保住标签做不到；让占位符跟着译文走，
    链接就不会丢。术语表的 key/value 里直接写 {0} 即可。
    命中范围里有链接、而译文没写回对应占位符时，这一段**放弃替换**，
    宁可留英文也不删链接。

术语表放在 tools/i18n/*.json，格式两种都收：
    "英文": "中文"
    "英文": {"zh": "中文", "mode": "exact"}      # exact=整段相等才替换

匹配规则：key 长度 >= SUB_MIN 时按子串替换（要求词边界，空白可跨换行匹配），
否则要求整段相等；含占位符的 key 一律只做整段匹配（{0} 的编号只对那一段成立）。

用法：
    python tools/translate_text.py            # 应用
    python tools/translate_text.py --check    # 统计未翻译的段落 → _todo.jsonl
    python tools/translate_text.py --verbose  # 打印需要人工复核的命中
"""
import glob
import io
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "cs61a_offline")
I18N = os.path.join(ROOT, "tools", "i18n")

SUB_MIN = 20           # 短于这个长度的 key 只做整段匹配
VERBOSE = "--verbose" in sys.argv

from segments import content_region, tokenize, runs_of, pages, tag_name  # noqa: E402

# 允许出现在译文里的标签：只放行纯样式，别的一律当成可疑（人工复核）。
ALLOWED_NEW = {"code", "strong", "em", "b", "i"}
# 只有「纯样式」标签允许随英文一起消失（译文一般用中文替代）。
# <a> 走占位符机制、<code> 走「按内文找回来」机制，都不在此列 ——
# 链接一个都不能丢，等宽标识符也一个都不能丢。
DROPPABLE = {"strong", "em", "b", "i", "span", "u", "s", "small", "big",
             "kbd", "var", "tt", "samp", "cite", "abbr", "dfn",
             "mark", "time", "q", "font", "sub", "sup", "del", "ins"}

PLACEHOLDER_RE = re.compile(r"\{(\d+)\}")
ANCHOR_RE = re.compile(r"(<a\b[^>]*>)([^<]*)(</a>)")
TAG_IN_VAL_RE = re.compile(r"</?\s*([A-Za-z0-9]+)")

# 术语表里有条目、但应用时被安全检查挡下来的段落。
# 这些段落会原样留英文 —— 必须显式记下来，否则「为什么这里还是英文」无从查起。
REJECTS = []


# ------------------------------------------------------------------ 术语表

def load_dict():
    """返回 {英文: (中文, 模式)}；模式 ∈ {auto, exact, sub}。

    skip.json 不在这里：它不是词条，是「不必翻译」的清单。
    """
    d = {}
    for path in sorted(glob.glob(os.path.join(I18N, "*.json"))):
        if os.path.basename(path) == "skip.json":
            continue
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
        for en, val in raw.items():
            if isinstance(val, dict):
                d[en] = (val["zh"], val.get("mode", "auto"))
            else:
                d[en] = (val, "auto")
    return d


def norm(s):
    """空白归一：段落里的换行/缩进不该影响查表。"""
    return " ".join(s.split())


def flex(k):
    """把 key 里的空白换成 \\s+，这样硬换行的原文也能匹配。"""
    return r"\s+".join(re.escape(w) for w in k.split())


def split_dict(d):
    """拆成 (整段表, 子串正则, 子串表)。"""
    exact, sub = {}, {}
    for k, (zh, mode) in d.items():
        nk = norm(k)
        if "{" in nk:                     # 含链接占位符的一律整段匹配
            mode = "exact"
        if mode == "exact" or (mode == "auto" and len(nk) < SUB_MIN):
            exact[nk] = zh
        else:
            sub[nk] = zh
    if not sub:
        return exact, None, {}
    keys = sorted(sub, key=len, reverse=True)
    pat = re.compile(r"(?<![A-Za-z0-9])(" +
                     "|".join(flex(k) for k in keys) +
                     r")(?![A-Za-z0-9])")
    return exact, pat, sub


# ------------------------------------------------------------------ 匹配

def is_open(raw):
    return not raw.startswith("</")


def pair_tags(items, toks):
    """把零宽行内标签按名字配对，返回 {item 下标: 伙伴 item 下标}。"""
    stack, pairs = [], {}
    for i, it in enumerate(items):
        if it[0] != "z":
            continue
        raw = toks[it[3]][1]
        name = tag_name(raw)
        if is_open(raw):
            stack.append((name, i))
        elif stack and stack[-1][0] == name:
            _, j = stack.pop()
            pairs[i] = j
            pairs[j] = i
    return pairs


def run_matches(F, exact, pat, sub, stats):
    """返回 [(起点, 终点, 译文)]；位置是 flat 文本上的下标。"""
    nf = norm(F)
    if nf in exact:
        stats["整段"] += 1
        return [(len(F) - len(F.lstrip()), len(F.rstrip()), exact[nf])]
    if pat is None:
        return []
    out = []
    for m in pat.finditer(F):
        out.append((m.start(), m.end(), sub[norm(m.group(1))]))
    stats["子串"] += len(out)
    return out


def check_value(val, anchors, need, stats):
    """译文里的占位符是否合法：范围内每个链接都必须写回，且不越界。"""
    used = set()
    for m in PLACEHOLDER_RE.finditer(val):
        k = int(m.group(1))
        if k >= len(anchors):
            return False
        used.add(k)
    if any(items_k not in used for items_k in need):
        return False
    for name in TAG_IN_VAL_RE.findall(val):
        if name.lower() not in ALLOWED_NEW:
            stats["可疑标签"] += 1
            if VERBOSE:
                stats.setdefault("可疑样例", []).append((val[:70], ""))
            break
    return True


def anchors_in(items, lo_idx, ms, me):
    """返回被这次替换吞掉的链接 item 下标。

    边界必须和 `splice` 里那圈「跳过 [ms, me] 内所有 item」的循环一致
    （都用闭区间）：零宽标签正好落在 me 上时，跳过循环会吞掉它，这里若不
    算进来，它就不会出现在 opens/closes 里 —— 结果就是标签凭空少一个。
    """
    out = []
    for i in range(lo_idx, len(items)):
        it = items[i]
        if it[1] > me:
            break
        if it[0] == "A":
            if it[1] >= ms:
                out.append(i)
            else:
                return [-1]                # 占位符被从中间切断 —— 拒绝
    return out


CODE_PAIR_RE = re.compile(r"<code>.*?</code>", re.S)


def _code_spans(val):
    return [m.span() for m in CODE_PAIR_RE.finditer(val)]


WORD_RE = re.compile(r"^[A-Za-z0-9_]+$")

# 一个标签的整体（<strong>、</code>、<a href="…">）。命中落在这里面等于把标签
# 从中间劈开 —— 见 find_code_slot 的说明。
TAG_SPAN_RE = re.compile(r"<[^>]*>")


def _tag_spans(val):
    return [m.span() for m in TAG_SPAN_RE.finditer(val)]


def _wordchar(c):
    """这个词素算不算「字母数字」——只认 ASCII。

    不能直接用 str.isalnum()：它对汉字也返回 True，于是中文里紧挨着标识符的
    写法（「接收一个非负整数n」）会被判成词中命中，短标识符的 <code> 就白丢了。
    词边界这条规则本来只为挡住 mutate 里的 t 这类英文误包，所以只看 ASCII 即可。
    """
    return c.isascii() and c.isalnum()


def find_code_slot(val, inner, used, taken):
    """给一段该加回 <code> 的内文找一个位置；找不到返回 None。

    译文里的 SQL 关键字、表名、变量名（SELECT / big_game / [columns] …）几乎
    总是原样保留，所以按内文找回去即可。两条约束：

      * 短标识符（t、x、n）必须落在词边界上，否则会把 mutate 里的 t 也包成
        等宽 —— 那是错的；
      * 不能落在已定下来的包裹范围里。英文里 <code>WHERE [condition]</code>
        套着 <code>[condition]</code>，外层先占住 "WHERE [condition]"，
        内层就得退而求其次去包句子后面那个单独的 [condition]，而不是钻进
        外层里面再套一层。

    每次都从头找、只用 used 防重复，**不能**用「上次找到的位置」当游标：
    中文的语序和英文不一样（"returns True if n is ..." 会翻成「如果 n 是……
    就返回 True」），游标一往无前就会把后面那些其实在前面的标识符全判成找不到。
    """
    if not inner:
        return None
    n = len(inner)
    word = bool(WORD_RE.match(inner))
    tags = _tag_spans(val)
    k = val.find(inner)
    while k >= 0:
        ok = k not in used and not any(k < y and x < k + n for x, y in taken)
        # 命中不能落在任何标签内部。英文 `… instead of <code>/</code>.` 的
        # 内文是单个斜杠，译文里 <strong> 还带着一层 —— 从头找找到的第一个
        # 斜杠正是 </strong> 里那个，包上去就把闭合标签劈成了
        # `<<code>/</code>strong>`，页面上多出一个孤儿 <strong>。这一类
        # 单字符内文（/ 和 .）最容易踩到，务必先排掉标签内部的位置。
        if ok and any(x <= k and k + n <= y for x, y in tags):
            ok = False
        if ok and word:
            ok = ((k == 0 or not _wordchar(val[k - 1]))
                  and (k + n == len(val) or not _wordchar(val[k + n])))
        if ok:
            return k
        k = val.find(inner, k + 1)
    return None


def straddles(items, pairs, ms, me):
    """有没有「一半被吞掉、一半留在外面」的行内标签对。

    有就不能替换：留在外面的那半个会被原样输出，被吞掉的半个却指望
    opens/closes 去还原 —— 一半对一半，页面里就多出孤儿标签。宁可留英文。
    区间取闭区间，与 `splice` 的吞掉范围保持一致。
    """
    for i, j in pairs.items():
        if i > j:
            continue                       # 只看开标签那一侧
        a = ms <= items[i][1] <= me
        b = ms <= items[j][1] <= me
        if a != b:
            return True
    return False


def plan_match(F, items, toks, pairs, ms, me, val, stats):
    """定下这一段里每个行内标签的去留。

    返回 (opens, closes, 新译文)；返回 None 表示这次替换放弃（宁可留英文）。
    """
    if straddles(items, pairs, ms, me):
        return "标签对跨越了命中边界"
    code_pairs, style_pairs = [], []
    for i, it in enumerate(items):
        if it[0] != "z" or not (ms <= it[1] <= me):
            continue
        raw = toks[it[3]][1]
        if i not in pairs:                 # 落单的标签：原样留着，不能吞掉
            style_pairs.append((it[1], True, raw, ""))
            continue
        j = pairs[i]
        if i > j or not (ms <= items[j][1] <= me):
            continue                       # 只看开标签那一侧，且伙伴要在范围内
        end = toks[items[j][3]][1]
        whole = (it[1] == ms and items[j][1] == me)
        if tag_name(raw) == "code":
            inner = "".join(toks[x][1] for x in range(it[3] + 1, items[j][3]))
            code_pairs.append((inner, it[1], whole, raw, end))
        elif tag_name(raw) in DROPPABLE:
            style_pairs.append((it[1], whole, raw, end))

    # 长的（外层的）先占位：英文里 <code>WHERE [condition]</code> 套着
    # <code>[condition]</code>，外层先认领 "WHERE [condition]"，内层就退到
    # 句子后面那个单独的 [condition] 上去包 —— 各自落在自己的位置上，
    # 既不会套娃，也不会白丢一层等宽。
    # taken 只装「这次新加」的包裹范围。译文里本来就有的 <code>（子代理自己
    # 写对的，比如 对于树 <code>t</code>：）不算占位 —— 它正是我们要的结果，
    # 那一段就该直接认领，而不是逼着内文另找一个地方去包。
    spans = _code_spans(val)
    used, taken, edits = set(), [], []
    for inner, at, whole, raw, end in sorted(code_pairs, key=lambda t: -len(t[0])):
        pos = find_code_slot(val, inner, used, taken)
        if pos is None:
            # 译文里没有这段内文 —— 中文把 the player <code>who</code> will say i
            # 写成了「将要说出 i 的玩家」，who 这个词整个消失了。此时绝不能
            # 「整段作废退回英文」：那会在页面上留下一整句没有翻译的英文，比
            # 少一层等宽样式严重得多。丢掉这一对 <code> 即可（whole 的情形本
            # 来就是原样保留标签本身，不受影响）。
            if whole:                      # 整段就是一个 <code> —— 包住译文
                style_pairs.append((at, True, raw, end))
            else:
                stats["丢code内文"] += 1
                if VERBOSE:
                    stats.setdefault("丢code内文样例", []).append(
                        (inner[:40], val[:60]))
            continue
        used.add(pos)
        if not any(a <= pos < b for a, b in spans):
            taken.append((pos, pos + len(inner)))
            edits.append((pos, inner))     # 译文里已经带 <code> 就不再包

    opens, closes = [], []
    for _, whole, raw, end in sorted(style_pairs):
        if whole:                          # 整段就是这个样式标签 —— 保留
            if raw.startswith("</"):
                closes.append(raw)
            else:
                # 译文自己已经带了这层标签（词条里写好了 <strong>…</strong>），
                # 就不要再从外面套一层，否则会套成 <strong><strong>…
                if end and ("<%s" % tag_name(raw)) in val:
                    continue
                opens.append(raw)
                if end:
                    closes.append(end)
        else:
            stats["丢样式"] += 1
            if VERBOSE:
                stats.setdefault("丢样式样例", []).append(
                    (F[ms:me][:70], val[:70]))
    for pos, inner in sorted(edits, reverse=True):
        val = val[:pos] + "<code>" + inner + "</code>" + val[pos + len(inner):]
    return opens, closes, val


def splice(F, items, toks, anchors, matches, stats):
    """把 matches 应用到 run 上，返回 HTML 文本；全被拒则返回 None。"""
    pairs = pair_tags(items, toks)

    planned = []
    for ms, me, val in matches:
        need = anchors_in(items, 0, ms, me)
        if need == [-1] or not check_value(
                val, anchors, [items[i][3] for i in need], stats):
            stats["链接放弃"] += 1
            REJECTS.append((F[ms:me], val, "链接占位符没写回"))
            continue
        pl = plan_match(F, items, toks, pairs, ms, me, val, stats)
        if isinstance(pl, str):
            stats["保标签放弃"] += 1
            REJECTS.append((F[ms:me], val, pl))
            continue
        planned.append((ms, me) + pl)
    if not planned:
        return None

    # 文字一律按 F 上的区间吐，item 只当「标签该插在哪」的坐标用。
    # 不能按 item 整体吐：一个文字 item 可能横跨命中边界（比如整句是一个
    # <strong>，而命中的只是句子中间一个术语），整体吐出去再回头吐命中段，
    # 就会漏字重字、把 fp 往回拨。
    res, ii, fp = [], 0, 0

    def tag_at(i):
        it = items[i]
        return anchors[it[3]] if it[0] == "A" else toks[it[3]][1]

    def emit_upto(limit):
        """吐出位置 < limit 的标签（连带它们之间的文字）。"""
        nonlocal ii, fp
        while ii < len(items) and items[ii][1] < limit:
            it = items[ii]
            if it[0] != "t":
                if it[1] > fp:
                    res.append(F[fp:it[1]])
                    fp = it[1]
                res.append(tag_at(ii))
            ii += 1
        if limit > fp:
            res.append(F[fp:limit])
            fp = limit

    def emit_rest():
        """收尾：位置正好等于 len(F) 的标签也要吐出来。"""
        nonlocal ii, fp
        while ii < len(items):
            it = items[ii]
            if it[0] != "t":
                if it[1] > fp:
                    res.append(F[fp:it[1]])
                    fp = it[1]
                res.append(tag_at(ii))
            ii += 1
        if len(F) > fp:
            res.append(F[fp:])
            fp = len(F)

    for ms, me, opens, closes, val in planned:
        emit_upto(ms)
        # 闭区间：零宽标签正好落在 me 上时也要吞掉并由 opens/closes 还原，
        # 否则收尾时会把它原样再吐一遍（</b> 就是这么变成两份的）
        while ii < len(items) and items[ii][1] <= me:
            ii += 1                        # 范围内的标签已由 plan_match 定夺
        res.extend(opens)
        res.append(PLACEHOLDER_RE.sub(lambda m: anchors[int(m.group(1))], val))
        res.extend(reversed(closes))
        fp = me
    emit_rest()
    return "".join(res)


def translate_anchor_text(html, exact, sub, stats):
    """链接文字（<a …>文字</a>）过一遍词条：整段相等才替换。

    两张表都要查。长度 ≥ SUB_MIN 的词条平时只进 sub、只用于正文的**子串**
    替换（见 split_dict），但链接文字天生就是一段独立完整的文本，整段相等
    即可安全替换。只查 exact 的话，长词条在侧边栏目录里永远翻不到 ——
    "Download starter files"（22 字符）就一直留着英文，而同一页的
    "Rules"（5 字符）翻了，目录变成中英夹杂。
    """
    def _f(m):
        key = norm(m.group(2))
        zh = exact.get(key) or sub.get(key) if key else None
        if zh:
            stats["链接文字"] += 1
            return m.group(1) + zh + m.group(3)
        return m.group(0)

    return ANCHOR_RE.sub(_f, html)


# ------------------------------------------------------------------ 主流程

# 标题形如「<主题> | CS 61A Summer 2026」；首页的标题没有主题，只有后半截，
# 所以前半截整体可选，否则首页标题永远匹配不上、原样留英文。
TITLE_SEP_RE = re.compile(r"^(?:(.*?)\s*\|\s*)?CS 61A Summer 2026\s*$", re.S)
MAIN_RE = re.compile(r"<main\b.*?</main>", re.S)


def replace_plain(fragment, exact, pat, sub):
    """对非正文片段（如 <title>）做整段/子串替换，返回 (新文本, 次数)。"""
    t = norm(fragment)
    if t in exact:
        return exact[t], 1
    if pat is None:
        return fragment, 0
    n = 0

    def _f(m):
        nonlocal n
        n += 1
        return sub[norm(m.group(1))]

    return pat.sub(_f, fragment), n


def apply_main(region, exact, pat, sub, stats):
    toks = tokenize(region)
    out, i = [], 0
    for F, items, anchors, lo, hi in runs_of(region):
        while i < lo:                      # run 之间的块级/代码标签原样输出
            out.append(toks[i][1])
            i += 1
        matches = run_matches(F, exact, pat, sub, stats)
        new = splice(F, items, toks, anchors, matches, stats) if matches else None
        if new is None:                    # 没命中：原文照搬（链接文字仍可译）
            new = "".join(toks[x][1] for x in range(lo, hi))
        out.append(translate_anchor_text(new, exact, sub, stats))
        i = hi
    while i < len(toks):
        out.append(toks[i][1])
        i += 1
    return "".join(out)


def process(path, exact, pat, sub, stats):
    with open(path, encoding="utf-8") as f:
        s0 = f.read()
    s = s0.replace('<html lang="en">', '<html lang="zh-CN">')

    m = re.search(r"<title>(.*?)</title>", s, re.S)
    if m:
        core = TITLE_SEP_RE.match(m.group(1))
        if core:
            body = (core.group(1) or "").strip()
            # 主题查不到词条时保持英文（如项目名 Ants Vs. SomeBees），
            # 但后缀一定要换成中文 —— 早先只在主题被译时才换，于是
            # 「Discussion 1」这类没有词条的主题整条标题都留了英文。
            newbody, _ = replace_plain(body, exact, pat, sub) if body else ("", 0)
            new = "%s | CS 61A 2026 暑期" % newbody if newbody else "CS 61A 2026 暑期"
            if new != norm(m.group(1)):
                stats["标题"] += 1
                s = s[:m.start(1)] + new + s[m.end(1):]

    mm = MAIN_RE.search(s)
    if mm:
        s = (s[:mm.start()] + apply_main(mm.group(0), exact, pat, sub, stats)
             + s[mm.end():])

    if s != s0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
        return True
    return False


def load_skip():
    """不必翻译的段落（数据值、标识符、人名、函数名…）。

    子代理在批次里回 null 的条目会由 batches.py --merge 记到这里，下一轮
    --check 就不会再把它们当成待译任务，剩余量才是真实的任务量。
    """
    path = os.path.join(I18N, "skip.json")
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        return {norm(k) for k in json.load(f)}


def check(exact, pat):
    """统计还有多少段落没被翻译，写出 _todo.jsonl。

    必须在**应用术语表之前**跑（run_all.py 里就是这么排的）：它数的是当前
    站点里还没被翻掉的那部分，也就是「已经过阶段 A 清理、剩下的英文正文」。
    跑在翻译之后就只会数出一堆中文段落，白忙一场。
    """
    skip = load_skip()
    cnt = Counter()
    for p in pages():
        with open(p, encoding="utf-8") as f:
            region = content_region(f.read())
        if region is None:
            continue
        for flat, _, _, _, _ in runs_of(region):
            t = flat.strip()
            if not t or norm(t) in exact or norm(t) in skip:
                continue
            rest = pat.sub("", t) if pat else t
            if not re.search(r"[A-Za-z]{3}", rest):
                continue
            cnt[t] += 1
    with open(os.path.join(ROOT, "_todo.jsonl"), "w", encoding="utf-8",
              newline="\n") as f:
        for t, n in cnt.most_common():
            f.write(json.dumps({"n": n, "t": t}, ensure_ascii=False) + "\n")
    print("未翻译段落：%d 个不同 / %d 次出现 → 已写出 _todo.jsonl"
          % (len(cnt), sum(cnt.values())))


def main():
    d = load_dict()
    exact, pat, sub = split_dict(d)
    print("术语表：%d 条（整段 %d / 子串 %d）" % (len(d), len(exact), len(sub)))

    if "--check" in sys.argv:
        check(exact, pat)
        return

    stats = Counter()
    n = 0
    for p in pages():
        if process(p, exact, pat, sub, stats):
            n += 1
    print("翻译完成：改写 %d 个页面。" % n)

    if REJECTS:
        seen, rows = set(), []
        for en, zh, why in REJECTS:
            k = norm(en)
            if k in seen:
                continue
            seen.add(k)
            rows.append({"en": en, "zh": zh, "why": why})
        with open(os.path.join(ROOT, "_rejected.jsonl"), "w", encoding="utf-8",
                  newline="\n") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("  ！有 %d 段查到了词条却没能应用（见 _rejected.jsonl）" % len(rows))
    for k in ("整段", "子串", "标题", "链接文字", "丢样式", "丢code内文",
              "链接放弃", "保标签放弃", "可疑标签"):
        if stats[k]:
            print("  %s：%d" % (k, stats[k]))
    if VERBOSE:
        for a, b in stats.get("丢样式样例", [])[:20]:
            print("   [丢样式]", a, "→", b)
        for a, b in stats.get("丢code内文样例", [])[:20]:
            print("   [丢code内文]", a, "→", b)
        for a, b in stats.get("可疑样例", [])[:20]:
            print("   [可疑标签]", a, b)


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
