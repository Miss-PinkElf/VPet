# Handoff: VPet Fork Migration And Refactor Guide

## Session Metadata
- Created: 2026-03-26 15:00:24
- Project: `E:\Learn\Vs\Code\agent-desktop-pet.worktrees\agent-desktop-pet-expore`
- Branch: `shuowang/dev-vpet`
- Purpose: 给后续在 fork 的 `VPet` 仓库里直接开工的自己或新 agent 使用

## Current State Summary

当前方向已经明确：主仓库仍然保留 `Electron + React + Python` 的探索结论，但单独开一个 `VPet` fork/分支，专门验证“保留 VPet 的桌宠窗口行为和帧动画表现层，再通过外部事件桥接入自己的 Python 后端”是否可行。这里的核心不是把 `VPet` 全量重构成新平台，而是做有限拆解：先打通“外部事件 -> VPet 动作状态”的最小链路，再决定是否继续向更深层逻辑动手。

## Goal In Forked VPet Repo

fork 后的新仓库，不是为了延续当前 `Electron` 前端，而是为了：

1. 保留 `VPet` 的强桌宠感基础
2. 复用 `VPet` 的窗口行为与帧动画体系
3. 把外部 Python 后端接进来
4. 逐步把“行为决策”和“表现执行”分层

一句话目标：

> 在 fork 的 `VPet` 仓库里做一个“高桌宠感身体层 + 外部 Python 大脑”的重构验证分支。

## Codebase Understanding

### Architecture Overview

当前要迁移到 fork 仓库里的整体结构可以理解成三层：

1. `VPet` 身体层
   - 负责窗口行为、帧动画、桌宠状态切换、拖拽和贴边等强桌宠感能力
2. `backend-agent/` 外部 Python 大脑
   - 负责聊天、记忆、事件总线、行为策略
3. 事件桥
   - 负责把 Python 侧的高层行为事件转成 `VPet` 能执行的动作状态

第一阶段只验证这三层能否打通，不做更多抽象。

### Why Fork VPet

本轮探索已经确认：

- `VPet` 的优势不只是渲染，而是完整的桌宠状态感
- 强桌宠感来自状态机、窗口行为、动画资源矩阵、交互节奏
- `Live2D` 更适合角色感，不一定最适合强桌宠动作感
- `WindowPet` 和 `clawd-on-desk` 值得参考，但 `VPet` 依然是最接近目标上限的现成样板

### What To Keep From VPet

优先保留并利用的结构：

- `VPet-Simulator.Windows` 一类桌面壳层/窗口行为
- `Graph / PNGAnimation / Picture` 一类表现层
- 现成拖拽、贴边、提起、趴下、状态切换等桌宠感相关代码

先不要深挖和大改的结构：

- `MainLogic / GameCore` 深层内部行为逻辑
- 存档、插件、外围产品化能力
- 原项目资源分发逻辑

### Forked Repo Critical Principle

不要把目标设成：

- “全面重构 VPet”
- “一次性把内部逻辑全部解耦”
- “先删到很干净再开始”

更现实的顺序是：

1. 保住能跑的桌宠壳层
2. 给它增加外部事件入口
3. 让 Python 发送高层行为事件
4. 只在必要时局部隔离内部逻辑

### Critical Files To Bring From Current Repo

| Path | Purpose | Why It Matters In Forked Repo |
|------|---------|-------------------------------|
| `backend/` | Python 后端代码 | 作为 `VPet` 的外部大脑原型 |
| `zzz-doc/桌宠技术路线探索总结.md` | 技术路线判断 | 说明为什么现在选择 fork `VPet` |
| `zzz-doc/back.md` | 后端设计记录 | 衔接后端结构和后续接口 |
| `zzz-doc/记忆相关.md` | 记忆系统设计记录 | 保证 fork 后不丢掉陪伴型目标 |
| `zzz-doc/zzz-prompt-debug/plan/桌宠项目详细PRD.md` | 产品需求 | fork 后仍需遵守的总目标 |
| `openspec/changes/desktop-pet-companion-roadmap/` | 路线 proposal/design/tasks | 为 fork 仓库保留路线说明和任务背景 |
| `.codex/AGENTS.md` | Codex 仓库级指令 | 保持新仓库里的 agent 行为一致 |
| `.claude/CLAUDE.md` | Claude 仓库级指令 | 保持新仓库里的 agent 行为一致 |
| `.gitignore` | 忽略规则 | 避免把本地缓存和生成物带进新仓库 |

## Work Completed In This Repo

### Tasks Finished

- [x] 补完 `zzz-doc/桌宠技术路线探索总结.md`，加入 `clawd-on-desk` 判断
- [x] 补完 `zzz-doc/桌宠技术路线探索总结.md`，加入“深度修改 `VPet` 的可行性补充”
- [x] 已将当前工作树切到 `shuowang/dev-vpet`
- [x] 已明确后续方向：fork `VPet` 仓库，开独立重构验证分支

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `zzz-doc/桌宠技术路线探索总结.md` | 新增 `clawd-on-desk` 分析、新增 `14.5 深度修改 VPet 的可行性补充`、更新最终判断 | 让技术探索文档能够直接支撑 VPet fork 重构决策 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 不直接迁移主仓库到 `VPet` | 直接迁移、继续 Electron、另开 fork 分支 | 主仓库节奏不能被高风险重构拖垮，但 `VPet` 值得单独验证 |
| 在 fork 的 `VPet` 仓库里做有限拆解 | 全量重构、只读参考、局部桥接 | 目标是尽快验证“外部事件 -> VPet 动作状态”是否可行 |
| 迁移当前仓库的一部分文档、后端和配置到 fork 仓库 | 什么都不带、整仓搬运 | 需要保留需求、后端与 agent 工作流，但不能把当前仓库杂项全带过去 |

## What To Copy Into Forked VPet Repo

### Must Copy

这些内容直接支撑 fork 仓库开工：

- `backend/`
  - 理由：这是后续外部 Python 大脑的核心
- `zzz-doc/桌宠技术路线探索总结.md`
  - 理由：解释为什么要 fork `VPet`、为什么不是直接换栈
- `zzz-doc/back.md`
  - 理由：后端相关设计和当前思路
- `zzz-doc/记忆相关.md`
  - 理由：记忆系统目标和约束
- `zzz-doc/zzz-prompt-debug/plan/桌宠项目详细PRD.md`
  - 理由：产品目标和需求边界
- `openspec/changes/desktop-pet-companion-roadmap/`
  - 理由：已有 roadmap、design、tasks
- `.codex/AGENTS.md`
  - 理由：Codex 在新仓库里继续工作时需要的指令上下文
- `.claude/CLAUDE.md`
  - 理由：Claude 系工作流在新仓库里继续使用时需要的上下文
- `.gitignore`
  - 理由：至少要人工合并规则，避免把缓存、构建物和本地配置提交进 fork 仓库

### Recommended Copy

这些不是开工必需，但强烈建议带过去：

- `前端需求.md`
- `zzz-doc/桌宠项目交互控制设计稿.md`
- `zzz-doc/桌宠毕设过程记录指南.md`
- `.codex/explore/desktop-pet-graduation-roadmap/`
- `.claude/explore/desktop-pet-graduation-roadmap/`

这些文件的价值在于保留“前因后果”，让 fork 后的新仓库不只是代码仓库，也能承接毕设叙事、路线记录和 agent 工作流。

### Copy With Review First

这些可以带，但不要无脑整目录复制：

- `.claude/settings.local.json`
  - 本地配置，可能机器相关，先检查再决定是否保留
- `.codex/skills/`、`.claude/skills/`
  - 如果你希望新仓库继续完全沿用当前 agent 工作流，可以复制；如果想保持 fork 仓库轻量化，则只复制必要指令文件
- 旧 handoff、旧 explore 记录
  - 有保留价值，但不一定都要进入新仓库主线

### Do Not Copy Directly

这些内容不要直接搬到 fork 仓库里：

- `frontend/`
  - 原因：这是当前 `Electron + React + Live2D` 路线，不是 `VPet` fork 的前端主线
- `node_modules/`
- `.electron-cache/`
- `.pnpm-store/`
- `electron-v40.4.1-win32-x64.zip`
- 与当前实验环境强绑定的临时文件、缓存、打包产物

## Suggested Structure Inside Forked VPet Repo

建议不要把当前仓库的内容直接散落到 `VPet` 根目录。更稳的方式是整理成下面这种结构：

```text
docs/
  agent-desktop-pet/
    requirements/
    research/
    backend/
    migration/
backend-agent/
.codex/
.claude/
```

建议落位：

- `backend/` 复制后改名为 `backend-agent/`
  - 避免和 `VPet` 自己的工程结构混淆
- `zzz-doc/桌宠技术路线探索总结.md`
  - 放到 `docs/agent-desktop-pet/research/`
- `zzz-doc/back.md`
  - 放到 `docs/agent-desktop-pet/backend/`
- `zzz-doc/记忆相关.md`
  - 放到 `docs/agent-desktop-pet/backend/`
- `桌宠项目详细PRD.md`
  - 放到 `docs/agent-desktop-pet/requirements/`
- 这份 handoff
  - 放到 `docs/agent-desktop-pet/migration/` 或 `.claude/handoffs/`

## First Actions In Forked Repo

### Step 1: Fork And Branch

在你 fork 的 `VPet` 仓库里：

1. fork upstream `VPet`
2. clone 你的 fork
3. 新建分支，建议直接叫：
   - `shuowang/dev-vpet`
   - 或 `shuowang/dev-vpet-refactor`

### Step 2: Do Minimal Cleanup First

先做“小删减”，不是大清理：

- 删除明显与当前验证目标无关的个人临时文件或本地产物
- 不要一开始删核心项目结构
- 不要先删除 `Windows` 壳层、`Core`、`Graph` 相关代码
- 不要先碰资源大搬家

### Step 3: Copy In Migration Materials

优先复制：

1. `backend/` -> `backend-agent/`
2. 需求文档和技术探索文档
3. `.codex/AGENTS.md`
4. `.claude/CLAUDE.md`
5. 手工合并 `.gitignore`

### Step 4: Add A Migration Readme

在 fork 仓库里新增一个顶层说明文件，至少写清：

- 这个 fork 的目标不是原样维护 `VPet`
- 这个 fork 是做“VPet 身体层 + Python 大脑”重构验证
- 当前阶段只验证外部事件桥，不做全面重构

### Step 5: Implement The Smallest Technical POC

最小 POC 只验证这三件事：

1. fork 后的 `VPet` 原工程能稳定跑起来
2. 能新增一个外部事件入口，例如 `HTTP / WebSocket / Named Pipe`
3. 外部事件能触发几个动作状态切换，例如：
   - `idle`
   - `thinking`
   - `remind`
   - `dragged`

只要这三件事通了，这条路线就成立。

## Immediate Next Steps

1. fork `VPet` 仓库并在 fork 内新建 `shuowang/dev-vpet` 或 `shuowang/dev-vpet-refactor`
2. 将本仓库中的后端、需求文档、技术探索文档和最小配置迁移到 fork 仓库
3. 在 fork 仓库中先做最小 POC：新增外部事件入口并打通一个动作状态切换

## Blockers/Open Questions

- [ ] `VPet` fork 后准备保留哪些上游目录，哪些要删减，需要先看一遍 fork 后的实际结构
- [ ] `backend-agent/` 放在 fork 仓库根目录还是单独 `integration/` 目录，当前还没定死
- [ ] `.claude/settings.local.json` 是否要保留，要根据你 fork 后的实际机器环境再决定

## Important Context

这个交接文档的目的不是继续当前 `Electron` 主线，而是让你在 fork 的 `VPet` 仓库里直接开始工作，并且知道：

- 为什么现在要 fork `VPet`
- 为什么不是全面重构
- 哪些当前仓库里的东西要带过去
- 哪些不要带过去
- 在 fork 仓库里第一步该做什么

最重要的设计边界是：

- `VPet` fork 仓库负责“高桌宠感身体层验证”
- 当前仓库已经有的 `Python` 后端负责“大脑”
- 两者之间通过外部事件桥连接

不要把 fork 仓库的第一阶段目标定得过大。第一阶段不是“做完完整 AI 桌宠”，而是：

> 证明外部 Python 可以驱动 `VPet` 的动作和状态。

## Assumptions Made

- 你会先 fork upstream `VPet`，而不是在当前仓库里继续硬拆
- 你希望新仓库还能继续用 agent 协作，所以需要带走一部分 `.codex` / `.claude` 配置
- 你要保留当前后端思路，因此 `backend/` 要跟着迁过去
- 你当前最关注的是桌宠感，而不是先统一技术栈

## Potential Gotchas

- 不要把当前仓库的 `frontend/` 带去 fork 仓库主线，否则目标会重新变混
- 不要整包复制 `.codex/skills`、`.claude/skills` 后又不检查体积和相关性
- `.gitignore` 最好手工合并，不要直接覆盖上游仓库的忽略规则
- `VPet` 代码许可和资源许可要分开看，发布时尤其小心
- 第一阶段不要试图重写 `GameCore`

## Environment State

### Tools/Services Used

- Git worktree
- Codex / Claude agent workflow
- Python backend scaffold already exists in current repo

### Active Processes

- No required long-running process for this handoff

### Environment Variables

- 暂无必须记录的环境变量名称

## Related Resources

- `zzz-doc/桌宠技术路线探索总结.md`
- `zzz-doc/back.md`
- `zzz-doc/记忆相关.md`
- `zzz-doc/zzz-prompt-debug/plan/桌宠项目详细PRD.md`
- `openspec/changes/desktop-pet-companion-roadmap/proposal.md`
- `openspec/changes/desktop-pet-companion-roadmap/design.md`
- `openspec/changes/desktop-pet-companion-roadmap/tasks.md`
- `backend/`
- `.codex/AGENTS.md`
- `.claude/CLAUDE.md`
