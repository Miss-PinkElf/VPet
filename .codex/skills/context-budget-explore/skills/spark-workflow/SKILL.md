---
name: spark-workflow
description: 当任务已经进入明确推进阶段，需要在当前 mission 工作区内完成对齐、提案、实施、验证与归档时使用。它是 context-budget-explore 的内层执行引擎，不是顶层 orchestrator。适用于需求已较清晰的探索收敛、proposal/design/tasks 产出、按任务实施、审查与验证收尾。
---

# SPARK-workflow（context-budget-explore 内置版）

OpenSpec 管生命周期，Superpowers 管质量门禁。

本 skill 是 **context-budget-explore 的内层执行引擎**。它不负责全局 workflow、checkpoint、handoff 或长期经验沉淀；这些由外层主 skill 负责。

```txt
Classify -> Align -> Propose -> Apply -> Review/Verify -> Archive
```

## 与外层主 skill 的关系

- 外层 `context-budget-explore` 负责 mission、状态、决策、经验、checkpoint、handoff
- 本 skill 负责当前子任务的执行路径与质量门禁
- 本 skill 产物默认写入当前 mission 的 `spec/` 目录
- 本 skill 每完成一个阶段后，应回到外层更新：
  - `state.md`
  - `decision-log.md`
  - `learnings.md`
  - `checkpoints.md`（如适用）

不要把本 skill 当成顶层 orchestrator 单独长期运行。

## 默认产物位置

如果外层已建立 mission 工作区，则默认使用：

```txt
.explore/<mission-slug>/spec/
```

其中：

- `proposal.md`
- `design.md`
- `tasks.md`

都是当前子任务的真相源。

如果 mission 尚未建立，先回到外层主 skill 初始化工作区，再继续。

## 适用范围与分流

| 请求形态 | 路由 |
| --- | --- |
| 纯讨论、方案探索、需求澄清 | 读取 [skills/openspec-explore/SKILL.md](skills/openspec-explore/SKILL.md) |
| 纯 bug 修复、根因未知、已有明显故障现象 | 读取 [skills/superpowers-systematic-debugging/SKILL.md](skills/superpowers-systematic-debugging/SKILL.md) |
| 现有页面或组件上的小型明确改动 | 走轻量路径：Classify -> Mini Align -> Propose -> Apply -> Verify |
| 常规功能交付、页面重构、组件改造、体验优化 | 走标准路径：Classify -> Align -> Propose -> Apply -> Review/Verify -> Archive |
| 全新大型模块且涉及重架构设计 | 回到外层，由外层决定是否切换到更重的规划模式 |

## 轻量路径信号

多数条件成立时才使用轻量路径：

- 目标状态已经足够明确
- 改动局限于已有页面、组件、交互或样式
- 不需要新增完整业务流程
- 不需要大范围模块、接口契约或状态架构设计

一旦出现需求歧义、多页面影响，或存在多种合理实现方案，就立刻退出轻量路径。

## 核心规则

### 1. OpenSpec 负责阶段推进

OpenSpec 负责回答：

- 当前工作处于哪个阶段
- 当前阶段需要什么 artifact
- 满足什么条件才能进入下一阶段
- 新信息推翻当前结论时，应回退到哪里

### 2. Superpowers 只在门禁点介入

| 门禁点 | 读取 | 作用 |
| --- | --- | --- |
| 进入 proposal 之前 | [skills/superpowers-brainstorming/SKILL.md](skills/superpowers-brainstorming/SKILL.md) | 对齐需求、约束和方案选项 |
| Apply 中出现失败或异常 | [skills/superpowers-systematic-debugging/SKILL.md](skills/superpowers-systematic-debugging/SKILL.md) | 先找根因，再修复 |
| Apply 中出现纯逻辑场景 | [skills/superpowers-test-driven-development/SKILL.md](skills/superpowers-test-driven-development/SKILL.md) | 提升纯变换逻辑的正确性 |
| 实现之后 | [skills/superpowers-requesting-code-review/SKILL.md](skills/superpowers-requesting-code-review/SKILL.md) 与 [skills/superpowers-receiving-code-review/SKILL.md](skills/superpowers-receiving-code-review/SKILL.md) | 审查后再宣称完成 |
| 收尾之前 | [skills/superpowers-verification-before-completion/SKILL.md](skills/superpowers-verification-before-completion/SKILL.md) | 用证据而不是信心判断完成 |

### 3. Artifact 真相源

从 Step 2 开始，以下文件是唯一真相源：

- `proposal.md`
- `design.md`
- `tasks.md`

一旦 artifact 存在，不要继续以聊天历史为准。

## 工作流

## Step 0：Classify

判断当前子任务是：

1. 讨论 / 探索
2. bug 调试
3. 计划性实施
4. 收尾与验证

然后宣布选定路径。

## Step 1：Align

目标：在 proposal artifact 出现之前，对齐意图、约束、边界和方案方向。

无论任务大小都必须做 Align，差别只在深度。

### 标准 Align

用于需求模糊或影响面较大的工作。

必做动作：

1. 扫描相关代码、文档和已有模式
2. 提炼未知项与风险
3. 一次只问一个问题
4. 给出 2-3 个方案、取舍和推荐
5. 总结建议方向，并等待用户明确确认

读取：

- [references/brainstorming-guide.md](references/brainstorming-guide.md)
- [skills/superpowers-brainstorming/SKILL.md](skills/superpowers-brainstorming/SKILL.md)

### Mini Align

只用于小型且清晰的改动。

最低要求：

1. 扫描代码和用户提供的文档
2. 提炼关键确认点
3. 至少进行一次交互式确认
4. 总结推荐方案
5. 在进入 proposal 之前等待确认

即使已有设计说明，也不能跳过确认。

## Step 2：Propose

把已对齐的结论转成可执行 artifact。

动作：

1. 读取 [skills/openspec-propose/SKILL.md](skills/openspec-propose/SKILL.md)
2. 确认当前 mission 与 `spec/` 位置
3. 产出 `proposal.md`、`design.md`、`tasks.md`
4. 如果用户提供规格说明，使用 [references/spec-to-artifact-mapping.md](references/spec-to-artifact-mapping.md) 做映射
5. 将任务拆成可独立实现、可独立验证的单元

模板：

- [assets/templates/proposal-template.md](assets/templates/proposal-template.md)
- [assets/templates/design-template.md](assets/templates/design-template.md)
- [assets/templates/tasks-template.md](assets/templates/tasks-template.md)

满足以下条件之前，不得进入 Step 3：

- proposal 覆盖范围与边界场景
- design 能解释结构、接口和数据流
- tasks 足够原子，可独立执行和验证
- 用户已批准 artifact，或已明确授权直接实现

## Step 3：Apply

按 `tasks.md` 实现，而不是凭记忆实现。

动作：

1. 读取 [skills/openspec-apply-change/SKILL.md](skills/openspec-apply-change/SKILL.md)
2. 选择执行模式
3. 严格按 `tasks.md` 逐项推进
4. 开始任务前标记 `in_progress`
5. 完成自检后，只有满足验收标准才能标记完成
6. 如果实现中暴露设计问题，停止并回退到 Step 2

### 执行模式

| 模式 | 适用场景 | 读取 |
| --- | --- | --- |
| 顺序模式 | 任务少或耦合强 | 按 `tasks.md` 顺序执行 |
| 并行模式 | 任务独立且低耦合 | [skills/superpowers-dispatching-parallel-agents/SKILL.md](skills/superpowers-dispatching-parallel-agents/SKILL.md) |
| 子代理模式 | 任务多、上下文大，或实现与审查分离更有利 | [skills/superpowers-subagent-driven-development/SKILL.md](skills/superpowers-subagent-driven-development/SKILL.md) |

默认顺序模式，除非低耦合非常明确。

## Step 4：Review / Verify / Archive

实现完成不等于工作完成。

### Review

1. 读取 [skills/superpowers-requesting-code-review/SKILL.md](skills/superpowers-requesting-code-review/SKILL.md)
2. 在里程碑节点或所有实现任务完成后发起审查
3. 在处理反馈前，读取 [skills/superpowers-receiving-code-review/SKILL.md](skills/superpowers-receiving-code-review/SKILL.md)
4. 如果反馈意味着需求或设计变化，回退到 Step 2

### Verify

1. 重新读取 `proposal.md`
2. 重新读取 `tasks.md`
3. 运行验证命令
4. 收集明确正确性证据

读取 [skills/superpowers-verification-before-completion/SKILL.md](skills/superpowers-verification-before-completion/SKILL.md)

### Archive

1. 读取 [skills/openspec-archive-change/SKILL.md](skills/openspec-archive-change/SKILL.md)
2. 归档已完成变更，或记录等价关闭状态
3. 回到外层主 skill，更新 `state.md`、`decision-log.md`、`learnings.md` 与必要 checkpoint

## 回退矩阵

| 当前阶段 | 触发情况 | 回退到 |
| --- | --- | --- |
| Align | 用户补充大量新约束 | 继续 Align |
| Propose | 用户推翻已同意方向 | Align |
| Apply | 发现设计缺口或任务拆分错误 | Propose |
| Apply | 三次修复失败，说明计划可能有问题 | 先 Debugging，通常再回 Propose |
| Review | 反馈意味着需求或设计变化 | Propose |
| Verify | 验证失败但设计仍成立 | Apply |
| Verify | 验证暴露设计缺陷 | Propose |

回退是校正，不是失败。

## 完成定义

只有全部满足时，才能声称当前子任务完成：

- Align 阶段已经完成交互式确认
- 方案方向或 artifact 已获批准
- `proposal.md` 覆盖范围和边界场景
- `design.md` 解释结构、接口和数据流
- `tasks.md` 已拆成原子任务
- 所有任务已完成
- review 问题已解决或已明确处置
- 验证命令已运行且通过
- 相关产出已同步回外层工作区记录

## 反模式

避免以下行为：

- 把本 skill 当外层 workflow 管理器使用
- 因为任务看起来简单就跳过 Align
- 一次问很多个问题
- 方案未确认就开始写 tasks
- artifact 已存在后继续以聊天历史为准
- 出错时靠猜修
- 已知设计缺陷还继续推进
- 没有证据就宣称完成

## 读取地图

```txt
纯讨论 -> skills/openspec-explore/SKILL.md
纯 bug 修复 -> skills/superpowers-systematic-debugging/SKILL.md
计划性改动 ->
  Step 1 Align:
    references/brainstorming-guide.md
    skills/superpowers-brainstorming/SKILL.md
  Step 2 Propose:
    skills/openspec-propose/SKILL.md
    assets/templates/*.md
    references/spec-to-artifact-mapping.md
  Step 3 Apply:
    skills/openspec-apply-change/SKILL.md
    references/quality-gates.md
    skills/superpowers-systematic-debugging/SKILL.md
    skills/superpowers-test-driven-development/SKILL.md
    skills/superpowers-dispatching-parallel-agents/SKILL.md
    skills/superpowers-subagent-driven-development/SKILL.md
  Step 4 Close:
    skills/superpowers-requesting-code-review/SKILL.md
    skills/superpowers-receiving-code-review/SKILL.md
    skills/superpowers-verification-before-completion/SKILL.md
    skills/openspec-archive-change/SKILL.md
```
