---
name: cflow_skill
description: 当用户在 cflow/笔记系统中执行笔记操作时（创建、修改、查询、上传附件、查标签、搜索、评论、时间胶囊、看板操作），可以使用该技能。
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
| 更新已有附件 | `update_attachment` |
| 下载笔记附件到本地 | `download_attachment` |
| 给笔记配 cflow 数据库 | `create_cflow_db`；之后可用 `exec_db` 执行 SQL |
| 操作 cflow 数据库附件（SQL 查询/建表/增删改） | `exec_db` |
| 改内容 / 标题 / 置顶 | `update_memo` |
| 评论 / 回复评论 | `list_comments` 看已有评论，`create_comment` 发表 |
| 时间胶囊 | `list_time_capsule` 看列表；已送达的用 `query_time_capsule` 看全文 |
| 看板相关 | 先 `kanban_list`，再按需 `kanban_detail` / `kanban_schema` 等 |

常见流程：
1. 写笔记：`list_space`（如需）→ `fetch_tags`（如需标签）→ `post_memo` →（可选）`add_attachment`
2. 找笔记：能精确匹配用 `search_memos`，否则用 `query_topic_memos`
3. 评论 / 回复：`query_memo` 找到笔记 → `list_comments` 看已有评论 → `create_comment`（回复时带 `--parent_comment_id`）
4. 看板：`kanban_list` → `kanban_detail` / `kanban_schema` → 增删改笔记

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
python3 scripts/add_attachment.py --memo_id 130 --file /path/to/file.pdf
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --memo_id | 是 | 笔记 ID |
| --file | 是 | 本地文件路径 |

### update_attachment - 覆盖更新已有附件

```bash
python3 scripts/update_attachment.py --attachment_id 456 --file /path/to/new.pdf
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --attachment_id | 是 | 目标附件 ID，即笔记 `resourceList` 里的 `id` |
| --file | 是 | 新文件的本地路径 |

只更新附件内容与大小，文件名、类型、挂载关系保持不变（本地文件名无需与线上一致）。**仅支持普通附件**（PDF/图片/音视频/Office/文本等）；内置类型附件（脑图、甘特图、diagram、drawio、excalidraw、MD 幻灯、cflow 数据库）不支持覆盖更新，其中 cflow 数据库只能用 `exec_db` 执行 SQL 修改。私密笔记的附件无法更新。

### download_attachment - 下载笔记附件到本地

```bash
python3 scripts/download_attachment.py --attachment_id 456 --dir /tmp
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --attachment_id | 是 | 附件 ID，即笔记 `resourceList` 里的 `id`（`query_memo` 可查到） |
| --dir | 否 | 保存目录，默认当前目录，不存在会自动创建 |
| --filename | 否 | 保存文件名，默认用附件原文件名 |

返回本地保存路径、文件大小等。私密笔记的附件无法下载。

### create_cflow_db - 为笔记创建 cflow 数据库附件

```bash
python3 scripts/create_cflow_db.py --memo_id 130 --filename "记账本"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --memo_id | 是 | 笔记 ID |
| --filename | 是 | 数据库名称 |

- 成功返回附件资源，`id` 即后续 `exec_db --attachment_id` 要用的 ID

### exec_db - 对 cflow 数据库附件执行 SQL

```bash
python3 scripts/exec_db.py --attachment_id 456 --sql "SELECT * FROM bills LIMIT 20"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --attachment_id | 是 | cflow 数据库附件 ID，即笔记 `resourceList` 里的 `id` |
| --sql | 是 | SQL 文本（SQLite 方言），多条语句用 `;` 分隔，整批一个事务 |

- 支持建表/删表/增删改查/索引/视图/JOIN/CTE 等；`DESC 表名` 简写可用；表结构用 `SELECT sql FROM sqlite_master WHERE type='table'` 查看
- **插入/变更多条数据务必合并成一次调用**（多条语句用 `;` 分隔，或一条多值 `INSERT`），不要每条数据调一次：逐条调用大部分会被 429 拒绝
- 成功时 `results` 只含**最后一条语句**的结果（查询带 `columns`/`rows`，变更带 `affected`）；`writeCount` 为本批写操作语句条数
- 任一语句失败整批回滚，返回 400 且带 `statementIndex`（失败语句序号，从 0 开始）
- 乐观锁：执行时自动带当前版本号，库被其它端同时修改过会返回 409，重新执行即可

### create_comment - 发表评论

```bash
python3 scripts/create_comment.py --memo_id 130 --content "评论内容"
python3 scripts/create_comment.py --memo_id 130 --content "回复内容" --parent_comment_id 12
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --memo_id | 是 | 笔记 ID |
| --content | 是 | 评论内容，换行用 `\n` |
| --parent_comment_id | 否 | 回复某条评论时传该评论的 ID，不填则为普通评论 |

回复评论前先用 `list_comments` 拿到目标评论的 `commentId`。私密笔记无法评论。

### list_comments - 拉取笔记的评论

```bash
python3 scripts/list_comments.py --memo_id 130
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --memo_id | 是 | 笔记 ID |

返回该笔记全部评论，含 `commentId`、`content`、`parentCommentId`（回复目标）、`createdBy`（`user` 用户 / `ai` 助手）、创建时间。私密笔记无法查看。

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

### list_time_capsule - 列出时间胶囊

```bash
python3 scripts/list_time_capsule.py
```

返回当前用户的全部时间胶囊。`state` 为 `unread` 的尚未送达，`memoId` / `content` / `message` / `sendAt` 会显示为 `***`。`sent` 为已送达，列表里即可看到正文。

### query_time_capsule - 查看单个时间胶囊

```bash
python3 scripts/query_time_capsule.py --time_capsule_id 12
```

| 参数 | 必填 | 说明 |
|------|------|------|
| --time_capsule_id | 是 | 时间胶囊 ID，来自 `list_time_capsule` 的 `timeCapsuleId` |

只用于已送达（`sent`）的胶囊，返回封存的笔记正文、留言和发送时间。尚未送达的会拒绝查看。

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
