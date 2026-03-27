---
name: context-budget-explore
description: |
  探索、需求、实施一体化的上下文预算工作流管理器。适用于长期探索、需求澄清、方案对比、迭代开发、质检闭环、跨对话续接、上下文过长、需要记录过程与决策的任务。优先在 Claude Code 中使用，但也可作为通用 skill：把阶段、任务、决策、经验、checkpoint、handoff 全部沉淀到仓库根目录 `.explore/`，让 AI 在长任务中始终有记录、有恢复点、有清晰过程。
  只要用户提到“探索一下”“先梳理需求”“边做边记录”“跨对话继续”“保存进度”“上下文太长”“这个任务会做很久”“想把过程沉淀下来”，都应该主动触发本 skill。
author: Claude Code
version: 3.0.0
date: 2026-03-27
allowed-tools:
  - TaskCreate
  - TaskGet
  - TaskList
  - TaskUpdate
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - Agent
---

# 上下文预算探索工作流

## 核心定位

这个 skill 是一个位于 superspec 外层的 mission/workflow 管理器。

它负责：

1. 管理任务全生命周期，而不是只盯当前一轮对话
2. 把需求、探索、实施、验证、交接过程沉淀到仓库根目录 `.explore/`
3. 在需要时调用内置 `skills/superspec/SKILL.md` 处理具体子任务
4. 在上下文过长、阶段结束或准备暂停时调用内置 `skills/session-handoff/SKILL.md` 生成交接

一句话：**superspec 负责把子任务做对，本 skill 负责让整件事有过程、有记录、有恢复点。**

## 适用范围

优先用于：

- 需求还不清楚，需要先探索、梳理、对齐
- 要做方案比较、代码调查、路径选择
- 一个任务会持续多轮，希望保留 workflow / todo / 决策 / 经验
- 既要做需求，又要做实现，还要保存完整过程
- 需要跨对话继续推进
- 用户明确提到“上下文太长”“太慢了”“先保存一下”“下次继续”

如果只是一次性的小修小改，且没有持续记录需求，可以不触发本 skill。

## 环境偏好

### Claude Code 优先

在 Claude Code 中，优先使用：

- `TaskCreate / TaskUpdate / TaskList` 管执行层任务
- `Read / Write / Edit / Glob / Grep` 管持久化文件
- `Agent` 做并行探索或拆分执行
- `Bash` 创建目录与运行验证命令

### 通用环境降级

如果缺少 TaskList、Agent 或 Bash，也仍然可以使用：

- 用 `session-tasks.md` 代替 TaskList
- 用 `.explore/` 下的状态文件承接上下文
- 无法自动执行时，写明确下一步与恢复指引

原则：**工具能力不同，但工作流与落盘结构保持一致。**

## 默认工作目录

默认使用仓库根目录：

```txt
.explore/
```

每个任务对应一个独立 mission：

```txt
.explore/<mission-slug>/
```

开始任务时：

1. 如果 `.explore/` 不存在，先创建
2. 为当前任务生成简短稳定的 `mission-slug`
3. 初始化 mission 目录及基础文件
4. 如果用户是在续接旧任务，优先读取已有 mission，而不是创建新目录

目录结构与模板说明，读取：

- `references/workspace-and-templates.md`

## 真相源

建立 mission 工作区后，以下内容优先级高于聊天历史：

- `workflow.md`
- `state.md`
- `decision-log.md`
- `learnings.md`
- `checkpoints.md`
- `spec/proposal.md`
- `spec/design.md`
- `spec/tasks.md`
- `handoffs/index.md`
- 最新 handoff 文件

聊天记录只用于辅助理解，**不是最终事实来源**。

## 路由规则

### 路由一：纯探索 / 需求梳理 / 方案比较

读取：

- `skills/superspec/SKILL.md`

走它的探索/对齐模式，但外层仍要更新：

- `workflow.md`
- `state.md`
- `decision-log.md`（必要时）
- `learnings.md`

### 路由二：方向已确定，需要产出 proposal / design / tasks

读取：

- `skills/superspec/SKILL.md`

把产物写到当前 mission 的 `spec/` 目录。

### 路由三：已批准，进入实施与验证

读取：

- `skills/superspec/SKILL.md`

按 `spec/tasks.md` 推进实现与验证。

### 路由四：需要 handoff / resume

读取：

- `skills/session-handoff/SKILL.md`

处理当前 mission 的多次 handoff。

## 标准流程

## 阶段 0：Classify

先判断当前请求属于哪类：

1. 只是探索，不做实现
2. 需要先对齐，再产出 spec
3. 已可实施，需要开发与验证
4. 需要 checkpoint / handoff / resume

然后明确告诉用户当前 route。

## 阶段 1：Mission Init

启动一个 mission 时，必须完成：

1. 定义任务目标
2. 定义范围内 / 范围外
3. 定义成功标准
4. 给出粗粒度阶段划分
5. 初始化 `.explore/<mission>/` 目录与基础文件
6. 创建执行层任务：
   - Claude Code 用 TaskList
   - 通用环境用 `session-tasks.md`

任务列表保持精简，通常 5-8 项。

## 阶段 2：Bounded Loop

每轮只推进一个清晰子目标：

```txt
选择下一个子目标
-> 读取 state / 最新 checkpoint / 最新 handoff / learnings
-> 选择内层路由（探索、提案、实施、验证）
-> 读取 skills/superspec/SKILL.md 执行
-> 外层回写 workflow / state / decision-log / learnings
-> 判断是否要 checkpoint 或 handoff
-> 进入下一轮
```

要求：

- 一次只推进一个主子目标
- 每轮结束都要留下可恢复记录
- 不允许只改代码、不更新状态文件

## 阶段 3：Checkpoint

以下时机必须考虑 checkpoint：

- 完成一个子任务后
- 切换到新子任务前
- 做出重要决策后
- 用户要求记录进度 / 保存状态
- 开始重复解释旧信息时
- 明显感觉上下文变重时

checkpoint 统一追加到：

- `checkpoints.md`

每个 checkpoint 至少包含：

- 当前阶段
- 本轮完成内容
- 本轮决策与原因
- 本轮沉淀的经验
- 待解决问题
- 下一步
- 可从活跃上下文中移除的内容

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
2. 读取 `state.md`
3. 读取 `handoffs/index.md`
4. 读取最新 handoff，必要时补读上一份
5. 验证 handoff 提到的文件和当前仓库状态是否仍成立
6. 从最新 handoff 的下一步继续

## 记录规则

- `workflow.md`：目标、范围、阶段、退出条件
- `state.md`：当前阶段、已确认事实、待解问题、下一步、最小活跃上下文
- `decision-log.md`：记会影响后续判断的决策
- `learnings.md`：只记可复用经验，不写流水账
- `checkpoints.md`：按阶段追加 checkpoint
- `spec/`：记录 proposal / design / tasks
- `handoffs/`：允许一个 mission 下有多次 handoff

## 硬性规则

1. 默认工作区就是仓库根目录 `.explore/`
2. 一个 mission 可以有多次 handoff，必须放在该 mission 的 `handoffs/` 目录
3. 主 skill 不依赖外部 superspec 或外部 session-handoff，只读取当前 skill 目录内子 skills
4. 日常输出保持短，不要每轮都写大总结
5. 已存在持久化文件时优先更新，而不是不断新建同类文件
6. 如果记录与当前仓库事实冲突，以当前事实为准，并回写修正
7. 内层执行完成后，必须回到外层更新记录，再进入下一轮

## 建议输出格式

平时只输出：

- 当前阶段
- 当前活跃任务
- 是否需要 checkpoint / handoff
- 刚更新了哪些文件
- 下一步

只有在 checkpoint 或 handoff 时，才输出完整阶段报告。

## 进阶读取顺序

启动或恢复 mission 时：

1. `references/workspace-and-templates.md`
2. 当前 mission 的 `state.md`
3. 当前 mission 的 `workflow.md`
4. 当前 mission 的 `learnings.md`
5. 当前 mission 的 `handoffs/index.md`（如存在）
6. `skills/superspec/SKILL.md` 或 `skills/session-handoff/SKILL.md`

## 运作良好的标志

- 需求、探索、实施都走同一个 mission 工作区
- 即使跨对话，AI 也能快速恢复，不依赖翻聊天记录
- 决策和经验可以从文件中快速查到
- 一个 mission 可以积累多份 handoff，而不是只保留一份摘要
- 即使换环境，仍可以通过 `.explore/` 目录继续工作
- 整个过程像“有状态的 superspec 外层管理器”，而不是一次性聊天
