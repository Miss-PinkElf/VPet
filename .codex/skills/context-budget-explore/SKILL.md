---
name: context-budget-explore
description: |
  探索、需求、实施一体化的上下文预算工作流管理器。适用于长期探索、需求澄清、方案对比、迭代开发、质检闭环、跨对话续接、上下文过长、需要记录过程与决策的任务。优先在 Claude Code 中使用，但也可作为通用 skill：把阶段、任务、决策、经验、checkpoint、handoff 全部沉淀到仓库根目录 `.explore/`，让 AI 在长任务中始终有记录、有恢复点、有清晰过程。
  只要用户提到“探索一下”“先梳理需求”“边做边记录”“跨对话继续”“保存进度”“上下文太长”“这个任务会做很久”“想把过程沉淀下来”，都应该主动触发本 skill。
author: Claude Code
version: 3.1.0
date: 2026-03-31
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

这个 skill 是一个位于 spark-workflow 外层的 mission/workflow 管理器。

它负责：

1. 管理任务全生命周期，而不是只盯当前一轮对话
2. 把需求、探索、实施、验证、交接过程沉淀到仓库根目录 `.explore/`
3. 在需要时调用内置 `skills/spark-workflow/SKILL.md` 处理具体子任务
4. 在上下文过长、阶段结束或准备暂停时调用内置 `skills/session-handoff/SKILL.md` 生成交接

一句话：**spark-workflow 负责把子任务做对，本 skill 负责让整件事有过程、有记录、有恢复点。**

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

- Claude Code 中优先用 `TaskCreate / TaskUpdate / TaskList` 管执行层，用 `Read / Write / Edit / Glob / Grep` 管持久化，用 `Agent` 做并行探索或拆分执行。
- 若缺少 TaskList、Agent 或 Bash，则退化为 `session-tasks.md` + `.explore/` 状态文件；工具能力不同，但工作流与落盘结构保持一致。

## 默认工作目录

默认工作区为仓库根目录 `.explore/`，每个任务对应 `.explore/<mission-slug>/`。

启动或恢复任务前，先读取：

- `references/workspace-and-templates.md`

## 真相源

建立 mission 工作区后，以 `.explore/<mission>/` 内持久化文件为准；聊天记录只用于辅助理解，不是最终事实来源。

优先信任：

- `state.md`
- `workflow.md`
- `decision-log.md`
- `learnings.md`
- `spec/` 下的 proposal / design / tasks
- 最新 handoff

## 路由规则

| 路由 | 场景 | 前置条件 | 读取 | 外层更新 |
|------|------|----------|------|----------|
| 一 | 纯探索 / 需求梳理 / 方案比较 | 无 | `skills/spark-workflow/SKILL.md` | `workflow.md` / `state.md` / `decision-log.md` / `learnings.md` |
| 二 | 方向已确定，产出 proposal / design / tasks | 路由一已完成，或需求已足够清晰 | `skills/spark-workflow/SKILL.md` | `spec/` 目录与 `state.md` |
| 三 | 已批准，进入实施与验证 | `spec/proposal.md` 和 `spec/tasks.md` 已存在，且已获用户批准 | `skills/spark-workflow/SKILL.md` | 按 `spec/tasks.md` 推进，并持续回写状态文件 |
| 四 | 需要 handoff / resume | 无 | `skills/session-handoff/SKILL.md` | `handoffs/` 与 `state.md` |

### 路由强制顺序

- Mission Init 完成后，首轮 Bounded Loop 必须先走路由一或路由二，进入 spark-workflow 的 Align 阶段。
- 路由三有前置门禁：`spec/proposal.md` 和 `spec/tasks.md` 必须已存在且已获用户批准；没有 spec 就写代码是本 skill 最严重的反模式。
- 即使用户给出的需求文档已经很详细，也至少要走一次 Mini Align 做确认，而不是直接进入实施。

## 标准流程概览

| 阶段 | 名称 | 核心动作 |
|------|------|----------|
| 0 | Classify | 判断请求类型，选择路由，并明确告知用户 |
| 1 | Mission Init | 定义目标/范围/成功标准，初始化 mission 工作区 |
| 2 | Bounded Loop | 每轮推进一个子目标，并在结束时回写状态文件 |
| 3 | Checkpoint | 阶段切换、关键决策或上下文变重时写 checkpoint |
| 4 | 上下文预算控制 | 轻度精简 -> 中度 checkpoint -> 重度 handoff |
| 5 | Handoff / Resume | 创建交接或从最新 handoff 恢复 |

进入具体阶段执行时，读取：

- `references/phases-and-rules.md`

## 硬性规则

1. 默认工作区就是仓库根目录 `.explore/`
2. 一个 mission 可以有多次 handoff，必须放在该 mission 的 `handoffs/` 目录
3. 主 skill 不依赖外部 spark-workflow 或外部 session-handoff，只读取当前 skill 目录内子 skills
4. 日常输出保持短，不要每轮都写大总结
5. 已存在持久化文件时优先更新，而不是不断新建同类文件
6. 如果记录与当前仓库事实冲突，以当前事实为准，并回写修正
7. 内层执行完成后，必须回到外层更新记录，再进入下一轮
8. Mission Init 后首轮必须走 Align，不能跳过需求对齐直接写代码
9. `spec/proposal.md` 和 `spec/tasks.md` 未创建或未获用户批准前，禁止进入路由三实施

## 建议输出格式

平时只输出：当前阶段、当前活跃任务、是否需要 checkpoint / handoff、刚更新了哪些文件、下一步。

只有在 checkpoint 或 handoff 时，才输出完整阶段报告。

## 读取顺序

启动或恢复 mission 时，按需分层读取：

1. `references/workspace-and-templates.md`
2. 当前 mission 的 `state.md`
3. 最新 handoff
4. 当前 mission 的 `workflow.md` 或 `learnings.md`（仅在需要补充上下文时）
5. `references/phases-and-rules.md`
6. `skills/spark-workflow/SKILL.md` 或 `skills/session-handoff/SKILL.md`
