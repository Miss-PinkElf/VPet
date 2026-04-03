---
name: session-handoff
description: 在 context-budget-explore 中，用于当前 mission 的交接、暂停恢复、上下文压缩和多次 handoff 管理。适用于用户说“保存进度”“下次继续”“创建交接”“上下文太长”或任务阶段性收尾时。默认把 handoff 写到 `.explore/<mission>/handoffs/`，并维护 `index.md`，支持一个 mission 下多次 handoff 串联。
---

# Session Handoff（内置版）

这是 `context-budget-explore` 的内置 handoff 子 skill。

它不是全局 handoff 池，而是**当前 mission 内的 handoff 管理器**。

## 核心原则

1. handoff 默认属于当前 mission
2. 一个 mission 可以有多次 handoff
3. 每次 handoff 都是独立文件，按时间顺序保存在 `handoffs/`
4. `handoffs/index.md` 负责维护索引
5. 恢复时优先读最新 handoff，必要时再补读上一份
6. handoff 只是恢复入口，不替代 `state.md` 与 `spec/` artifact

## 默认位置

```txt
.explore/<mission-slug>/handoffs/
```

建议文件命名：

```txt
YYYY-MM-DD-<序号>-<slug>.md
```

例如：

- `2026-03-27-001-init.md`
- `2026-03-27-002-checkpoint.md`
- `2026-03-27-003-resume-ready.md`

## 模式选择

### 模式一：创建 handoff

适用场景：

- 用户要求保存进度
- 准备暂停当前工作
- 对话上下文明显过长
- 一个阶段结束，适合切换下个阶段
- 已做出较多决策，希望把恢复成本降下来

### 模式二：从 handoff 恢复

适用场景：

- 用户说继续上次任务
- 用户明确提到某个 mission 或某份 handoff
- 当前会话需要从之前的阶段继续推进

## 创建 handoff 流程

1. 确认当前 mission 已存在
2. 读取：
   - `../../references/workspace-and-templates.md`（如需要确认结构）
   - 当前 mission 的 `state.md`
   - 当前 mission 的 `workflow.md`
   - 当前 mission 的 `spec/` artifact（如存在）
   - 当前 mission 的最新 checkpoint（如存在）
3. 使用模板创建新的 handoff 文件：
   - `assets/templates/handoff-template.md`
4. 在 `handoffs/index.md` 追加一条索引记录
5. 同步更新 `state.md`：
   - 当前状态
   - 下一步
   - 最新 handoff
6. 告知用户 handoff 位置，以及下次如何恢复

## 恢复流程

1. 先读取 `handoffs/index.md`
2. 找到最新 handoff
3. 完整读取 handoff 文件
4. 参考 `references/resume-checklist.md` 核验上下文
5. 必要时参考 `references/staleness-checklist.md` 判断 handoff 是否过期
6. 再读取：
   - `state.md`
   - `workflow.md`
   - `spec/` 中相关 artifact
7. 从 handoff 的“立即下一步”继续

## 多次 handoff 管理

每个 mission 下允许多次 handoff：

```txt
handoffs/
├── index.md
├── 2026-03-27-001-init.md
├── 2026-03-27-002-mid-review.md
└── 2026-03-27-003-resume-ready.md
```

管理规则：

- 最新 handoff 在 `index.md` 中显式标明
- 较早 handoff 可标记为 `superseded`，但不删除
- 如果最新 handoff 只覆盖局部阶段，恢复时可补读上一份
- 不要把所有历史都不断覆盖到同一个 `handoff.md`

## 必填信息

创建 handoff 时，字段要求参考：

- `references/handoff-fields.md`

至少包含：

- 当前目标
- 当前阶段
- 当前进度
- 本轮完成内容
- 关键决策与原因
- 关键文件/产物
- 风险 / 阻塞项 / 开放问题
- 立即下一步
- 恢复指引

## 约束

- handoff 不能替代 `state.md`
- handoff 不能省略“下一步”
- handoff 不要包含密钥、令牌、密码等敏感信息
- 如果 handoff 内容与当前仓库状态冲突，以当前仓库事实为准，并更新记录
- 如果一个阶段刚结束，优先先写 checkpoint，再决定是否生成 handoff

## 推荐阅读顺序

创建 handoff 前：

1. 当前 mission 的 `state.md`
2. 当前 mission 的 `workflow.md`
3. 当前 mission 的 `checkpoints.md`
4. 当前 mission 的 `spec/` artifact
5. `assets/templates/handoff-template.md`

恢复 handoff 时：

1. `handoffs/index.md`
2. 最新 handoff
3. `references/resume-checklist.md`
4. `references/staleness-checklist.md`
5. 当前 mission 的 `state.md`
6. 当前 mission 的 `spec/` artifact
