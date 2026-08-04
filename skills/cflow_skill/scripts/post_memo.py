#!/usr/bin/env python3
"""发表memo"""
import argparse
import json
import os
import sys

import requests

BASE_URL = os.environ.get("CFLOW_BASE_URL", "https://api.cflow.cc/v2/agent")


def main():
    parser = argparse.ArgumentParser(description="发表memo")
    parser.add_argument("--content", required=True, help="memo内容")
    parser.add_argument("--title", default="", help="memo标题")
    parser.add_argument("--spaceId", default="", help="空间ID")
    args = parser.parse_args()

    token = os.environ.get("CFLOW_TOKEN")
    if not token:
        print("错误: 请设置环境变量 CFLOW_TOKEN", file=sys.stderr)
        sys.exit(1)

    content = args.content.replace("\\n", "\n")
    resp = requests.post(f"{BASE_URL}/post_memo", headers={"Authorization": f"Bearer {token}"},
        json={"content": content, "title": args.title, "spaceId": args.spaceId})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
