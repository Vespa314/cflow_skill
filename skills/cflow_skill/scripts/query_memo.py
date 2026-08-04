#!/usr/bin/env python3
"""查询一个memo"""
import argparse
import json
import os
import sys

import requests

BASE_URL = os.environ.get("CFLOW_BASE_URL", "https://api.cflow.cc/v2/agent")


def main():
    parser = argparse.ArgumentParser(description="查询一个memo")
    parser.add_argument("--memo_id", required=True, help="memo ID")
    args = parser.parse_args()

    token = os.environ.get("CFLOW_TOKEN")
    if not token:
        print("错误: 请设置环境变量 CFLOW_TOKEN", file=sys.stderr)
        sys.exit(1)

    resp = requests.get(f"{BASE_URL}/query_memo", headers={"Authorization": f"Bearer {token}"},
        params={"memo_id": args.memo_id})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
