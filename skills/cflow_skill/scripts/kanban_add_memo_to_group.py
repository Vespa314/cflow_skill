#!/usr/bin/env python3
"""添加备忘录到看板分组"""
import argparse
import json
import os
import sys

import requests

BASE_URL = os.environ.get("CFLOW_BASE_URL", "https://api.cflow.cc/v2/agent")


def main():
    parser = argparse.ArgumentParser(description="添加备忘录到看板分组")
    parser.add_argument("--kanban_id", required=True, help="看板ID")
    parser.add_argument("--group_id", required=True, help="分组ID")
    parser.add_argument("--memoIds", required=True, help="备忘录ID列表，逗号分隔，如 1,2,3")
    parser.add_argument("--kanbanSrc", required=False, help="添加到看板的原因,除非特别说明,否则不要填")
    parser.add_argument("--groupSrc", required=False, help="添加到分组的原因,除非特别说明,否则不要填")
    args = parser.parse_args()

    token = os.environ.get("CFLOW_TOKEN")
    if not token:
        print("错误: 请设置环境变量 CFLOW_TOKEN", file=sys.stderr)
        sys.exit(1)

    memo_ids = [int(x.strip()) for x in args.memoIds.split(",")]
    payload = {"kanban_id": args.kanban_id, "group_id": args.group_id, "memoIds": memo_ids}
    if args.kanbanSrc:
        payload["kanbanSrc"] = args.kanbanSrc
    if args.groupSrc:
        payload["groupSrc"] = args.groupSrc
    resp = requests.post(f"{BASE_URL}/kanban_add_memo_to_group", headers={"Authorization": f"Bearer {token}"}, json=payload)
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
