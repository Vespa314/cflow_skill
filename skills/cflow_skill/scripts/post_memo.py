#!/usr/bin/env python3
"""发表memo"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="发表memo")
    parser.add_argument("--content", required=True, help="memo内容")
    parser.add_argument("--title", default="", help="memo标题")
    parser.add_argument("--spaceId", default="", help="空间ID")
    args = parser.parse_args()

    token = load_token()
    content = args.content.replace("\\n", "\n")
    resp = requests.post(f"{base_url()}/post_memo", headers=auth_headers(token),
        json={"content": content, "title": args.title, "spaceId": args.spaceId})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
