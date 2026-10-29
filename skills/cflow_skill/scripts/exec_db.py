#!/usr/bin/env python3
"""对 cflow 数据库附件执行 SQL"""
import argparse
import json
import sys

import requests
from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="对 cflow 数据库附件执行 SQL")
    parser.add_argument("--attachment_id", required=True, help="cflow 数据库附件 ID（笔记 resourceList 里的 id）")
    parser.add_argument("--sql", required=True, help="SQL 文本，多条语句用分号分隔（整批一个事务）")
    args = parser.parse_args()

    token = load_token()
    resp = requests.post(f"{base_url()}/exec_db", headers=auth_headers(token),
        json={"attachment_id": args.attachment_id, "sql": args.sql}, timeout=120)
    try:
        result = resp.json()
    except ValueError:
        result = {"msg": resp.text}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if resp.status_code != 200:
        sys.exit(1)


if __name__ == "__main__":
    main()
