#!/usr/bin/env python3
"""搜索笔记"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="搜索笔记")
    parser.add_argument("--query", required=True, help="搜索关键词，如 #微信读书")
    parser.add_argument("--space_id", default="", help="空间ID，默认为空")
    parser.add_argument("--page", type=int, default=0, help="页码，默认0")
    parser.add_argument("--pagesize", type=int, default=20, help="每页数量，最大100，默认20")
    args = parser.parse_args()

    token = load_token()
    resp = requests.post(f"{base_url()}/search_memos", headers=auth_headers(token),
        json={"query": args.query, "space_id": args.space_id, "page": args.page, "pagesize": args.pagesize})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
