#!/usr/bin/env python3
"""拉取tag"""
import argparse
import json
import os
import sys

import requests

BASE_URL = os.environ.get("CFLOW_BASE_URL", "https://api.cflow.cc/v2/agent")


def main():
    parser = argparse.ArgumentParser(description="拉取tag")
    parser.add_argument("--space_id", default="", help="空间ID，默认为空")
    args = parser.parse_args()

    token = os.environ.get("CFLOW_TOKEN")
    if not token:
        print("错误: 请设置环境变量 CFLOW_TOKEN", file=sys.stderr)
        sys.exit(1)

    resp = requests.post(f"{BASE_URL}/fetch_tags", headers={"Authorization": f"Bearer {token}"},
        json={"space_id": args.space_id})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
