"""把「补回来的加粗/斜体标记」并回术语表。

翻译是按「扁平文本」（看不见标签的句子）做的，子代理看不到哪里是粗体，于是
<strong>/<em> 在译文里整片消失 —— 页面上原本加粗的 **Hint:**、**定义：** 全变成
普通文字，视觉结构塌了一半。

补救不必重译：英文段落和它已定稿的中文都还在，只要把标记安回中文里对应的位置
即可。style_todo 生成 sNN.json（带标记的英文 + 裸中文），子代理产出 sNN.zh.json
（把标记插回去的中文），这个脚本按「英文去掉标签」还原成术语表的 key 写回去。

    python tools/style_todo.py       # 生成 tools/i18n/style/sNN.json
    python tools/style_merge.py      # 收 sNN.zh.json → tools/i18n/batch_zh.json
"""
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLE = os.path.join(ROOT, "tools", "i18n", "style")
DICT = os.path.join(ROOT, "tools", "i18n", "batch_zh.json")
TAG_RE = re.compile(r"</?(?:strong|em|b|i|code|span|u|s|small|big|kbd|var|tt|"
                    r"samp|cite|abbr|dfn|mark|time|q|font|sub|sup|del|ins)\b[^>]*>")


def flat(s):
    """带标记的英文 → 术语表的 key（去标签、压空白）。"""
    return " ".join(TAG_RE.sub("", s).split())


def merge():
    with open(DICT, encoding="utf-8") as f:
        d = json.load(f)
    bykey = {flat(k): k for k in d}
    n, miss, bad = 0, [], []
    for qpath in sorted(glob.glob(os.path.join(STYLE, "s??.json"))):
        apath = qpath[:-5] + ".zh.json"
        if not os.path.exists(apath):
            miss.append(os.path.basename(qpath))
            continue
        items = json.load(open(qpath, encoding="utf-8"))
        ans = json.load(open(apath, encoding="utf-8"))
        for it in items:
            k = str(it["id"])
            v = ans.get(k)
            if not v:
                bad.append(k)
                continue
            key = bykey.get(flat(it["en"]))
            if key is None:
                bad.append("no-key:" + k)
                continue
            d[key] = v
            n += 1
    with open(DICT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=1, sort_keys=True)
    print("补回标记 %d 条 → %s（共 %d 条）" % (n, DICT, len(d)))
    if bad:
        print("  ! %d 条没有可用译文，例如 %s" % (len(bad), bad[:5]))
    if miss:
        print("  还没收到的批次：%s" % miss)


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    merge()
