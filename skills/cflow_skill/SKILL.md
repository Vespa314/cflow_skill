---
name: cflow_skill
description: 当用户在 cflow/笔记系统中执行笔记操作时（创建、修改、查询、上传附件、查标签、搜索、看板操作），可以使用该技能。
---

## 配置 Token（首次使用必读）

所有工具脚本都通过 `scripts/_auth.py` 统一从本地文件 `scripts/.auth/token` 读取 `CFLOW_TOKEN`。

去 cflow 「设置 - 我的账号」创建一个用途为 **Agent** 的 Access Token，然后任选其一写入：

```bash
# 交互式（推荐）
python3 scripts/setup_token.py

# 直接传入
python3 scripts/setup_token.py --token "你的token"

# 查看是否已配置（脱敏显示）
python3 scripts/setup_token.py --show

# 切换用户 / 清除
python3 scripts/setup_token.py --clear
```

配置一次后所有脚本自动读取。**未配置时调用任何工具都会失败并打印上述指引。**

注意事项：
- 批量请求务必控制频率，至少间隔 3 秒一次。
- **参数名必须与下方表格完全一致**（如 `spaceId` 与 `space_id` 不同，不可混用）。
- 可选参数不需要时不要传，也不要传空字符串。
- 工作目录为本 skill 根目录，用 `python3 scripts/xxx.py` 调用。

## 工具选用

| 场景 | 用哪个 |
|------|--------|
| 不知道有哪些空间 | `list_space` |
| 知道关键词 / 标签 / 过滤条件 | `search_memos`（语法见 ./references/搜索语法.md） |
| 只知道大概意思，不确定用词 | `query_topic_memos`（语义匹配） |
| 按时间顺序浏览某空间笔记 | `list_memos` |
| 已知笔记 ID，看全文 | `query_memo` |
| 写笔记前需要已有标签 | 先 `fetch_tags`，再把合适标签写进 content |
| 创建笔记 | `post_memo`；需要附件再 `add_attachment` |
| 改内容 / 标题 / 置顶 | `update_memo` |
| 看板相关 | 先 `kanban_list`，再按需 `kanban_detail` / `kanban_schema` 等 |

常见流程：
1. 写笔记：`list_space`（如需）→ `fetch_tags`（如需标签）→ `post_memo` →（可选）`add_attachment`
2. 找笔记：能精确匹配用 `search_memos`，否则用 `query_topic_memos`
3. 看板：`kanban_list` → `kanban_detail` / `kanban_schema` → 增删改笔记

笔记内容格式见 ./references/markdown.md。标签必须写在 content 里（如 `#工作`），不要发明用户从未用过的标签（先 `fetch_tags`）。

---

# 一、笔记操作

### list_space - 列出可用空间

每个笔记有且只能属于一个空间。

```bash
python3 scripts/list_space.py
```

### post_memo - 发表笔记

```bash
python3 scripts/post_memo.py --content "笔记内容" --title "标题" --spaceId "work"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --content | 是 | 笔记内容，换行用 `\n`，格式见 ./references/markdown.md |
| --title | 否 | 标题，默认为空，非必要不填 |
| --spaceId | 否 | 空间 ID，不填则为默认空间 |

成功时返回中含 `MemoId`，后续更新 / 附件 / 入看板都用这个 ID。创建后请告知用户笔记 ID。

### update_memo - 更新已有笔记

```bash
python3 scripts/update_memo.py --memo_id 130 --content "新内容" --title "新标题"
python3 scripts/update_memo.py --memo_id 131 --pin true
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --memo_id | 是 | 笔记 ID |
| --content | 否 | 笔记内容，不填则不更新，格式见 ./references/markdown.md |
| --pin | 否 | 是否置顶 `true` / `false`，不填则不更新 |
| --title | 否 | 笔记标题，不填则不更新 |

`--content`、`--title` 和 `--pin` 不能同时为空。私密笔记无法更新。

### fetch_tags - 拉取可用标签

为笔记加标签时，先拉取用户已用过的标签，从中选取合适的写入 content，不要自造标签。

```bash
python3 scripts/fetch_tags.py --space_id "work"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --space_id | 否 | 空间 ID，不填则为默认空间 |

### add_attachment - 为笔记增加附件（追加到已有后面）

```bash
python3 scripts/add_attachment.py --memo_id 130 --file /path/to/file.pdf --content_type application/pdf
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --memo_id | 是 | 笔记 ID |
| --file | 是 | 本地文件路径 |
| --content_type | 是 | MIME 类型，如 `text/plain`、`image/png`、`application/pdf` |

### query_memo - 查询单个笔记

```bash
python3 scripts/query_memo.py --memo_id 130
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --memo_id | 是 | 笔记 ID |

返回笔记全文、标题、创建时间等。私密笔记无法查看。

### list_memos - 列出笔记

```bash
python3 scripts/list_memos.py --offset 0 --limit 20 --spaceId "work"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --offset | 否 | 偏移量，默认 0 |
| --limit | 否 | 每页数量，默认 20，最大 100 |
| --spaceId | 否 | 空间 ID，不填则为默认空间 |

按时间倒序浏览某空间笔记；需要条件过滤请用 `search_memos`。

### query_topic_memos - 基于语义查找相关笔记

```bash
python3 scripts/query_topic_memos.py --query "Docker部署安装方法" --limit 10
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --query | 是 | 用自然语言描述要找的内容 |
| --limit | 否 | 返回数量上限，最大 30，默认 10 |
| --space_id | 否 | 空间 ID，不填则为默认空间 |

越靠前相关性越高。适合用户说不清精确用词的场景。

### search_memos - 按语法搜索笔记

```bash
python3 scripts/search_memos.py --query "#微信读书" --page 0 --pagesize 20
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --query | 是 | 搜索语法，详见 ./references/搜索语法.md |
| --space_id | 否 | 空间 ID，不填则为默认空间 |
| --page | 否 | 页码，默认 0 |
| --pagesize | 否 | 每页数量，最大 100，默认 20 |

返回顺序为笔记 ID 越大越靠前。调用前请阅读搜索语法文件。

---

# 二、看板操作

### kanban_list - 获取看板列表

```bash
python3 scripts/kanban_list.py
```

### kanban_create - 创建看板

```bash
python3 scripts/kanban_create.py --name "我的看板"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --name | 是 | 看板名称 |

### kanban_detail - 获取看板详情

```bash
python3 scripts/kanban_detail.py --kanban_id 1
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --kanban_id | 是 | 看板 ID |

结果包含看板及其所有笔记的详情。

### kanban_schema - 获取看板 schema

```bash
python3 scripts/kanban_schema.py --kanban_id 1
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --kanban_id | 是 | 看板 ID |

返回看板的 schema 定义（分组结构、字段配置等）。

### kanban_create_group - 创建看板分组

```bash
python3 scripts/kanban_create_group.py --kanban_id 1 --groupName "进行中"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --kanban_id | 是 | 看板 ID |
| --groupName | 是 | 分组名称 |

### kanban_add_memo_to_group - 添加笔记到分组

```bash
python3 scripts/kanban_add_memo_to_group.py --kanban_id 1 --group_id 1 --memoIds "1,2,3"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --kanban_id | 是 | 看板 ID |
| --group_id | 是 | 分组 ID |
| --memoIds | 是 | 笔记 ID 列表，逗号分隔 |
| --kanbanSrc | 否 | 添加到看板的原因；除非用户特别说明，否则不要填 |
| --groupSrc | 否 | 添加到分组的原因；除非用户特别说明，否则不要填 |

### kanban_update_memo - 更新看板中的笔记

```bash
python3 scripts/kanban_update_memo.py --kanban_id 1 --memo_id 10 --groupId 2 --isPin true --deadline 1700000000
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --kanban_id | 是 | 看板 ID |
| --memo_id | 是 | 笔记 ID |
| --groupId | 否 | 移动到目标分组 ID |
| --groupSrc | 否 | 移动原因；`groupId` 非空时可填，除非特别说明否则不要填 |
| --isPin | 否 | 是否置顶 `true` / `false` |
| --isMark | 否 | 是否高亮 `true` / `false` |
| --deadline | 否 | 截止时间戳（`<=0` 清除） |
| --tags | 否 | 标签（逗号分隔） |
| --isWatching | 否 | 是否关注 `true` / `false` |

所有可选字段不填则不更新。注意：这里的置顶参数是 `--isPin`，与笔记的 `--pin` 不同。

### kanban_remove_memo - 从看板移除笔记

```bash
python3 scripts/kanban_remove_memo.py --kanban_id 1 --memo_id 10
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --kanban_id | 是 | 看板 ID |
| --memo_id | 是 | 笔记 ID |
