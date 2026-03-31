# 阶段详细流程与记录规则

本文件包含各阶段的完整执行指南和记录归档策略。由 `SKILL.md` 按需指引读取。

## 阶段 0：Classify

先判断当前请求属于哪类：

1. 只是探索，不做实现
2. 需要先对齐，再产出 spec
3. 已可实施，需要开发与验证
4. 需要 checkpoint / handoff / resume

然后明确告诉用户当前 route，并说明本轮只推进哪个主子目标。

## 阶段 1：Mission Init

启动一个 mission 时，必须完成：

1. 定义任务目标
2. 定义范围内 / 范围外
3. 定义成功标准
4. 给出粗粒度阶段划分
5. 初始化 `.explore/<mission>/` 目录及基础文件
6. 创建执行层任务：
   - Claude Code 用 TaskList
   - 通用环境用 `session-tasks.md`

任务列表保持精简，通常 5-8 项。

### Mission Init 后的强制流程

Mission Init 只是创建了工作区骨架，不代表可以开始写代码。

Init 完成后，首轮 Bounded Loop 必须按以下顺序推进：

1. 首先走 Align：读取 `skills/spark-workflow/SKILL.md`，进入其 Align 阶段，触发 brainstorming 对齐需求方向
2. 然后产出 spec：Align 完成后进入 Propose，在 `spec/` 目录下产出 `proposal.md`、`design.md`、`tasks.md`
3. 等待用户批准 spec：用户必须明确批准 spec 后，才能进入实施
4. 才能写代码：按 `spec/tasks.md` 逐项推进实施

绝对禁止的流程：

- Mission Init -> 直接创建 TaskList 写代码
- Mission Init -> 只写 `workflow.md` / `state.md` 就开始改文件

正确的流程：

- Mission Init -> Align -> Propose -> 用户批准 -> Apply

## 阶段 2：Bounded Loop

每轮只推进一个清晰子目标：

```txt
选择下一个子目标
-> 读取 state / 最新 handoff / 必要时补读 workflow 或 learnings
-> 选择内层路由（探索、提案、实施、验证）
-> 读取 skills/spark-workflow/SKILL.md 执行
-> 外层回写 workflow / state / decision-log / learnings
-> 判断是否要 checkpoint 或 handoff
-> 进入下一轮
```

要求：

- 一次只推进一个主子目标
- 每轮结束都要留下可恢复记录
- 不允许只改代码、不更新状态文件
- 如果最新持久化记录与仓库事实冲突，先以仓库事实修正，再继续推进

## 阶段 3：Checkpoint

以下时机必须考虑 checkpoint：

- 完成一个子任务后
- 切换到新子任务前
- 做出重要决策后
- 用户要求记录进度 / 保存状态
- 开始重复解释旧信息时
- 明显感觉上下文变重时

checkpoint 统一追加到 `checkpoints.md`。

每个 checkpoint 至少包含：

- 当前阶段
- 本轮完成内容
- 本轮决策与原因
- 本轮沉淀的经验
- 待解决问题
- 下一步
- 可从活跃上下文中移除的内容

### Checkpoint 滚动窗口

`checkpoints.md` 只保留最近 3 个完整 checkpoint。当写入第 4 个时：

1. 把最早的 checkpoint 移到 `checkpoints-archive.md`，只追加不覆盖
2. 在被移走的位置留一行摘要：`> [已归档] YYYY-MM-DD - 一句话概括`
3. `checkpoints-archive.md` 不主动读取，只在需要回溯历史时按需查看

这样 `checkpoints.md` 会始终保持轻量，恢复时不会加载过多历史。

## 阶段 4：上下文预算控制

出现以下信号时，应压缩上下文：

- 对话轮次明显偏长
- 开始反复复述已确定结论
- 回复速度变慢
- 用户说“太慢了 / 太贵了 / 保存一下 / 下次继续”
- 一个阶段已经结束，适合切换

处理优先级：

1. 轻度：回复只保留结论，不复述推导
2. 中度：补写 checkpoint，并明确哪些内容可遗忘
3. 重度：创建 handoff，建议下次从 handoff 恢复

## 阶段 5：Handoff / Resume

### 创建 handoff

当任务要暂停、阶段结束、上下文过重时：

1. 读取 `skills/session-handoff/SKILL.md`
2. 在 `handoffs/` 写入新的时间戳 handoff 文件
3. 更新 `handoffs/index.md`
4. 同步更新 `state.md` 的当前状态、下一步、最新 handoff

### 恢复任务

当用户说“继续上次的探索/需求/开发”时：

1. 找到对应 mission
2. 读取 `state.md`，这是最重要的恢复入口
3. 读取最新 handoff，只默认读最新 1 份
4. 验证 handoff 提到的文件和当前仓库状态是否仍成立
5. 从最新 handoff 的下一步继续
6. 如果最新 handoff 信息不足，再按需读取 `handoffs/index.md` 或上一份 handoff

## 记录规则

- `workflow.md`：记录任务目标、范围边界、阶段规划、当前阶段与退出条件
- `state.md`：记录当前阶段、已确认事实、待解问题、下一步与最小活跃上下文
- `decision-log.md`：只记录会影响后续判断的决策，不写流水账
- `learnings.md`：只记录可复用经验、低成本技巧与应避免的坑
- `checkpoints.md`：保留最近 3 个完整 checkpoint
- `checkpoints-archive.md`：保存滚动归档的旧 checkpoint，默认不主动读取
- `spec/`：记录 `proposal.md`、`design.md`、`tasks.md`
- `handoffs/`：允许一个 mission 下有多次 handoff

### Decision-Log 自动摘要

当 `decision-log.md` 中完整决策记录超过 5 条时：

1. 保留最近 5 条完整记录
2. 更早的决策压缩为一行摘要格式：`> [#序号] YYYY-MM-DD - 选择了 X，因为 Y`
3. 摘要放在文件顶部的“历史决策摘要”区域，完整记录放在下方

这样既保留可追溯性，也避免文件无限膨胀。

## 反模式

| 反模式 | 为什么有害 | 正确做法 |
|--------|------------|----------|
| Mission Init 后直接写代码 | 跳过需求对齐，可能做错方向 | Init 后首轮必须走 Align |
| 只创建 `workflow.md` 不创建 `spec/` | 没有可审查方案，用户无法批准 | Align 后必须 Propose，产出 `spec/` |
| 用 TaskList 替代 `spec/tasks.md` | TaskList 是执行跟踪，`spec/tasks.md` 是方案设计 | 先有 `spec/tasks.md`，再用 TaskList 跟踪执行 |
| `spec/` 未获批准就进入实施 | 用户可能不认可方案 | 明确等待用户批准后再写代码 |
| 跳过 brainstorming 直接出方案 | 缺少方案比较与取舍讨论 | 通过 spark-workflow 的 Align 阶段触发 brainstorming |
