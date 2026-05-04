# 原生桌宠交互设计文档 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers-subagent-driven-development (recommended) or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 VPet 原生桌宠交互逻辑（Native Desktop Pet Interaction Logic）整理成一份面向项目设计借鉴的详细中文文档。

**Architecture:** 本轮只新增文档，不修改业务代码。文档以已有源码探索结论为依据，分成“原生机制解释”“好桌宠设计原则”“可迁移到当前项目的架构模型”“后续路线建议”四层。

**Tech Stack:** Markdown、devflow mission 文档。

---

## 文件结构

- Create: `.devflow/desktop-pet-native-interaction-explore/learnings/desktop-pet-interaction-design-guide.md`
  - 职责：面向后续设计与实现的详细设计说明文档。
- Modify: `.devflow/desktop-pet-native-interaction-explore/state.md`
  - 职责：记录新增设计文档入口。
- Modify: `.devflow/desktop-pet-native-interaction-explore/checkpoints.md`
  - 职责：记录本轮文档沉淀 checkpoint。

## 任务

### Task 1: 写设计说明文档

**Files:**
- Create: `.devflow/desktop-pet-native-interaction-explore/learnings/desktop-pet-interaction-design-guide.md`

- [ ] **Step 1: 写入文档主体**

写入以下内容结构：

```markdown
# 桌宠交互设计借鉴文档

## 文档目的
...
```

文档必须覆盖：

- VPet 原生设计的核心抽象
- 自动行为设计
- 动作系统设计
- 屏幕移动与贴边设计
- 用户交互设计
- 一个好的桌宠应具备的能力清单
- 当前项目可借鉴的架构层次
- 不建议直接照搬的部分
- 后续路线建议

- [ ] **Step 2: 自查术语**

确认首次出现的专业术语使用中文 + 英文双语表达，例如：

- 分层状态机（Layered State Machine）
- 图形类型（GraphType）
- 动画阶段（AnimatType）
- 触摸区域（TouchArea）
- 行为调用（behavior.invoke）

### Task 2: 更新 mission 状态

**Files:**
- Modify: `.devflow/desktop-pet-native-interaction-explore/state.md`
- Modify: `.devflow/desktop-pet-native-interaction-explore/checkpoints.md`

- [ ] **Step 1: 更新 state**

在 `state.md` 的最新沉淀中加入：

```markdown
- `learnings/desktop-pet-interaction-design-guide.md`
```

- [ ] **Step 2: 写 checkpoint**

在 `checkpoints.md` 追加本轮 checkpoint，记录设计文档已落盘。

## 验证

- [ ] 使用 `Get-Content -Raw` 读取新增文档，确认内容完整。
- [ ] 使用 `git status --short` 确认只有预期文档变更和既有未跟踪文件。

