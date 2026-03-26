---
name: context-budget-explore
description: |
  探索工作流管理器，用于长期探索、质检工作流、agent 闭环、迭代优化等场景，解决上下文过长导致的费用高、速度慢问题。
  外层管理 workflow/todolist + 经验沉淀，内层通过 superspec 走开发流程，达到上下文阈值时自动触发 session-handoff 生成交接文档，支持跨对话续接。
  当用户要做以下事情时，积极触发本 skill：
  - 探索性工作（质检工作流、agent 闭环、迭代优化、方案对比）
  - 维护 todolist/workflow、记录进度、沉淀经验
  - 提到"上下文太长"、"跨对话继续"、"记录进度"、"太慢了"、"太贵了"
  - 长时间迭代优化、反复调试某个功能
  - 需要跨多轮对话持续推进的任务
  - 在本仓库中，用户提到“毕设”“毕业设计”“阶段推进”“路线图”“记录过程”“答辩”“继续桌宠项目”“继续上次桌宠”“写论文材料”“整理开发过程”时，必须优先触发
  - 在本仓库中，用户提到“桌宠”“前后端闭环”“简单对话”“记忆系统”“OpenSpec 任务状态”“阶段完成度”时，如果目标是持续推进而非单次问答，也应触发
  即使用户没有明确说"用 context-budget-explore"，只要是探索性、迭代性的长任务，也应该主动使用。
author: Claude Code
version: 2.1.0
date: 2026-03-24
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
  - Skill
  - Agent
---

# 探索工作流管理器

## 解决什么问题

探索性工作（质检工作流、agent 闭环、迭代优化）很容易陷入以下困境：

- 上下文越来越长 → 速度变慢、费用增加
- 多个并行线索堆在一个对话里 → 混乱
- 做过的决策没记下来 → 反复讨论同一个问题
- 优化经验没沉淀 → 下次还踩同样的坑
- 对话中断后 → 无法快速恢复

本 skill 的核心理念：**活跃上下文保持精简，持久化状态保持丰富**。

## 架构：三层协作

```
┌──────────────────────────────────────────────┐
│  context-budget-explore（外层管理器）           │
│  职责：workflow 管理 / 经验沉淀 / 上下文预算     │
│                                              │
│  ┌────────────────────────────────────┐      │
│  │  superspec（内层流程引擎）            │      │
│  │  职责：具体任务走 propose → apply     │      │
│  │  每完成一个迭代 → 自动回报外层         │      │
│  └────────────────────────────────────┘      │
│                                              │
│  ┌────────────────────────────────────┐      │
│  │  session-handoff（续接引擎）          │      │
│  │  职责：上下文过长时生成交接文档         │      │
│  │  下次对话通过 handoff 快速恢复         │      │
│  └────────────────────────────────────┘      │
└──────────────────────────────────────────────┘
```

- **外层**负责全局进度、经验沉淀、上下文预算
- **内层 superspec**负责每个具体开发任务的流程（classify → align → propose → apply → verify）
- **session-handoff**在上下文接近极限时自动生成交接文档

## 项目特化：agent-desktop-pet 毕设版

在当前仓库 `/Users/mobius/Documents/111AAA-code/agent-desktop-pet` 中，本 skill 不是抽象通用工作流，而是**桌宠毕业设计推进管理器**。触发后默认这样理解用户意图：

- 用户通常不是只想解决一个零散问题，而是想继续推进整份毕业设计
- 记录的目标不仅是续接开发，还包括后续写论文、写周报、准备答辩
- 需要把“全局阶段推进”和“局部技术调试”分层管理，避免所有记录都堆在一个目录

### 本项目中的默认记录分层

#### 1. 全局主线记录

优先使用：

```text
.codex/explore/desktop-pet-graduation-roadmap/
```

这个目录负责：

- 毕设当前阶段
- 阶段目标和边界
- 当前主线任务
- 决策沉淀
- 经验沉淀
- 续接 handoff

#### 2. 专项问题记录

按主题使用独立 explore 目录，例如：

```text
.codex/explore/desktop-pet-ui-debug-v2/
```

这类目录只记录某个具体问题或功能迭代，例如：

- 边框联动缩放
- 后端简单对话联调
- 记忆系统调研

#### 3. 功能实现真相源

当任务进入具体实现时，默认与 OpenSpec 联动，真相源是：

```text
openspec/changes/desktop-pet-companion-roadmap/
```

尤其是：

- `proposal.md`
- `design.md`
- `tasks.md`

#### 4. 产品和论文需求真相源

默认优先读取：

- `zzz-doc/zzz-prompt-debug/origin/原始PRD.md`
- `zzz-doc/zzz-prompt-debug/origin/1.md`
- `zzz-doc/zzz-prompt-debug/plan/桌宠项目详细PRD.md`
- `zzz-doc/桌宠毕设过程记录指南.md`
- `references/agent-desktop-pet-workflows.md`

如果用户是在问“我现在需要干什么”“新需求怎么推进”“修 bug 怎么走”“什么时候做 checkpoint / handoff”，优先读取：

- `references/agent-desktop-pet-workflows.md`

### 本项目中的稳定触发规则

在本仓库里，只要满足以下任一情况，就应默认触发本 skill，而不是把它当成一次性聊天：

- 用户说“继续毕设”“继续桌宠项目”“继续上次”
- 用户说“帮我记录一下过程”“阶段推进一下”“整理当前状态”
- 用户说“我要开始下一阶段”“更新任务状态”“同步 OpenSpec”
- 用户说“后面还会继续做”“这个要长期推进”“把这轮写进文档”
- 用户提到“论文怎么写”“答辩怎么讲”“想留开发过程记录”

### 本项目中的默认启动动作

在当前仓库触发后，优先按下面顺序工作：

1. 读取全局 roadmap：
   - `.codex/explore/desktop-pet-graduation-roadmap/handoff.md`
   - `.codex/explore/desktop-pet-graduation-roadmap/state.md`
   - `.codex/explore/desktop-pet-graduation-roadmap/learnings.md`
2. 如任务是某个专项问题，再读取对应专项目录
3. 如任务涉及实现阶段，读取 OpenSpec 的 `proposal.md / design.md / tasks.md`
4. 判断这轮是：
   - 只更新记录
   - 记录 + 调整任务状态
   - 记录 + 进入 superspec 做实现

### 本项目中的默认阶段划分

如果用户没有另行指定，默认将毕设推进理解为以下主线：

1. 前端展示与交互稳定
2. 前后端简单对话闭环
3. 基础记忆与配置能力
4. 轻量上下文感知
5. 演示脚本、论文材料与答辩收口

### 本项目中的记录要求

每轮有实质推进时，至少回写：

- 全局 `state.md`
- 全局 `decision-log.md`
- 全局 `learnings.md`

如果这轮是专项调试，再补对应专项目录的：

- `state.md`
- `handoff.md`
- 必要时 `workflow.md`

如果这轮已经影响阶段完成度，还要同步：

- `openspec/changes/desktop-pet-companion-roadmap/tasks.md`

关键要求：

- 记录不只写“做了什么”，还要写“为什么这样做、放弃了什么、下一步是什么”
- 用词要适合后续提炼为论文材料
- 所有新增记录保持简体中文

## 四层记忆模型

1. **执行层（TaskList）** — 当前会话的 todolist，跟踪进行中的任务
2. **状态层（持久化文件）** — workflow.md / state.md 等，跨 checkpoint 存活
3. **决策层（经验日志）** — decision-log.md / learnings.md，可复用的洞察
4. **回忆层（跨对话记忆）** — handoff.md + session-handoff 交接文档

## 工作流程

### 阶段一：启动（Mission Init）

收到探索性任务时：

1. **定义任务边界**
   - 目标是什么
   - 范围边界（做什么/不做什么）
   - 成功标准
   - 预估迭代次数（粗略即可）

2. **创建执行脚手架**
   - 在 TaskList 创建任务列表（保持精简，5-8 个有意义的任务）
   - 确定工作目录，创建持久化文件

3. **初始化持久化文件**
   - 在用户指定的工作目录下创建文件（默认 `.codex/explore/`）
   - 如果是续接任务，先读取已有的 handoff.md 恢复状态

### 当前仓库的 Mission Init 默认模板

如果用户没有指定目录，在本仓库默认这样初始化：

1. 全局主线：
   - `.codex/explore/desktop-pet-graduation-roadmap/`
2. 当前专项：
   - 按主题创建 `.codex/explore/desktop-pet-<topic>/`
3. 真相源同步：
   - `openspec/changes/desktop-pet-companion-roadmap/tasks.md`
4. 论文/需求参考：
   - `zzz-doc/zzz-prompt-debug/plan/桌宠项目详细PRD.md`

### 阶段二：迭代执行（Bounded Loop）

每个迭代遵循这个闭环：

```
┌→ 选择子目标（从 TaskList 取下一个）
│
├→ 使用 superspec 执行
│   - 如果是开发任务 → superspec 的 propose → apply → verify
│   - 如果是探索任务 → 调研 → 总结 → 记录
│
├→ 迭代回报（每完成一轮自动执行）
│   - 更新 state.md（当前状态）
│   - 追加 decision-log.md（本轮决策）
│   - 追加 learnings.md（本轮经验）
│   - 更新 TaskList（标记完成，发现新任务则添加）
│
├→ 上下文预算检查
│   - 如果对话已经很长 → 触发 checkpoint
│   - 如果接近极限 → 触发 session-handoff
│
└→ 进入下一个迭代
```

### 阶段三：Checkpoint（阶段性保存）

以下时机触发 checkpoint：

- 一个子任务完成
- 切换到新的子任务前
- 做了重要决策后
- 感觉上下文开始变长变重时
- 用户主动要求

Checkpoint 输出格式：

```markdown
## Checkpoint [编号] - [日期时间]
### 当前阶段
...

### 本轮完成了什么
- ...

### 本轮做的决策
- 决策：...
- 原因：...

### 沉淀的经验
- ...

### 待解决的问题
- ...

### 下一步
- ...

### 可以从活跃上下文中移除的内容
- ...（这一项必填，明确标出哪些信息不再需要留在对话中）
```

### 阶段四：上下文预算管理

**预算信号判断**（不需要精确计数，通过以下信号判断）：

- 对话轮次已经超过 15-20 轮 → 考虑 checkpoint
- 开始反复解释之前已经讨论过的内容 → 需要 checkpoint
- 单次回复开始变慢 → 上下文可能过长
- 用户说"太慢了"/"太贵了" → 立即触发

**预算控制手段**：

1. **轻度压缩**：在回复中只引用结论，不重复推导过程
2. **中度压缩**：创建 checkpoint，明确标出可以遗忘的内容
3. **重度压缩**：触发 session-handoff，生成完整交接文档，建议用户开新对话

### 阶段五：跨对话续接

当需要跨对话时：

1. **生成交接文档**：调用 `session-handoff` skill，生成标准交接文档
   - 交接文档会包含：当前目标、进度、决策、下一步
   - 存储在当前 explore 目录下的 `handoffs/` 子目录，例如 `.codex/explore/desktop-pet-ui-debug-v2/handoffs/`

2. **同时更新持久化文件**：
   - 更新 handoff.md（精简版，快速恢复用）
   - 更新 state.md（完整状态）
   - 确保 learnings.md 是最新的

3. **恢复时**：
   - 用户在新对话中说"继续上次的探索"或类似的话
   - 读取最新的 handoff.md 和 state.md
   - 恢复 TaskList
   - 从上次的 next step 继续

## 自动经验沉淀机制

这是本 skill 的核心差异化能力。每次迭代完成后，自动提取并记录：

### 记录什么

```markdown
# learnings.md 追加格式

## [日期] 第 N 轮迭代经验

### 有效的做法
- ...（什么方法奏效了，为什么）

### 无效的做法
- ...（什么方法失败了，为什么）

### 降低成本/延迟的技巧
- ...

### 导致上下文膨胀的行为
- ...

### 可复用的策略
- ...

### 下次要避免的坑
- ...
```

### 何时沉淀

- 每完成一个 superspec 的 apply → verify 周期
- 每次 debug 成功解决问题后
- 每次方案对比做出选择后
- 每次 checkpoint 时

### 经验复用

- 每次开始新迭代前，快速浏览 learnings.md，避免重复踩坑
- 如果某个经验被反复引用（3次以上），建议用户考虑将其固化为规范或 skill

## 与 superspec 的集成

当内层任务需要走开发流程时：

1. **外层** 选定子目标，创建任务上下文
2. **调用 superspec**：`/superspec` 走标准流程
   - classify → align → propose → apply → verify
3. **superspec 完成后**，回到外层：
   - 外层收集本轮产出
   - 更新 state.md
   - 追加 learnings.md
   - 检查上下文预算
   - 决定下一个子目标

关键点：superspec 负责"怎么做好这个具体任务"，外层负责"做哪个任务、进度如何、学到了什么"。

在本项目里，推荐的职责分工是：

- `context-budget-explore`：
  - 管毕业设计阶段推进
  - 管记录体系
  - 管跨对话续接
  - 管任务状态回写
- `superspec`：
  - 管“这一轮具体功能怎么落地”
  - 管 proposal / design / tasks
  - 管 apply / verify / review

如果用户是在问流程而不是问实现细节，直接按 `references/agent-desktop-pet-workflows.md` 输出具体步骤，不要只停留在抽象原则。

## 与 session-handoff 的集成

触发条件（满足任一）：

- 对话明显过长，回复开始变慢
- 用户说"先到这"、"下次继续"、"保存进度"
- 一个大阶段完成，适合切换对话
- 外层主动判断需要切换

触发时：

1. 先创建本 skill 的 checkpoint
2. 更新所有持久化文件
3. 调用 session-handoff 生成标准交接文档，写入当前 explore 目录下的 `handoffs/`
4. 告知用户：交接文档位置 + 下次如何恢复

## 持久化文件模板

### `workflow.md`
```markdown
# 探索工作流

## 任务目标
...

## 范围边界
- 范围内：...
- 范围外：...

## 成功标准
- ...

## 阶段规划
1. ...
2. ...
3. ...

## 当前阶段
阶段 X：...

## 退出条件
- ...
```

### `state.md`
```markdown
# 当前状态

## 当前阶段
...

## 已确认的事实
- ...

## 工作假设
- ...

## 待解决的问题
- ...

## 下一步
- ...

## 最小活跃上下文摘要
（用最少的文字描述当前需要记住的核心信息）
...
```

### `decision-log.md`
```markdown
# 决策日志

## [日期] 决策：...
- **背景**：...
- **选择**：...
- **原因**：...
- **放弃的方案**：...
- **影响**：...
```

### `learnings.md`
```markdown
# 经验沉淀

## [日期] 第 N 轮迭代

### 有效的做法
- ...

### 无效的做法
- ...

### 可复用的策略
- ...

### 要避免的坑
- ...
```

### `handoff.md`
```markdown
# 交接文档

## 当前目标
...

## 当前进度
...

## 关键文件/产物
- ...

## 已做的决策（摘要）
- ...

## 立即要做的下一步
- ...

## 恢复指引
1. 读取本文件了解上下文
2. 读取 state.md 了解详细状态
3. 读取 learnings.md 了解历史经验
4. 从"立即要做的下一步"继续
```

### `handoffs/`
```text
.codex/explore/<topic>/handoffs/
  ├─ 2026-03-26-103000-round-1.md
  ├─ 2026-03-26-154500-round-2.md
  └─ 2026-03-27-091200-round-3.md
```

说明：

- `handoff.md` 是当前 explore 的精简摘要入口
- `handoffs/` 用来存放该 explore 的多次标准交接文档
- 一个 explore 可以有很多次交接，按时间戳持续追加，不混到别的 explore 里

## 输出规范

日常输出保持精简，包含：

- 当前阶段
- 活跃任务
- 是否需要 checkpoint
- 哪个持久化文件需要更新
- 下一步建议

不要在没有必要时输出大段总结。只在 checkpoint 时输出完整的阶段性报告。

## 验证标准

本 skill 运作良好的标志：

- 对话不再重复解释旧的结论
- 从 handoff.md 或 state.md 可以快速恢复进度
- 决策可以从 decision-log.md 快速查到，不需要翻聊天记录
- 下一步行动始终明确
- 用户可以安全地暂停，下次以最小成本继续
- 每次迭代的经验都有记录，不会重复犯错

## 示例场景

### 场景一：质检工作流迭代优化

用户说：
> 我们要做一个质检闭环，会一直迭代优化，顺便把经验沉淀下来。

响应：
1. 创建 TaskList：[定义质检规则] → [实现检测逻辑] → [测试验证] → [优化调整] → [沉淀经验]
2. 初始化 workflow.md、state.md、learnings.md
3. 第一个任务用 superspec 走流程
4. 每完成一轮：更新 state + 追加 learnings
5. 上下文变长时：checkpoint → 必要时 session-handoff

### 场景二：跨对话继续

用户说：
> 继续上次的质检优化工作。

响应：
1. 读取 `.codex/explore/handoff.md`
2. 读取 `state.md` 恢复详细状态
3. 读取 `learnings.md` 回顾历史经验
4. 恢复 TaskList
5. 从 handoff 中的"下一步"继续

## 注意事项

- 持久化文件优先更新已有文件，不要不断创建新文件
- checkpoint 要精简，不是完整的会议纪要
- learnings.md 记录的是可复用的经验，不是事件日志
- 如果某个经验已经稳定且被反复验证，考虑写入项目的 CLAUDE.md 或提取为独立 skill
- 所有文档使用中文
- 在本项目中，优先维持“全局 roadmap + 专项 explore + OpenSpec 真相源”的三层结构
- 在本项目中，如果用户提到“毕设”“阶段推进”“记录过程”“继续桌宠”，默认应触发本 skill
