# cflow_skill

面向 [cflow](https://cflow.cc) 的 Agent Skill：笔记、标签、搜索、附件（上传 / 下载）、评论、时间胶囊与看板操作。

## 安装

```bash
npx skills add Vespa314/cflow_skill
```

## 依赖

- Python 3 + `requests`
- Access Token（用途为 Agent）：cflow「设置 → 我的账号」创建，用 `python3 scripts/setup_token.py --token "你的token"` 写入本地

## 用法

Agent 在 Skill 目录下执行 `python3 scripts/xxx.py`。完整工具表见 `skills/cflow_skill/SKILL.md`。

## 许可

MIT
