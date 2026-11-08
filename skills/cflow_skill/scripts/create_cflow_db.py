#!/usr/bin/env python3
"""为笔记创建 cflow 数据库附件（创建后用 exec_db.py 执行 SQL）"""
import argparse
import json
import sys

from _throttle import post
from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="为笔记创建 cflow 数据库附件")
    parser.add_argument("--memo_id", required=True, help="笔记 ID")
    parser.add_argument("--filename", required=True, help="数据库名称")
    args = parser.parse_args()

    token = load_token()
    resp = post(f"{base_url()}/create_cflow_db", headers=auth_headers(token),
        json={"memo_id": args.memo_id, "filename": args.filename}, timeout=120)
    try:
        result = resp.json()
    except ValueError:
        result = {"msg": resp.text}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if resp.status_code != 200:
        sys.exit(1)


if __name__ == "__main__":
    main()
