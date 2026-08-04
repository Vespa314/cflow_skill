#!/usr/bin/env python3
"""查询某个话题相关的笔记"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="查询某个话题相关的笔记")
    parser.add_argument("--query", required=True, help="查询内容")
    parser.add_argument("--limit", type=int, default=10, help="返回数量上限，最大30")
    parser.add_argument("--space_id", default="", help="空间ID，默认为空")
    args = parser.parse_args()

    token = load_token()
    resp = requests.post(f"{base_url()}/query_topic_memos", headers=auth_headers(token),
        json={"query": args.query, "limit": args.limit, "space_id": args.space_id})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
