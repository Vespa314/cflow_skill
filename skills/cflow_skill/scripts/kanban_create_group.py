#!/usr/bin/env python3
"""创建看板分组"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="创建看板分组")
    parser.add_argument("--kanban_id", required=True, help="看板ID")
    parser.add_argument("--groupName", required=True, help="分组名称")
    args = parser.parse_args()

    token = load_token()
    resp = requests.post(f"{base_url()}/kanban_create_group", headers=auth_headers(token), json={"kanban_id": args.kanban_id, "groupName": args.groupName})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
