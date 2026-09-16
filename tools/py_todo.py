"""把 .py 起始代码里该翻的段落抽出来，分成批次交给子代理。

翻的是 docstring 正文和 # 注释（见 pytext.py）。同一条英文可能出现在好几个
包里（lab 和 sol-lab 共用一份 hailstone 说明），先去重，翻一份就够 ——
术语表 py_zh.json 按「扁平文本」存，写回时逐条查表。

子代理只看到 {id, en}，看不到文件、也看不到任何代码上下文：这样它们不会
想着去「顺手改一下代码」。写回由 py_apply.py 独立完成。

    python tools/py_todo.py          # → tools/i18n/py/pNN.json
    python tools/py_apply.py         # 收 pNN.zh.json，写回并重新打包
"""
import glob
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytext

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "i18n", "py")
SIZE = 120


def norm(s):
    return " ".join(s.split())


def collect(skip=()):
    """[{id, en}] —— 按段落英文去重，跳过 skip 里已有的 key。"""
    rows, seen = [], set(skip)
    import zipfile
    for zpath, name in pytext.targets():
        try:
            with zipfile.ZipFile(zpath) as z:
                src = z.read(name).decode("utf-8")
        except (KeyError, UnicodeDecodeError):
            continue
        for seg in pytext.scan(src):
            key = norm(seg["en"])
            if key in seen:
                continue
            seen.add(key)
            rows.append({"id": len(rows), "en": seg["en"]})
    return rows


def existing():
    """已经出过批次的 key，以及下一个可用的批次号。"""
    keys, nxt = set(), 0
    for p in sorted(glob.glob(os.path.join(OUT, "p??.json"))):
        if p.endswith(".zh.json"):
            continue
        nxt = max(nxt, int(os.path.basename(p)[1:3]) + 1)
        for it in json.load(open(p, encoding="utf-8")):
            keys.add(norm(it["en"]))
    return keys, nxt


def main():
    """--delta：sol-* 包比普通包多出的那几段，只补新的，不动已发的批次。"""
    os.makedirs(OUT, exist_ok=True)
    delta = "--delta" in sys.argv
    if delta:
        done, nxt = existing()
        rows = collect(done)
    else:
        for old in os.listdir(OUT):
            if old.startswith("p") and old.endswith(".json"):
                os.remove(os.path.join(OUT, old))
        nxt, rows = 0, collect()
    for n in range(0, len(rows), SIZE):
        path = os.path.join(OUT, "p%02d.json" % (nxt + n // SIZE))
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(rows[n:n + SIZE], f, ensure_ascii=False, indent=1)
    print("待翻段落：%d 段 → 从 p%02d 起 → %s"
          % (len(rows), nxt, OUT))


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
