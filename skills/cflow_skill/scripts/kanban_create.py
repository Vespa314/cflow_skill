#!/usr/bin/env python3
"""创建看板"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="创建看板")
    parser.add_argument("--name", required=True, help="看板名称")
    args = parser.parse_args()

    token = load_token()
    resp = requests.post(f"{base_url()}/kanban_create", headers=auth_headers(token), json={"name": args.name})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
