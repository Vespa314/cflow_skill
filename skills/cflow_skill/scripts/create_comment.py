#!/usr/bin/env python3
"""创建评论"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="创建评论")
    parser.add_argument("--memo_id", required=True, help="笔记 ID")
    parser.add_argument("--content", required=True, help="评论内容")
    parser.add_argument("--parent_comment_id", default=None, help="回复的目标评论 ID")
    args = parser.parse_args()

    token = load_token()
    data = {
        "memo_id": args.memo_id,
        "content": args.content.replace("\\n", "\n"),
    }
    if args.parent_comment_id is not None:
        data["parent_comment_id"] = args.parent_comment_id
    resp = requests.post(f"{base_url()}/create_comment", headers=auth_headers(token), json=data)
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
