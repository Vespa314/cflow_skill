#!/usr/bin/env python3
"""配置 cflow token。

支持几种用法：

    python3 scripts/setup_token.py                      # 交互式，提示输入
    python3 scripts/setup_token.py --token "xxxx"       # 命令行直接传入
    python3 scripts/setup_token.py --show               # 查看是否已配置（只显示前后 4 位）
    python3 scripts/setup_token.py --clear              # 删除已保存的 token

token 写入 scripts/.auth/token（权限 0600）。该目录被 .gitignore 忽略，不会提交。
"""
import argparse
import os
import sys

from _auth import TOKEN_FILE


def save_token(token: str):
    token = token.strip()
    if not token:
        print("错误: token 不能为空", file=sys.stderr)
        sys.exit(1)

    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(token + "\n", encoding="utf-8")
    try:
        os.chmod(TOKEN_FILE, 0o600)
    except OSError:
        pass

    print(f"已保存到 {TOKEN_FILE}")
    print("所有脚本会自动读取。如需切换用户，重新运行本命令覆盖即可。")


def show_token():
    if TOKEN_FILE.exists():
        s = TOKEN_FILE.read_text(encoding="utf-8").strip()
        if s:
            masked = f"{s[:4]}...{s[-4:]}" if len(s) > 8 else "***"
            print(f"已配置 token：{masked}")
            print(f"位置：{TOKEN_FILE}")
        else:
            print(f"文件存在但为空：{TOKEN_FILE}")
    else:
        print(f"未配置：{TOKEN_FILE}")
        print("运行 `python3 scripts/setup_token.py` 进行配置。")


def clear_token():
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        print(f"已删除：{TOKEN_FILE}")
    else:
        print(f"本来就没有：{TOKEN_FILE}")


def main():
    parser = argparse.ArgumentParser(description="配置 cflow token")
    parser.add_argument("--token", help="直接传入 token（不交互）")
    parser.add_argument("--show", action="store_true", help="查看当前配置（脱敏）")
    parser.add_argument("--clear", action="store_true", help="删除已保存的 token")
    args = parser.parse_args()

    if args.show:
        show_token()
        return
    if args.clear:
        clear_token()
        return

    token = args.token
    if not token:
        try:
            token = input("请粘贴你的 cflow Access Token（用途选 Agent）：").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n已取消", file=sys.stderr)
            sys.exit(1)

    save_token(token)


if __name__ == "__main__":
    main()
