#!/usr/bin/env python3
"""更新memo"""
import argparse
import json
import os
import sys

import requests

BASE_URL = os.environ.get("CFLOW_BASE_URL", "https://api.cflow.cc/v2/agent")


def main():
    parser = argparse.ArgumentParser(description="更新memo")
    parser.add_argument("--memo_id", required=True, help="memo ID")
    parser.add_argument("--content", default=None, help="新内容")
    parser.add_argument("--title", default=None, help="新标题")
    parser.add_argument("--pin", default=None, help="是否置顶 true/false")
    args = parser.parse_args()

    token = os.environ.get("CFLOW_TOKEN")
    if not token:
        print("错误: 请设置环境变量 CFLOW_TOKEN", file=sys.stderr)
        sys.exit(1)

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

    resp = requests.post(f"{BASE_URL}/update_memo", headers={"Authorization": f"Bearer {token}"}, json=data)
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
