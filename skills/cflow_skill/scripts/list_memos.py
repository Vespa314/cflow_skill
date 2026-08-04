#!/usr/bin/env python3
"""分页列出笔记"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="分页列出笔记")
    parser.add_argument("--offset", type=int, default=0, help="偏移量，默认0")
    parser.add_argument("--limit", type=int, default=20, help="每页数量，默认20，最大100")
    parser.add_argument("--spaceId", default="", help="空间ID，不填则为默认空间")
    args = parser.parse_args()

    token = load_token()
    resp = requests.get(
        f"{base_url()}/list_memos",
        headers=auth_headers(token),
        params={"offset": args.offset, "limit": args.limit, "spaceId": args.spaceId},
    )
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
