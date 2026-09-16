"""体检：确认 .py 的翻译只动了「给人读的字」，代码一个字节没变。

对每个起始代码包里的每个被翻过的 .py，把它和 _backup_en 里的英文原版比：

  ast       去掉 docstring 之后的语法树必须完全一致 —— 这是「代码逻辑不变」
            的硬保证：任何一行代码、任何字符串字面量、任何缩进被改动，
            ast.dump 都会变。
  token     除注释和 docstring 之外的所有 token 逐字一致；行号也一致
            （pytext 按原行数摊开译文，正是为了不动后面的行号）。
  doctest   <pre> 之外，docstring 里 >>> 开头及其后续期望输出行逐字一致。
  compile   py_compile 通过。

用法：
    python tools/py_verify.py
"""
import ast
import glob
import io
import os
import py_compile
import sys
import tempfile
import tokenize
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytext

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "cs61a_offline")
BACKUP = os.path.join(ROOT, "_backup_en")


def strip_docstrings(tree):
    """把所有 docstring 常量抹成空串 —— 只留代码结构。"""
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(body, list) and body:
            first = body[0]
            if isinstance(first, ast.Expr) \
                    and isinstance(first.value, ast.Constant) \
                    and isinstance(first.value.value, str):
                first.value.value = ""
    return ast.dump(tree)


def doc_positions(src):
    """docstring 里 STRING token 的位置集合 —— 这些 token 允许变。"""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return set()
    out = set()
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(body, list) and body:
            first = body[0]
            if isinstance(first, ast.Expr) \
                    and isinstance(first.value, ast.Constant) \
                    and isinstance(first.value.value, str):
                out.add((first.value.lineno, first.value.col_offset))
    return out


def code_tokens(src):
    """除注释、除 docstring 字符串之外的全部 token 及位置。"""
    docs = doc_positions(src)
    out = []
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError) as e:
        return None, str(e)
    for t in toks:
        if t.type in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE,
                      tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING,
                      tokenize.ENDMARKER):
            continue
        if t.type == tokenize.STRING and (t.start[0], t.start[1]) in docs:
            continue                      # docstring 本身：译文就写在这里
        out.append((t.type, t.string, t.start, t.end))
    return out, None


def main():
    bad = 0
    nfile = nseg = 0
    tmp = tempfile.mkdtemp()
    for zpath, name in pytext.targets(dedup=False):
        rel = os.path.relpath(zpath, SITE).replace(os.sep, "/")
        bz = os.path.join(BACKUP, rel)
        if not os.path.exists(bz):
            print("[缺备份] %s" % rel)
            bad += 1
            continue
        with zipfile.ZipFile(zpath) as z, zipfile.ZipFile(bz) as bz_f:
            try:
                new = z.read(name).decode("utf-8")
                old = bz_f.read(name).decode("utf-8")
            except (KeyError, UnicodeDecodeError):
                continue
        if new == old:
            continue                       # 没翻到，不用比
        nfile += 1
        problems = []
        try:
            if strip_docstrings(ast.parse(old)) != strip_docstrings(ast.parse(new)):
                problems.append("ast 变了")
        except SyntaxError as e:
            problems.append("语法错误：%s" % e)
        to, eo = code_tokens(old)
        tn, en_ = code_tokens(new)
        if eo or en_:
            problems.append("tokenize 失败：%s%s" % (eo or "", en_ or ""))
        elif to != tn:
            problems.append("token 不同（%d → %d）" % (len(to), len(tn)))
            for a, b in zip(to, tn):
                if a != b:
                    problems.append("    %r → %r" % (a, b))
                    break
        p = os.path.join(tmp, "x.py")
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(new)
        try:
            py_compile.compile(p, doraise=True,
                               cfile=os.path.join(tmp, "x.pyc"))
        except py_compile.PyCompileError as e:
            problems.append("编译失败：%s" % str(e).split("\n")[0])
        if problems:
            bad += 1
            print("[不一致] %s / %s" % (rel, name))
            for s in problems[:4]:
                print("    " + s)
    if not bad:
        print("起始代码体检通过：%d 个文件被翻译，代码与 doctest 逐字一致。"
              % nfile)
    else:
        print("有 %d 个文件有问题。" % bad)


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
