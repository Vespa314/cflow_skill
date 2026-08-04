#!/usr/bin/env python3
"""更新看板中的备忘录"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="更新看板中的备忘录")
    parser.add_argument("--kanban_id", required=True, help="看板ID")
    parser.add_argument("--memo_id", required=True, help="备忘录ID")
    parser.add_argument("--groupId", default=None, help="移动到目标分组ID")
    parser.add_argument("--groupSrc", default=None, help="分组来源，如 manual")
    parser.add_argument("--isPin", default=None, help="是否置顶 true/false")
    parser.add_argument("--isMark", default=None, help="是否高亮 true/false")
    parser.add_argument("--deadline", default=None, help="截止时间戳(<=0清除)")
    parser.add_argument("--tags", default=None, help="标签(逗号分隔)")
    parser.add_argument("--isWatching", default=None, help="是否关注 true/false")
    args = parser.parse_args()

    token = load_token()
    data = {"kanban_id": args.kanban_id, "memo_id": args.memo_id}
    if args.groupId is not None:
        data["groupId"] = int(args.groupId)
    if args.groupSrc is not None:
        data["groupSrc"] = args.groupSrc
    if args.isPin is not None:
        data["isPin"] = args.isPin.lower() == "true"
    if args.isMark is not None:
        data["isMark"] = args.isMark.lower() == "true"
    if args.deadline is not None:
        data["deadline"] = int(args.deadline)
    if args.tags is not None:
        data["tags"] = args.tags
    if args.isWatching is not None:
        data["isWatching"] = args.isWatching.lower() == "true"

    resp = requests.post(f"{base_url()}/kanban_update_memo", headers=auth_headers(token), json=data)
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
