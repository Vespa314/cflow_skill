#!/usr/bin/env python3
"""查询某个话题相关的笔记"""
import argparse
import json
import os
import sys

import requests

BASE_URL = os.environ.get("CFLOW_BASE_URL", "https://api.cflow.cc/v2/agent")


def main():
    parser = argparse.ArgumentParser(description="查询某个话题相关的笔记")
    parser.add_argument("--query", required=True, help="查询内容")
    parser.add_argument("--limit", type=int, default=10, help="返回数量上限，最大30")
    parser.add_argument("--space_id", default="", help="空间ID，默认为空")
    args = parser.parse_args()

    token = os.environ.get("CFLOW_TOKEN")
    if not token:
        print("错误: 请设置环境变量 CFLOW_TOKEN", file=sys.stderr)
        sys.exit(1)

    resp = requests.post(f"{BASE_URL}/query_topic_memos", headers={"Authorization": f"Bearer {token}"},
        json={"query": args.query, "limit": args.limit, "space_id": args.space_id})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
