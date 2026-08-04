#!/usr/bin/env python3
"""获取看板 schema"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="获取看板 schema")
    parser.add_argument("--kanban_id", required=True, help="看板ID")
    args = parser.parse_args()

    token = load_token()
    resp = requests.get(f"{base_url()}/kanban_schema", headers=auth_headers(token), params={"kanban_id": args.kanban_id})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
