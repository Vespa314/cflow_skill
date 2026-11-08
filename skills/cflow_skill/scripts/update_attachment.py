#!/usr/bin/env python3
"""覆盖更新已有附件（仅普通附件）"""
import argparse
import json
import os
import sys

from _throttle import post

from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="覆盖更新已有附件")
    parser.add_argument("--attachment_id", required=True, help="附件 ID，即笔记 resourceList 里的 id")
    parser.add_argument("--file", required=True, help="本地文件路径")
    args = parser.parse_args()

    token = load_token()
    with open(args.file, "rb") as f:
        resp = post(f"{base_url()}/update_attachment", headers=auth_headers(token),
            files={"file": (os.path.basename(args.file), f)},
            data={"attachment_id": args.attachment_id}, timeout=120)
    try:
        result = resp.json()
    except ValueError:
        result = {"msg": resp.text}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if resp.status_code != 200:
        sys.exit(1)


if __name__ == "__main__":
    main()
