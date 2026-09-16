"""结构体检：把「翻译前 / 翻译后」的关键指标比一遍。

翻译只该动「给人看的英文」，其它一律不许变。所以每页记录这些指标：

  div        开合标签数（必须相等，且与基线一致）
  pre        <pre> 个数（代码块一个都不能少）
  doctest    <pre> 里以 &gt;&gt;&gt; 开头的行数（文档测试是评分依据）
  slot       <div class="solution/alt ..."> 答案槽个数
  code       <code> 标签个数
  script     <script> 个数
  underscore ______ 占位符个数
  href       所有 href 的排序指纹（链接不能被改动）

用法：
    python tools/verify.py --snap     # 存基线 _baseline.json
    python tools/verify.py            # 与基线比对
"""
import glob
import hashlib
import io
import json
import os
import re
import sys

from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "cs61a_offline")
BASE = os.path.join(ROOT, "_baseline.json")
DIRS = ["lab", "hw", "disc", "proj"]
ROOT_PAGES = ["index.html"]     # 与 segments.ROOT_PAGES 保持一致

PRE_RE = re.compile(r"<pre\b.*?</pre>", re.S)
HREF_RE = re.compile(r'href\s*=\s*"([^"]*)"')
# 行内标签必须成对。翻译会按语义重组句子，某个 <code>x</code> 可能因为
# 中文里不再单独出现 x 而合理地少一个 —— 但绝不能出现「有开没闭」的孤儿标签。
INLINE_TAGS = ["code", "strong", "em", "b", "i", "a", "span", "kbd", "var",
               "tt", "samp", "cite", "abbr", "sub", "sup", "small", "big"]
OPEN_RE = re.compile(r"<(%s)\b" % "|".join(INLINE_TAGS))
CLOSE_RE = re.compile(r"</(%s)\s*>" % "|".join(INLINE_TAGS))


def metrics(path):
    s = open(path, encoding="utf-8").read()
    pres = PRE_RE.findall(s)
    doctest = sum(1 for p in pres for ln in p.splitlines()
                  if ln.strip().startswith("&gt;&gt;&gt;")
                  or ln.strip().startswith(">>>"))
    # 源站自己有一处畸形锚点 `<a href=">`（缺地址和引号），正则会把后面一大段
    # 正文当成 href 值吞进来 —— 译文一变长，这个「值」就跟着变。它不是链接，
    # 滤掉，否则 href 指标永远报警。
    hrefs = [h for h in HREF_RE.findall(s) if "<" not in h]
    opens = Counter(OPEN_RE.findall(s))
    closes = Counter(CLOSE_RE.findall(s))
    # 记「开-闭」的差，不记两个原始个数：源站本身就有极少数畸形标记
    # （有 </a> 没 <a>），那属于原样保留的前提，只要差值和英文版一致就没被改坏。
    unbal = sorted([t, opens[t] - closes[t]] for t in set(opens) | set(closes)
                   if opens[t] != closes[t])
    return {
        "len": len(s),
        "unbal": unbal,
        "div": s.count("<div") - s.count("</div>"),
        "divn": s.count("<div"),
        "pre": len(pres),
        "doctest": doctest,
        "slot": len(re.findall(r'<div class="(?:solution|alt)\b', s)),
        "code": s.count("<code"),
        "script": s.count("<script"),
        "underscore": s.count("______"),
        "href": hashlib.md5(
            "\n".join(sorted(hrefs)).encode("utf-8")).hexdigest()[:12],
        "hrefn": len(hrefs),
    }


def pages():
    out = []
    for d in DIRS:
        for root, _, files in os.walk(os.path.join(SITE, d)):
            if "index.html" in files:
                out.append(os.path.relpath(os.path.join(root, "index.html"),
                                           ROOT).replace(os.sep, "/"))
    for p in ROOT_PAGES:
        f = os.path.join(SITE, p)
        if os.path.exists(f):
            out.append(os.path.relpath(f, ROOT).replace(os.sep, "/"))
    return sorted(set(out))


def main():
    snap = "--snap" in sys.argv
    cur = {p: metrics(os.path.join(ROOT, p)) for p in pages()}

    if snap:
        with open(BASE, "w", encoding="utf-8", newline="\n") as f:
            json.dump(cur, f, ensure_ascii=False, indent=1, sort_keys=True)
        print("基线已保存：%d 个页面 → _baseline.json" % len(cur))
        return

    with open(BASE, encoding="utf-8") as f:
        old = json.load(f)

    bad = 0
    for p in sorted(cur):
        o, n = old.get(p), cur[p]
        if o is None:
            print("[新增] %s" % p)
            bad += 1
            continue
        diff = {k: (o[k], n[k]) for k in o if o[k] != n[k]}
        if diff:
            bad += 1
            print("[不一致] %s" % p)
            for k, (a, b) in diff.items():
                print("    %-10s %s → %s" % (k, a, b))
    if not bad:
        print("结构体检通过：%d 个页面全部一致。" % len(cur))
    else:
        print("有 %d 个页面与基线不一致。" % bad)


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
