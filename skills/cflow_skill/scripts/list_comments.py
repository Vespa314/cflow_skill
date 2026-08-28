#!/usr/bin/env python3
"""拉取笔记的评论"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="拉取笔记的评论")
    parser.add_argument("--memo_id", required=True, help="笔记 ID")
    args = parser.parse_args()

    token = load_token()
    resp = requests.get(f"{base_url()}/list_comments", headers=auth_headers(token),
        params={"memo_id": args.memo_id})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
