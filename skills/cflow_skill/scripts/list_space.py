#!/usr/bin/env python3
"""列出用户可用的空间"""
import json

import requests

from _auth import auth_headers, base_url, load_token


def main():
    token = load_token()
    resp = requests.get(f"{base_url()}/list_space", headers=auth_headers(token))
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
