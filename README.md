# cflow_skill

用 Agent 操作 [cflow](https://cflow.cc) 笔记：创建 / 修改 / 查询 / 搜索 / 标签 / 附件 / 看板。

## Install

```bash
npx skills add Vespa314/cflow_skill
```

只装这一项：

```bash
npx skills add Vespa314/cflow_skill --skill cflow_skill
```

## Requirements

- Python 3
- `pip install requests`（脚本依赖）
- 环境变量 `CFLOW_TOKEN`：在 cflow「设置 → 我的账号」创建用途为 Agent 的 Access token

可选：

```bash
export CFLOW_BASE_URL=https://api.cflow.cc/v2/agent   # 默认即此
```

## What It Does

安装后，Agent 可通过本 Skill 的 `scripts/` 调用 cflow Agent API，覆盖：

- 空间与标签：`list_space`、`fetch_tags`
- 笔记 CRUD / 附件：`post_memo`、`update_memo`、`query_memo`、`list_memos`、`add_attachment`
- 搜索：`search_memos`（语法搜索）、`query_topic_memos`（语义搜索）
- 看板：列表、创建、详情、分组、加减笔记等

## How It Works

1. 在 Skill 根目录执行 `python3 scripts/<tool>.py ...`
2. 脚本读取 `CFLOW_TOKEN`，请求 cflow Agent API
3. 批量调用请至少间隔 3 秒

详细参数与选用策略见 `skills/cflow_skill/SKILL.md`。

## Example Requests

- 「列出我有哪些空间」
- 「用标签 #工作 搜索笔记」
- 「写一条笔记到 work 空间，标题为周报」
- 「把笔记 130 加到看板 1 的分组 2」

## Safety / Limitations

- 需要有效的 `CFLOW_TOKEN`；不要把 token 写进仓库或对话记录
- 私密笔记可能无法查看或更新
- 参数名必须与 Skill 文档表格完全一致（如 `spaceId` ≠ `space_id`）

## License

MIT
