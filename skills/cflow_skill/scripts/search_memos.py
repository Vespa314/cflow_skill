#!/usr/bin/env python3
"""搜索笔记"""
import argparse
import json
import os
import sys

import requests

BASE_URL = os.environ.get("CFLOW_BASE_URL", "https://api.cflow.cc/v2/agent")


def main():
    parser = argparse.ArgumentParser(description="搜索笔记")
    parser.add_argument("--query", required=True, help="搜索关键词，如 #微信读书")
    parser.add_argument("--space_id", default="", help="空间ID，默认为空")
    parser.add_argument("--page", type=int, default=0, help="页码，默认0")
    parser.add_argument("--pagesize", type=int, default=20, help="每页数量，最大100，默认20")
    args = parser.parse_args()

    token = os.environ.get("CFLOW_TOKEN")
    if not token:
        print("错误: 请设置环境变量 CFLOW_TOKEN", file=sys.stderr)
        sys.exit(1)

    resp = requests.post(f"{BASE_URL}/search_memos", headers={"Authorization": f"Bearer {token}"},
        json={"query": args.query, "space_id": args.space_id, "page": args.page, "pagesize": args.pagesize})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
