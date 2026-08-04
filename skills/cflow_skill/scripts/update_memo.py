#!/usr/bin/env python3
"""更新memo"""
import argparse
import json
import sys

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="更新memo")
    parser.add_argument("--memo_id", required=True, help="memo ID")
    parser.add_argument("--content", default=None, help="新内容")
    parser.add_argument("--title", default=None, help="新标题")
    parser.add_argument("--pin", default=None, help="是否置顶 true/false")
    args = parser.parse_args()

    token = load_token()
    data = {"memo_id": args.memo_id}
    if args.content is not None:
        data["content"] = args.content.replace("\\n", "\n")
    if args.title is not None:
        data["title"] = args.title
    if args.pin is not None:
        data["pin"] = args.pin.lower() == "true"
    if "content" not in data and "title" not in data and "pin" not in data:
        print("错误: --content、--title 和 --pin 不能同时为空", file=sys.stderr)
        sys.exit(1)

    resp = requests.post(f"{base_url()}/update_memo", headers=auth_headers(token), json=data)
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
