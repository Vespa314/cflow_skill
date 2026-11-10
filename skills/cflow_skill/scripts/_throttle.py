#!/usr/bin/env python3
"""客户端滚动窗口频控：通用桶 5 次/s + 30 次/min（与服务端 Go NonFrontendTokenRateLimit 同口径）。
cflow DB 写入口（/exec_db、/create_cflow_db）服务端另有更严的 cflowDBRateLimit（1/s burst 1，
按用户按入口分桶），这里叠加一个共享 1/s DB 桶挡在前面，连续 exec/create 不会再吃 429。

所有工具脚本共用 scripts/.auth/ 下的时间戳日志（每行一个请求时间戳）做跨进程共享：
POSIX 用 flock，Windows 用 msvcrt.locking，锁覆盖「读 → 算 → 睡 → 记」全程，并发脚本自然串行。
超限自动 sleep 到窗口释放；服务端仍返回 429 时按 Retry-After 退避重试。
提示一律打 stderr（不污染 stdout 的 JSON 输出）。
"""
import sys
import time
from pathlib import Path

import requests

try:
    import fcntl
except ImportError:  # Windows 无 fcntl，降级 msvcrt 字节区域锁
    fcntl = None

RATE_DIR = Path(__file__).resolve().parent / ".auth"
RATE_LOG = RATE_DIR / "rate_log"
DB_LOG = RATE_DIR / "rate_log_db"

PER_SEC = 5      # 通用桶：每秒最多 5 次
PER_MIN = 30     # 通用桶：每分钟最多 30 次
DB_PER_SEC = 1   # DB 写桶：对齐服务端 cflowDBRateLimit（1/s burst 1）
WIN_SEC = 1.0
WIN_MIN = 60.0
KEEP_SEC = 120.0  # 日志只保留近 2 分钟，防文件无限增长

DB_WRITE_SUFFIXES = ("/exec_db", "/create_cflow_db")
RETRY_MAX = 3


def _lock(f):
    if fcntl is not None:
        fcntl.flock(f, fcntl.LOCK_EX)
        return
    import msvcrt
    while True:  # msvcrt.LK_LOCK 只重试约 10s，套一层循环逼近 flock 的阻塞语义
        try:
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
            return
        except OSError:
            time.sleep(0.5)


def _unlock(f):
    if fcntl is not None:
        fcntl.flock(f, fcntl.LOCK_UN)
        return
    import msvcrt
    f.seek(0)
    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)


def _wait_and_record(log_path, per_sec, per_min=None):
    log_path.parent.mkdir(exist_ok=True)
    with open(log_path, "a+", encoding="utf-8") as f:
        _lock(f)
        now = time.time()
        f.seek(0)
        stamps = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                stamps.append(float(line))
            except ValueError:  # 半截行等损坏数据：跳过而不是崩掉
                continue
        stamps = [t for t in stamps if now - t < KEEP_SEC]

        wait = 0.0
        sec_win = [t for t in stamps if now - t < WIN_SEC]
        if len(sec_win) >= per_sec:
            wait = max(wait, sec_win[0] + WIN_SEC - now)
        if per_min is not None:
            min_win = [t for t in stamps if now - t < WIN_MIN]
            if len(min_win) >= per_min:
                wait = max(wait, min_win[0] + WIN_MIN - now)

        if wait > 0:
            desc = f"{per_sec}次/s" + (f" · {per_min}次/min" if per_min else "")
            print(f"[频控] 触发 {desc} 上限，等待 {wait:.1f}s 后重试", file=sys.stderr)
            time.sleep(wait)
            now = time.time()

        stamps.append(now)
        f.seek(0)
        f.truncate()
        f.write("".join(f"{t:.3f}\n" for t in stamps if now - t < KEEP_SEC))
        f.flush()  # 解锁前必须落盘到 OS 缓冲，否则并发进程拿到锁读到旧/空日志，一起穿透频控
        _unlock(f)


def request(method, url, **kwargs):
    """统一请求入口：先过频控再发请求。仅用于 /v2/agent/* API 调用；
    对 COS 等第三方 URL 的直接下载不走本函数（不占服务端限频桶）。
    DB 写入口自动叠加 1/s 独立桶；429 时尊重 Retry-After 退避重试。"""
    is_db_write = url.rstrip("/").endswith(DB_WRITE_SUFFIXES)
    attempt = 0
    while True:
        _wait_and_record(RATE_LOG, PER_SEC, PER_MIN)
        if is_db_write:
            _wait_and_record(DB_LOG, DB_PER_SEC)
        resp = requests.request(method, url, **kwargs)
        if resp.status_code != 429 or attempt >= RETRY_MAX:
            return resp
        attempt += 1
        try:
            delay = float(resp.headers.get("Retry-After", "1"))
        except ValueError:
            delay = 1.0
        delay = min(max(delay, 0.5), 60.0)
        print(f"[频控] 服务端 429，等待 {delay:.1f}s 后重试（第 {attempt}/{RETRY_MAX} 次）",
              file=sys.stderr)
        time.sleep(delay)


def get(url, **kwargs):
    return request("GET", url, **kwargs)


def post(url, **kwargs):
    return request("POST", url, **kwargs)
