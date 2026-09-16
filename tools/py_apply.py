"""把 .py 译文写回起始代码包，重新打包。

译文按「扁平文本」存成术语表 py_zh.json（由 pNN.json + pNN.zh.json 合成），
写回时逐段查表。每段的替换是**行数对齐**的（见 pytext.spread）：译文摊成
恰好与原段落相同的行数，因此行号一个都不平移，文件形状不变。

打包保留原 zip 的每一个字节细节：条目顺序、压缩方式、时间戳、权限位，
连 ok 那个已打过补丁的 zipapp 也是原样搬运。只有被替换的 .py 条目内容变。

    python tools/py_apply.py --check     # 只报会改哪些文件、多少段，不写
    python tools/py_apply.py --export    # 另存到 _py_zh/ 供人工校对，也不写
    python tools/py_apply.py             # 真正写回并重新打包
"""
import glob
import io
import json
import os
import shutil
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytext

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "cs61a_offline")
PYDIR = os.path.join(ROOT, "tools", "i18n", "py")
EXPORT = os.path.join(ROOT, "_py_zh")


def norm(s):
    return " ".join(s.split())


def glossary():
    """{扁平英文: 中文} —— 合并所有已收回的批次。"""
    d, miss = {}, []
    for q in sorted(glob.glob(os.path.join(PYDIR, "p??.json"))):
        if q.endswith(".zh.json"):
            continue
        a = q[:-5] + ".zh.json"
        if not os.path.exists(a):
            miss.append(os.path.basename(a))
            continue
        items = json.load(open(q, encoding="utf-8"))
        ans = json.load(open(a, encoding="utf-8"))
        for it in items:
            v = ans.get(str(it["id"]))
            if v and v.strip():
                d[norm(it["en"])] = v.strip()
    return d, miss


def rewrite(src, d, un):
    """一个 .py 的译文版；un 收集没查到译文的段落。"""
    edits = []
    for seg in pytext.scan(src):
        pin = seg.get("prefix")
        if pin:
            # 「E.g., <返回值示例>」：示例是学生必须逐字返回的字符串，只译引导词。
            # 这条规则写在 pytext 里（要与同 docstring 的 doctest 期望输出对上），
            # 这里直接照做，不查术语表 —— 免得某次翻译又把它译成中文。
            zh = pytext.EXAMPLE_ZH.get(pin.strip(), "例如，") \
                + seg["en"][len(pin):]
            edits.append((seg, zh))
            continue
        zh = d.get(norm(seg["en"]))
        if zh is None:
            un.append(seg["en"])
            continue
        edits.append((seg, zh))
    if not edits:
        return src, 0
    return pytext.apply_edits(src, edits), len(edits)


def repack(zpath, repl):
    """repl: {包内路径: 新字节}。其余条目原样搬运。"""
    tmp = zpath + ".tmp"
    with zipfile.ZipFile(zpath) as src, \
            zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            data = repl.get(info.filename) or src.read(info.filename)
            dst.writestr(info, data)        # info 复用 → 时间戳/权限/压缩方式不变
    os.replace(tmp, zpath)


def main():
    check = "--check" in sys.argv
    export = "--export" in sys.argv
    d, miss = glossary()
    print("术语表：%d 条" % len(d))
    if miss:
        print("  ! 还没收到的批次：%s" % miss)

    if export and os.path.isdir(EXPORT):
        shutil.rmtree(EXPORT)

    # dedup=False：内容相同的包也要逐个写回，否则另一份留在英文
    byzip = {}
    for zpath, name in pytext.targets(dedup=False):
        byzip.setdefault(zpath, []).append(name)

    un, nfile, nseg, changed = [], 0, 0, []
    for zpath in sorted(byzip):
        repl, hits = {}, 0
        with zipfile.ZipFile(zpath) as z:
            for name in byzip[zpath]:
                try:
                    src = z.read(name).decode("utf-8")
                except (KeyError, UnicodeDecodeError):
                    continue
                out, k = rewrite(src, d, un)
                if not k:
                    continue
                nfile += 1
                hits += k
                if out != src:
                    repl[name] = out.encode("utf-8")
                    if export:
                        # 包内路径的首层通常就是包名，与 zip 所在目录同名
                        # （hw/hw01/hw01.zip 里是 hw01/hw01.py）。照搬会导出成
                        # hw/hw01/hw01/hw01.py，同名校对时白多点两层，去掉它。
                        stem, _, rest = name.partition("/")
                        if rest and stem == os.path.basename(
                                os.path.dirname(zpath)):
                            name = rest
                        p = os.path.join(EXPORT, os.path.relpath(
                            os.path.dirname(zpath), SITE).replace(os.sep, "/"),
                            name)
                        os.makedirs(os.path.dirname(p), exist_ok=True)
                        with open(p, "w", encoding="utf-8", newline="\n") as f:
                            f.write(out)
        if repl:
            nseg += hits
            changed.append((os.path.relpath(zpath, ROOT), len(repl)))
            # --export 只是「导出给人看」，和 --check 一样不落盘：校对没过之前
            # 不该动真包。写回必须显式无参数运行。
            if not check and not export:
                repack(zpath, repl)

    print("%s：%d 个 .py / %d 段；未查到译文 %d 段"
          % ("将写回" if check else "已写回", nfile, nseg, len(un)))
    for p, n in changed:
        print("   %-46s %d 个文件" % (p, n))
    if un:
        print("  未查到译文的段落（保持英文）：")
        for s in sorted(set(un))[:20]:
            print("   ", s[:90])


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
