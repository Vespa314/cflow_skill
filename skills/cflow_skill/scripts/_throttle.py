#!/usr/bin/env python3
"""客户端滚动窗口频控：5 次/s + 30 次/min（与服务端 Go NonFrontendTokenRateLimit 同口径）。

所有工具脚本共用 scripts/.auth/rate_log（每行一个请求时间戳）做跨进程共享，
flock 排它锁覆盖「读 → 算 → 睡 → 记」全程，并发脚本自然串行。
超限时自动计算并 sleep 到窗口释放，提示打到 stderr（不污染 stdout 的 JSON 输出）。
"""
import fcntl
import sys
import time
from pathlib import Path

import requests

RATE_LOG = Path(__file__).resolve().parent / ".auth" / "rate_log"

PER_SEC = 5      # 每秒最多 5 次
PER_MIN = 30     # 每分钟最多 30 次
WIN_SEC = 1.0
WIN_MIN = 60.0
KEEP_SEC = 120.0  # 日志只保留近 2 分钟，防文件无限增长


def _wait_and_record():
    RATE_LOG.parent.mkdir(exist_ok=True)
    with open(RATE_LOG, "a+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        now = time.time()
        f.seek(0)
        stamps = [float(line) for line in f if line.strip()]
        stamps = [t for t in stamps if now - t < KEEP_SEC]

        wait = 0.0
        sec_win = [t for t in stamps if now - t < WIN_SEC]
        if len(sec_win) >= PER_SEC:
            wait = max(wait, sec_win[0] + WIN_SEC - now)
        min_win = [t for t in stamps if now - t < WIN_MIN]
        if len(min_win) >= PER_MIN:
            wait = max(wait, min_win[0] + WIN_MIN - now)

        if wait > 0:
            print(f"[频控] 触发 {PER_SEC}次/s · {PER_MIN}次/min 上限，等待 {wait:.1f}s 后重试",
                  file=sys.stderr)
            time.sleep(wait)
            now = time.time()

        stamps.append(now)
        f.seek(0)
        f.truncate()
        f.write("".join(f"{t:.3f}\n" for t in stamps if now - t < KEEP_SEC))
        fcntl.flock(f, fcntl.LOCK_UN)


def request(method, url, **kwargs):
    """统一请求入口：先过频控再发请求。仅用于 /v2/agent/* API 调用；
    对 COS 等第三方 URL 的直接下载不走本函数（不占服务端限频桶）。"""
    _wait_and_record()
    return requests.request(method, url, **kwargs)


def get(url, **kwargs):
    return request("GET", url, **kwargs)


def post(url, **kwargs):
    return request("POST", url, **kwargs)
