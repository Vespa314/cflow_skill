#!/usr/bin/env python3
"""创建看板分组"""
import argparse
import json
import os
import sys

import requests

BASE_URL = os.environ.get("CFLOW_BASE_URL", "https://api.cflow.cc/v2/agent")


def main():
    parser = argparse.ArgumentParser(description="创建看板分组")
    parser.add_argument("--kanban_id", required=True, help="看板ID")
    parser.add_argument("--groupName", required=True, help="分组名称")
    args = parser.parse_args()

    token = os.environ.get("CFLOW_TOKEN")
    if not token:
        print("错误: 请设置环境变量 CFLOW_TOKEN", file=sys.stderr)
        sys.exit(1)

    resp = requests.post(f"{BASE_URL}/kanban_create_group", headers={"Authorization": f"Bearer {token}"}, json={"kanban_id": args.kanban_id, "groupName": args.groupName})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
