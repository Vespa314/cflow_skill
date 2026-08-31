#!/usr/bin/env python3
"""下载笔记附件到本地"""
import argparse
import json
import os
import sys

import requests
from _auth import auth_headers, base_url, load_token


def main():
    parser = argparse.ArgumentParser(description="下载笔记附件到本地")
    parser.add_argument("--attachment_id", required=True, help="附件 ID（笔记 resourceList 里的 id）")
    parser.add_argument("--dir", default=".", help="保存目录，默认当前目录，不存在会自动创建")
    parser.add_argument("--filename", help="保存文件名，默认用附件原文件名")
    args = parser.parse_args()

    token = load_token()
    resp = requests.post(f"{base_url()}/get_attachment", headers=auth_headers(token),
        json={"attachment_id": args.attachment_id})
    if resp.status_code != 200:
        try:
            result = resp.json()
        except ValueError:
            result = {"msg": resp.text}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)
    info = resp.json()

    filename = args.filename or info.get("filename") or f"attachment_{args.attachment_id}"
    os.makedirs(args.dir, exist_ok=True)
    dst = os.path.join(args.dir, filename)

    try:
        with requests.get(info["url"], stream=True, timeout=300) as r:
            r.raise_for_status()
            tmp = f"{dst}.tmp"
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=64 * 1024):
                    if chunk:
                        f.write(chunk)
            os.replace(tmp, dst)
    except requests.RequestException as exc:
        print(json.dumps({"msg": f"下载附件失败: {exc}"}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps({
        "path": os.path.abspath(dst),
        "filename": filename,
        "size": os.path.getsize(dst),
        "type": info.get("type"),
        "memoId": info.get("memoId"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
