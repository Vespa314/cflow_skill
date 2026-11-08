#!/usr/bin/env python3
"""列出用户可用的空间"""
import json

from _throttle import get

from _auth import auth_headers, base_url, load_token


def main():
    token = load_token()
    resp = get(f"{base_url()}/list_space", headers=auth_headers(token))
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
