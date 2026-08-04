#!/usr/bin/env python3
"""统一鉴权模块。

所有工具脚本通过 `load_token()` 拿 CFLOW_TOKEN，
统一从本地文件 `scripts/.auth/token` 读取（一行裸 token）。

`CFLOW_BASE_URL` 走环境变量，缺省 `https://api.cflow.cc/v2/agent`。
"""
import os
import sys
from pathlib import Path

TOKEN_FILE = Path(__file__).resolve().parent / ".auth" / "token"

ENV_BASE_URL_NAME = "CFLOW_BASE_URL"
DEFAULT_BASE_URL = "https://api.cflow.cc/v2/agent"


def load_token():
    """返回 token。找不到就在 stderr 打印指引并 sys.exit(1)。"""
    try:
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        token = ""
    except OSError:
        token = ""

    if token:
        return token

    print(
        f"错误: 未配置 CFLOW_TOKEN。\n"
        f"  运行 `python3 scripts/setup_token.py` 把 token 写入\n"
        f"  {TOKEN_FILE}\n"
        f"  token 在 cflow 「设置 - 我的账号」创建，用途选 Agent。",
        file=sys.stderr,
    )
    sys.exit(1)


def base_url():
    return os.environ.get(ENV_BASE_URL_NAME, DEFAULT_BASE_URL)


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}
