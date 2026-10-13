#!/usr/bin/env python3
"""查看单个时间胶囊"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="查看单个时间胶囊")
    parser.add_argument("--time_capsule_id", required=True, help="时间胶囊 ID")
    args = parser.parse_args()

    token = load_token()
    resp = requests.get(
        f"{base_url()}/query_time_capsule",
        headers=auth_headers(token),
        params={"time_capsule_id": args.time_capsule_id},
    )
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
