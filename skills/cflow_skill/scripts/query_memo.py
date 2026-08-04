#!/usr/bin/env python3
"""查询一个memo"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="查询一个memo")
    parser.add_argument("--memo_id", required=True, help="memo ID")
    args = parser.parse_args()

    token = load_token()
    resp = requests.get(f"{base_url()}/query_memo", headers=auth_headers(token),
        params={"memo_id": args.memo_id})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
