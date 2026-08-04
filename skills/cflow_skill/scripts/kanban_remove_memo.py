#!/usr/bin/env python3
"""从看板移除备忘录"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="从看板移除备忘录")
    parser.add_argument("--kanban_id", required=True, help="看板ID")
    parser.add_argument("--memo_id", required=True, help="备忘录ID")
    args = parser.parse_args()

    token = load_token()
    resp = requests.get(f"{base_url()}/kanban_remove_memo", headers=auth_headers(token), params={"kanban_id": args.kanban_id, "memo_id": args.memo_id})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
