"""备份将被中文化修改的文件到 _backup_en/（保持原目录结构）。

备份对象：cs61a_offline/ 下所有 .html 与 .zip 文件（导航翻译会改全部 html，
内容翻译改核心 lab/hw/disc/proj，代码注释翻译改 zip）。用于人工校对与回滚。
"""
import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "cs61a_offline")
DST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "_backup_en")

EXTS = (".html", ".zip")

copied = 0
skipped = 0

for root, dirs, files in os.walk(SRC):
    for name in files:
        if not name.endswith(EXTS):
            continue
        src = os.path.join(root, name)
        rel = os.path.relpath(src, SRC)
        dst = os.path.join(DST, rel)
        if os.path.exists(dst):
            skipped += 1
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1

print(f"备份完成：复制 {copied} 个文件，跳过已存在 {skipped} 个。")
print(f"备份目录：{DST}")
