# 工作区与模板说明

## 默认工作区

本 skill 默认在仓库根目录创建：

```txt
.explore/
```

每个任务对应一个独立 mission：

```txt
.explore/<mission-slug>/
```

推荐的 `mission-slug`：

```txt
<领域>-<任务>-<短标识>
```

例如：

- `skill-context-budget-explore`
- `quality-loop-optimizer`
- `antd-form-refactor`

## Mission 目录结构

```txt
.explore/<mission-slug>/
├── workflow.md
├── state.md
├── decision-log.md
├── learnings.md
├── checkpoints.md
├── checkpoints-archive.md
├── session-tasks.md
├── spec/
│   ├── proposal.md
│   ├── design.md
│   └── tasks.md
└── handoffs/
    ├── index.md
    ├── YYYY-MM-DD-001-init.md
    ├── YYYY-MM-DD-002-checkpoint.md
    └── YYYY-MM-DD-003-resume-ready.md
```

## 初始化规则

开始一个新 mission 时：

1. 创建 mission 目录
2. 创建 `spec/` 与 `handoffs/` 子目录
3. 初始化以下文件：
   - `workflow.md`
   - `state.md`
   - `decision-log.md`
   - `learnings.md`
   - `checkpoints.md`
   - `checkpoints-archive.md`
   - `session-tasks.md`
   - `handoffs/index.md`
4. 如果用户是在续接旧任务，先读取已有文件，除非必要不要覆盖

## 基础文件职责

### `workflow.md`

记录：

- 任务目标
- 范围内 / 范围外
- 成功标准
- 阶段规划
- 当前阶段
- 退出条件

### `state.md`

记录：

- 当前阶段
- 已确认事实
- 工作假设
- 待解决问题
- 下一步
- 最新 handoff
- 最小活跃上下文摘要

### `decision-log.md`

记录会影响后续判断的决策，分成两块：

- 历史决策摘要：只放早期决策的一行摘要
- 完整记录：保留最近 5 条完整决策

### `learnings.md`

记录可复用经验：

- 有效做法
- 无效做法
- 降低成本或延迟的技巧
- 导致上下文膨胀的行为
- 可复用策略
- 要避免的坑

### `checkpoints.md`

按时间顺序追加 checkpoint，但只保留最近 3 个完整 checkpoint。

每条 checkpoint 至少包含：

- 当前阶段
- 本轮完成内容
- 本轮决策与原因
- 本轮沉淀经验
- 待解决问题
- 下一步
- 可以从活跃上下文移除的内容

更早的 checkpoint 滚动归档到 `checkpoints-archive.md`。

### `checkpoints-archive.md`

保存由滚动窗口归档的旧 checkpoint。

默认不主动读取，只在需要回溯历史时按需查看。

### `session-tasks.md`

用于非 Claude Code 环境下替代 TaskList。

建议格式：

```md
# 会话任务

- [ ] 任务 1
- [ ] 任务 2
- [x] 已完成任务
```

### `spec/`

内置 spark-workflow 产物目录：

- `proposal.md`
- `design.md`
- `tasks.md`

### `handoffs/index.md`

记录当前 mission 下的 handoff 索引：

- 最新 handoff
- 每次 handoff 的编号与标题
- 所属阶段
- 是否已 superseded
- 恢复时建议优先读取哪一份

## 建议初始化模板

### `workflow.md`

```md
# 任务工作流

## 任务目标
-

## 范围边界
- 范围内：
- 范围外：

## 成功标准
-

## 阶段规划
1.
2.
3.

## 当前阶段
-

## 退出条件
-
```

### `state.md`

```md
# 当前状态

## 当前阶段
-

## 已确认的事实
-

## 工作假设
-

## 待解决的问题
-

## 下一步
-

## 最新 handoff
- 无

## 最小活跃上下文摘要
-
```

### `decision-log.md`

```md
# 决策日志

## 历史决策摘要

（当完整记录超过 5 条时，旧决策压缩到这里）

## 完整记录
```

### `learnings.md`

```md
# 经验沉淀
```

### `checkpoints.md`

```md
# Checkpoints
```

### `checkpoints-archive.md`

```md
# Checkpoints 归档

（由滚动窗口自动归档的旧 checkpoint，按需查看，恢复时不主动读取）
```

### `handoffs/index.md`

```md
# Handoff 索引

## 最新 handoff
- 无

## 历史记录
- 暂无
```

## 更新策略

- 优先更新已有文件，不要无意义重复创建
- 每轮推进后至少更新 `state.md`
- 做了关键选择后更新 `decision-log.md`
- 形成可复用经验后更新 `learnings.md`
- 阶段切换或准备暂停时更新 `checkpoints.md` 或 `handoffs/`
- `checkpoints.md` 只保留最近 3 个完整 checkpoint，旧内容滚到 `checkpoints-archive.md`
- `decision-log.md` 只保留最近 5 条完整决策，更早内容压缩到摘要区

## 恢复策略

恢复任务时按这个顺序读取：

1. `state.md`
2. 最新 handoff（只读最新 1 份，不默认读多份）
3. `workflow.md`（仅在 `state.md` 信息不足时）
4. `learnings.md`（按需）
5. `spec/` 中相关 artifact（按需）

不主动读取的文件：

- `handoffs/index.md`（只在最新 handoff 信息不足时读取）
- `checkpoints-archive.md`（只在需要回溯历史时读取）
- `decision-log.md` 的历史摘要区

如果文件内容与当前仓库状态冲突，以当前代码和仓库状态为准，再回写修正记录。
