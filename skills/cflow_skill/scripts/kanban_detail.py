#!/usr/bin/env python3
"""获取看板详情"""
import argparse
import json
import os
import sys

import requests

BASE_URL = os.environ.get("CFLOW_BASE_URL", "https://api.cflow.cc/v2/agent")


def main():
    parser = argparse.ArgumentParser(description="获取看板详情")
    parser.add_argument("--kanban_id", required=True, help="看板ID")
    args = parser.parse_args()

    token = os.environ.get("CFLOW_TOKEN")
    if not token:
        print("错误: 请设置环境变量 CFLOW_TOKEN", file=sys.stderr)
        sys.exit(1)

    resp = requests.get(f"{BASE_URL}/kanban_detail", headers={"Authorization": f"Bearer {token}"}, params={"kanban_id": args.kanban_id})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
