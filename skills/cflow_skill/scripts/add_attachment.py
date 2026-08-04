#!/usr/bin/env python3
"""为memo增加附件"""
import argparse
import json
import os

import requests

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="为memo增加附件")
    parser.add_argument("--memo_id", required=True, help="memo ID")
    parser.add_argument("--file", required=True, help="本地文件路径")
    parser.add_argument("--content_type", required=True, help="文件MIME类型，如 text/plain, image/png, application/pdf")
    args = parser.parse_args()

    token = load_token()
    with open(args.file, "rb") as f:
        resp = requests.post(f"{base_url()}/add_attachment", headers=auth_headers(token),
            files={"file": (os.path.basename(args.file), f, args.content_type)},
            data={"memo_id": args.memo_id})
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
