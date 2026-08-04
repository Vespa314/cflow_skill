#!/usr/bin/env python3
"""拉取tag"""
import argparse
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="拉取tag")
    parser.add_argument("--space_id", default="", help="空间ID，默认为空")
    args = parser.parse_args()

    token = load_token()
    resp = requests.post(f"{base_url()}/fetch_tags", headers=auth_headers(token),
        json={"space_id": args.space_id})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
