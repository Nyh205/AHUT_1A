"""按正确顺序跑完整条中文化流水线。

这几个脚本有先后依赖，且 localize_pages.py 依赖「英文原版」这一前提才能
幂等（例如它删掉的 <div> 外壳不会再出现）。所以重跑时先恢复到英文原版：

    恢复页面/zip  →  translate_nav.py  →  prune_nav.py  →  localize_pages.py
    →  prune_site.py  →  translate_text.py  →  rename_course.py
    →  patch_ok_local.py  →  py_apply.py

rename_course.py 必须排在翻译之后 —— 词表里有多条 key 含 "CS 61A"，提前改名
会让它们失配、整段漏翻，所以它跟着翻译走，不能单独跑。

用法：
    python tools/run_all.py          # 全量重跑（先恢复英文原版）
    python tools/run_all.py --keep   # 不恢复，只在当前状态上继续做增量清理

    --no-translate   跳过 translate_text 与 rename_course
    --no-rename      只跳过 rename_course
    --no-py          跳过起始代码包那两步
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "cs61a_offline")
BACKUP = os.path.join(ROOT, "_backup_en")
DIRS = ["lab", "hw", "disc", "proj"]
# 站根下也参与流水线的单页（首页），与 segments.ROOT_PAGES 一致
ROOT_PAGES = ["index.html"]
# 这些页面已人工逐句翻译，不能从英文备份覆盖。
# 副作用：它永远停在上一轮跑完的样子，所以 rename_course.py 报的替换数在首轮
# 之后会少 3 处（该页的 <title>、导航栏品牌、meta description）—— 只是计数差，
# 页面内容两轮完全一致，因为改名本身幂等。
SKIP_RESTORE = {"lab/lab00/index.html"}


def restore():
    """把 _backup_en 里的英文原版页面全部拷回去。

    不只恢复教学页：prune_site.py 还会改 <head> 与页脚，而带页脚的是
    articles/、exam/、resources/ 这些外围页面，它们也得从原版重来，
    否则规则一改就没法重新推导。备份里共 109 个 html。
    """
    n = 0
    for root, _, files in os.walk(BACKUP):
        for f in files:
            if not f.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(root, f), BACKUP)
            if rel.replace(os.sep, "/") in SKIP_RESTORE:
                continue
            shutil.copy2(os.path.join(BACKUP, rel), os.path.join(SITE, rel))
            n += 1
    print("恢复英文原版页面：%d 个" % n)


def restore_zips():
    """起始代码包也要从英文备份恢复，否则 py_apply 没有「英文原版」可依。

    恢复会一并抹掉 ok 的本地化补丁，所以后面必须重跑 patch_ok_local.py。
    """
    n = 0
    for root, _, files in os.walk(BACKUP):
        for f in files:
            if not f.endswith(".zip"):
                continue
            src = os.path.join(root, f)
            dst = os.path.join(SITE, os.path.relpath(src, BACKUP))
            shutil.copy2(src, dst)
            n += 1
    print("恢复英文原版起始代码包：%d 个" % n)


def run(script, *args):
    print("--- %s %s ---" % (script, " ".join(args)))
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", script)] + list(args),
                   cwd=ROOT, check=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--keep" not in sys.argv:
        restore()
        restore_zips()
    for s in ["translate_nav.py", "prune_nav.py", "localize_pages.py",
              "prune_site.py"]:
        run(s)
    # 顺序要紧：--check 数的是「清理完还没翻的英文」，必须在应用术语表之前跑
    if "--no-translate" not in sys.argv:
        run("translate_text.py", "--check")
        run("translate_text.py")
        # 课程名替换跟在翻译之后，且只在翻译跑过时才跑：它一旦提前，
        # 词表里含 "CS 61A" 的那些 key 就再也匹配不上了。
        if "--no-rename" not in sys.argv:
            run("rename_course.py")
    # 起始代码包：先打 ok 的本地化补丁，再把注释译文写回去
    if "--no-py" not in sys.argv:
        run("patch_ok_local.py")
        run("py_apply.py")
