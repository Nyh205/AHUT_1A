"""把 ok 改为默认「纯本地模式」：禁用一切网络活动，只保留本地测试。

CS61A 的 ok 是一个 zipapp（打包的 Python 应用），内含 __main__.py、client/
源码与内嵌的 requests 等库。它在运行时会向 Berkeley 服务器备份代码、上报
解锁分组等。本脚本对每个作业 zip 里的 ok 做两处最小改动：

  1) client/cli/ok.py —— --local 参数默认开启。这是 okpy 官方开关，语义正是
     "disable any network activity"，会让 backup / collaborate / autostyle /
     hinting / 版本更新检查全部跳过。
  2) client/utils/guidance.py —— UnlockProtocol.set_tg() 里，在读取邮箱之前
     就短路返回，避免它绕过 --local 直接向 tg-server 发起请求。

改动只涉及这两个位置，不动评分逻辑；本地测试（doctest / ok_test）不受影响。
"""
import glob
import io
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "cs61a_offline")

# 锚点 1：--local 参数定义（client/cli/ok.py）
A1 = "server.add_argument('--local', action='store_true',"
A1_NEW = "server.add_argument('--local', action='store_true', default=True,"

# 锚点 2：set_tg 里读取邮箱的逻辑（client/utils/guidance.py）
A2 = '''            cur_email = self.assignment.get_student_email()
            log.info("Current email is %s", cur_email)
            if not cur_email:
                self.tg_id = -1
                return EMPTY_MISUCOUNT_TGID_PRNTEDMSG'''
A2_NEW = '''            if self.args.local:
                self.tg_id = -1
                return EMPTY_MISUCOUNT_TGID_PRNTEDMSG
            cur_email = self.assignment.get_student_email()
            log.info("Current email is %s", cur_email)
            if not cur_email:
                self.tg_id = -1
                return EMPTY_MISUCOUNT_TGID_PRNTEDMSG'''

TARGETS = {
    "client/cli/ok.py": (A1, A1_NEW),
    "client/utils/guidance.py": (A2, A2_NEW),
}


def rebuild(entries):
    """按原始条目属性重新打包，返回字节。"""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for info, data in entries:
            zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            zi.compress_type = info.compress_type
            zi.external_attr = info.external_attr
            zi.internal_attr = info.internal_attr
            zi.create_system = info.create_system
            zout.writestr(zi, data)
    return buf.getvalue()


def patch_ok_bytes(ok_data):
    """patch zipapp 形式的 ok。

    返回 (状态, 新字节)，状态取值：
      patched    —— 已成功改写
      already    —— 之前已改写（幂等重跑）
      not_zipapp —— 不是 zipapp（如 exam 里的 shell 包装脚本），保持原样
      no_anchor  —— 是 zipapp 但找不到锚点，保持原样
    """
    try:
        with zipfile.ZipFile(io.BytesIO(ok_data)) as zin:
            entries = [(i, zin.read(i.filename)) for i in zin.infolist()]
    except zipfile.BadZipFile:
        return "not_zipapp", None

    texts = {info.filename: data.decode("utf-8")
             for info, data in entries if info.filename in TARGETS}
    if len(texts) != len(TARGETS):
        return "no_anchor", None
    if any(new in texts[name] for name, (_, new) in TARGETS.items()):
        return "already", None
    if any(old not in texts[name] for name, (old, _) in TARGETS.items()):
        return "no_anchor", None

    new_entries = []
    for info, data in entries:
        pair = TARGETS.get(info.filename)
        if pair:
            old, new = pair
            data = data.decode("utf-8").replace(old, new, 1).encode("utf-8")
        new_entries.append((info, data))
    return "patched", rebuild(new_entries)


def is_ok(name):
    return name == "ok" or name.endswith("/ok")


def patch_zip(path):
    """返回 (本次改写的 ok 数, 状态说明)。"""
    with zipfile.ZipFile(path) as zin:
        entries = [(i, zin.read(i.filename)) for i in zin.infolist()]

    changed = 0
    statuses = []
    new_entries = []
    for info, data in entries:
        if is_ok(info.filename):
            status, patched = patch_ok_bytes(data)
            statuses.append(status)
            if status == "patched":
                data = patched
                changed += 1
        new_entries.append((info, data))

    if changed == 0:
        return 0, ",".join(sorted(set(statuses))) or "未找到 ok"

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        for info, data in new_entries:
            zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            zi.compress_type = info.compress_type
            zi.external_attr = info.external_attr
            zi.internal_attr = info.internal_attr
            zi.create_system = info.create_system
            zout.writestr(zi, data)
    return changed, ",".join(sorted(set(statuses)))


def main():
    patched_zips = 0
    tally = {}
    for zp in sorted(glob.glob(os.path.join(SITE, "**", "*.zip"), recursive=True)):
        try:
            n, status = patch_zip(zp)
        except Exception as exc:
            tally.setdefault("error", []).append(
                (zp, f"{type(exc).__name__}: {exc}"))
            continue
        if n:
            patched_zips += 1
        tally.setdefault(status, []).append(zp)

    print(f"ok 本地化补丁完成：本次改写 {patched_zips} 个 zip。")
    for status, paths in sorted(tally.items()):
        print(f"  [{status}] {len(paths)} 个")
        if status == "error":
            for zp, why in paths[:10]:
                print(f"      {os.path.relpath(zp, ROOT)}  —— {why}")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
