#!/usr/bin/env python3
"""为memo增加附件"""
import argparse
import json
import os
import sys

import requests

BASE_URL = os.environ.get("CFLOW_BASE_URL", "https://api.cflow.cc/v2/agent")


def main():
    parser = argparse.ArgumentParser(description="为memo增加附件")
    parser.add_argument("--memo_id", required=True, help="memo ID")
    parser.add_argument("--file", required=True, help="本地文件路径")
    parser.add_argument("--content_type", required=True, help="文件MIME类型，如 text/plain, image/png, application/pdf")
    args = parser.parse_args()

    token = os.environ.get("CFLOW_TOKEN")
    if not token:
        print("错误: 请设置环境变量 CFLOW_TOKEN", file=sys.stderr)
        sys.exit(1)

    with open(args.file, "rb") as f:
        resp = requests.post(f"{BASE_URL}/add_attachment", headers={"Authorization": f"Bearer {token}"},
            files={"file": (os.path.basename(args.file), f, args.content_type)},
            data={"memo_id": args.memo_id})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
