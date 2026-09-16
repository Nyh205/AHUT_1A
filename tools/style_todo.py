"""找出「该有加粗/斜体、译文里却没了」的段落，生成补标记的批次。

翻译输入是扁平文本（看不见标签），子代理自然写不出 <strong>。判据很简单：
英文该段里出现了 <strong>/<em>，且英文去标签后正好是某条术语的 key —— 这种
段落的中文已经在词条里定稿，补标记不会碰任何字词，最稳。

    python tools/style_todo.py       # → tools/i18n/style/sNN.json
    python tools/style_merge.py      # 收 sNN.zh.json 并回写术语表
"""
import glob
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import segments

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP = os.path.join(ROOT, "_backup_en")
DICT = os.path.join(ROOT, "tools", "i18n", "batch_zh.json")
OUT = os.path.join(ROOT, "tools", "i18n", "style")
DIRS = ["lab", "hw", "disc", "proj"]
WANT = ("strong", "em", "b", "i")
SIZE = 140


def main():
    d = json.load(open(DICT, encoding="utf-8"))
    norm = lambda s: " ".join(s.split())            # noqa: E731
    bykey = {norm(k): k for k in d}

    pages = []
    for x in DIRS:
        pages += glob.glob(os.path.join(BACKUP, x, "**", "index.html"),
                           recursive=True)

    rows, seen = [], set()
    for p in sorted(pages):
        region = segments.content_region(open(p, encoding="utf-8").read())
        if region is None:
            continue
        toks = segments.tokenize(region)
        for flat, _items, _anchors, lo, hi in segments.runs_of(region):
            key = norm(flat.strip())
            if key in seen or key not in bykey:
                continue
            names = [segments.tag_name(t[1]) for t in toks[lo:hi]
                     if t[0] == "inline"]
            if not any(t in names for t in WANT):
                continue
            # 把这一段按原样渲染回带标签的英文，让子代理看得见哪几个词是粗体。
            # 超链接照 build_run 的规矩落成 {k}，和译文里的占位符对得上。
            out, i, ai = [], lo, 0
            while i < hi:
                kind, pay = toks[i]
                if kind == "text":
                    out.append(pay)
                    i += 1
                    continue
                if segments.tag_name(pay) == "a" and not pay.startswith("</"):
                    j = segments._anchor_end(toks, i, hi)
                    if j is not None:
                        out.append("{%d}" % ai)
                        ai += 1
                        i = j + 1
                        continue
                out.append(pay)
                i += 1
            seen.add(key)
            rows.append({"id": len(rows), "en": "".join(out),
                         "zh": d[bykey[key]]})

    os.makedirs(OUT, exist_ok=True)
    for old in glob.glob(os.path.join(OUT, "s*.json")):
        os.remove(old)
    for n in range(0, len(rows), SIZE):
        path = os.path.join(OUT, "s%02d.json" % (n // SIZE))
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(rows[n:n + SIZE], f, ensure_ascii=False, indent=1)
    print("待补标记：%d 段 → %d 批 → %s"
          % (len(rows), (len(rows) + SIZE - 1) // SIZE, OUT))


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
