"""把待译段落切成批次、收回来合并成术语表。

分段翻译交给子代理做：它们只看到「编号 + 英文」，只回「编号 → 中文」，
不碰 HTML 一个字符，所以结构绝不会被改坏。

    python tools/batches.py --make 200      # 生成 tools/i18n/batches/bNN.json
    python tools/batches.py --merge         # 收 tools/i18n/batches/bNN.zh.json
                                            # → tools/i18n/batch_zh.json

批次输入  bNN.json   : [{"id": 12, "en": "..."}, ...]
批次输出  bNN.zh.json: {"12": "译文", ...}   （id 为字符串）
   译文填 null 或与原文相同 = 这段是代码/标识符，不要翻译。
"""
import glob
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, "tools", "i18n", "batches")
OUT = os.path.join(ROOT, "tools", "i18n", "batch_zh.json")
SKIP = os.path.join(ROOT, "tools", "i18n", "skip.json")


def read_todo():
    rows = []
    with open(os.path.join(ROOT, "_todo.jsonl"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def make(size):
    rows = read_todo()
    os.makedirs(BATCH_DIR, exist_ok=True)
    for old in glob.glob(os.path.join(BATCH_DIR, "*.json")):
        os.remove(old)
    n = 0
    for i in range(0, len(rows), size):
        chunk = rows[i:i + size]
        items = [{"id": i + j, "en": r["t"]} for j, r in enumerate(chunk)]
        path = os.path.join(BATCH_DIR, "b%02d.json" % n)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(items, f, ensure_ascii=False, indent=1)
        n += 1
    print("切成 %d 个批次，共 %d 段 → %s" % (n, len(rows), BATCH_DIR))


def merge():
    """收 bNN.zh.json，和它的题面 bNN.json 配对后写进术语表。

    英文取自批次文件本身，不查 _todo.jsonl —— 那样一旦 _todo 重排（新增或
    修好一段，编号就全变），旧批次的内容就会被张冠李戴地塞进别的词条。
    """
    out, skip, missing, bad = {}, set(), [], []
    for qpath in sorted(glob.glob(os.path.join(BATCH_DIR, "b??.json"))):
        apath = qpath[:-5] + ".zh.json"
        if not os.path.exists(apath):
            missing.append(os.path.basename(qpath))
            continue
        with open(qpath, encoding="utf-8") as f:
            items = json.load(f)
        with open(apath, encoding="utf-8") as f:
            ans = json.load(f)
        for it in items:
            k = str(it["id"])
            if k not in ans:
                bad.append((os.path.basename(apath), k))
                continue
            v, en = ans[k], it["en"]
            # 译文为空或与原文相同 = 这段是代码/标识符/数据，不该翻译
            if not v or not v.strip() or v.strip() == en.strip():
                skip.add(" ".join(en.split()))
                continue
            out[" ".join(en.split())] = v

    prev = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            prev = json.load(f)
    prev.update(out)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(prev, f, ensure_ascii=False, indent=1, sort_keys=True)

    old_skip = set()
    if os.path.exists(SKIP):
        with open(SKIP, encoding="utf-8") as f:
            old_skip = set(json.load(f))
    new_skip = sorted(old_skip | skip)
    with open(SKIP, "w", encoding="utf-8", newline="\n") as f:
        json.dump(new_skip, f, ensure_ascii=False, indent=1)

    print("合并 %d 条（累计 %d 条）→ %s" % (len(out), len(prev), OUT))
    print("  另记 %d 段「不必翻译」（累计 %d 段）→ %s"
          % (len(skip), len(new_skip), SKIP))
    if bad:
        print("  有 %d 个编号没有译文，例如 %s" % (len(bad), bad[:3]))
    if missing:
        print("  还没收到译文的批次：%s" % missing)


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if "--make" in sys.argv:
        make(int(sys.argv[sys.argv.index("--make") + 1]))
    else:
        merge()
