# Checkpoints

> [已归档] 2026-03-27 - Mission Migration
> [已归档] 2026-03-27 - Window Move + State Loop
> [已归档] 2026-03-27 - Combo Validation + State Expansion
> [已归档] 2026-03-27 - Sequence / Scenario Entry
> [已归档] 2026-03-27 - Context Save
> [已归档] 2026-03-27 - Standard 18787 Startup Fix + Long Sequence
> [已归档] 2026-03-28 - Sleep Handoff
> [已归档] 2026-03-28 - Timeline Observability + Legacy UI Demotion
> [已归档] 2026-03-30 - Display Control Surface Analysis
> [已归档] 2026-03-28 - Quick Test JSON Catalog Page
> [已归档] 2026-03-28 - Quick Test File-Backed Catalog
> [已归档] 2026-03-28 - Current Phase Test Catalog
> [已归档] 2026-03-28 - Quick Test Result Writeback
> [已归档] 2026-03-28 - Move Instability Root Cause
> [已归档] 2026-03-28 - Sequence Delay Relaxation
> [已归档] 2026-03-28 - Smart Move Style
> [已归档] 2026-03-28 - Sequence Wait-For Gating
> [已归档] 2026-03-29 - Sleep Handoff After Sequence Gating
> [已归档] 2026-03-29 - Real Retest After Event-Applied + Move Tolerance Fix
> [已归档] 2026-03-29 - Event Correlation Fields + Longer Story Sequence
> [已归档] 2026-03-29 - Sleep Handoff After Event Correlation
> [已归档] 2026-03-31 - Focus Quick Test For Story Sequence
> [已归档] 2026-03-31 - Story Sequence Result Triage
> [已归档] 2026-03-31 - Motion Complete Stabilization
> [已归档] 2026-03-31 - Motion Recovered Gate
> [已归档] 2026-03-31 - Tail-Step Relaxation For Story Sequence
> [已归档] 2026-03-31 - Smart Move Easing Pass
> [已归档] 2026-03-31 - Native Move Direction Dev-Only Entry
> [已归档] 2026-03-31 - Native Move Paused And Return To Mainline

## Checkpoint 29 - 2026-04-01 Phase 1 Emotion Alias Cleanup

### 当前阶段
- 阶段 3：继续 phase 1 正式协议维护，不进入 phase 2，也不重开 native move

### 本轮完成内容
- 在 `VPet.Plugin.AgentBridge/AgentBridgePoller.cs` 中把 graph 解析收口为三层：
  - 显式 `graph`
  - stable emotion / expression alias
  - legacy 近似映射
- 当前 stable alias 明确保持为：
  - `think`
  - `thinking`
  - `pinch`
- `shy` 继续只保留为 legacy≈`pinch` 兼容，不升级成新的正式 phase 1 emotion
- `/dev/control` 已同步更新文案：
  - `graph` 字段明确为显式优先
  - `emotion` 字段明确区分正式值与 `shy (legacy≈pinch)`
- `spec/protocol-phase1.md` 已同步写清这条边界
- `quick-tests.json` 已补三条 phase 1 emotion 回归项：
  - `emotion-thinking`
  - `emotion-pinch`
  - `emotion-shy-legacy`

### 本轮决策与原因
- 决策：phase 1 的 emotion alias 继续保持小而明确，避免回到“靠继续堆 alias 承接展示层扩展”的方向
- 原因：当前主线只需要维护稳定基线；真正的控制面扩张仍然属于冻结中的 phase 2

### 本轮沉淀经验
- 在 phase 1 里，最容易再次扩散协议面的点不是 move，而是 `emotion.set`
- 兼容旧调用和值得正式承诺的新语义不是一回事；把 `shy` 显式降级为 legacy 近似，比默默继续把它当正式值更稳
- `quick-tests.json` 之前对 emotion alias 基本没有单独回归项，这会让协议边界长期只存在于代码和记忆里

### 验证情况
- 待运行代码级验证：
  - `python -m compileall backend-agent/app`
  - `quick-tests.json` JSON 解析校验
  - `dotnet build 'VPet.Plugin.AgentBridge/VPet.Plugin.AgentBridge.csproj' -c Debug`
- 若插件 build 失败，仍优先按既有注意事项判断是否为运行中 VPet 锁 DLL

### 下一步
- 不做真实联调
- 由你在 `/dev/quick-test` 自己回写：
  - `emotion-thinking`
  - `emotion-pinch`
  - `emotion-shy-legacy`
- 如果这 3 条稳定，再决定：
  - 是否将 `emotion -> graph` 这一项从活跃任务里视为已收口
  - 还是继续保留为“仅在 phase 2 catalog/play 体系下再处理”的开放项

### 可以从活跃上下文中移除的内容
- “phase 1 的 emotion 边界还只存在于散落硬编码里” 这件事

## Checkpoint 30 - 2026-04-01 Pause Handoff After Phase 1 Emotion Cleanup

### 当前阶段
- 阶段 3：phase 1 主线稳定维护，native move 继续 paused，phase 2 继续冻结

### 本轮完成内容
- 新建 handoff：
  - `handoffs/2026-04-01-017-phase1-emotion-cleanup-pause.md`
- 更新 handoff 索引的最新入口到：
  - `2026-04-01-017-phase1-emotion-cleanup-pause.md`
- 更新根目录继续提示词：
  - `CONTINUE_VPET_BRIDGE_PROMPT.md`
- 同步 `state.md` 的最新 handoff 指针
- 同步 `session-tasks.md`，把 phase 1 emotion alias 的实现收口和待回写测试分开记录

### 本轮决策与原因
- 决策：当前先以 handoff + continue prompt 的形式冻结本轮上下文，而不是再继续扩实现
- 原因：当前代码级工作已经收口，剩余主要是用户自己回写真实 quick test 结果

### 下一步
- 由用户自己在 `/dev/quick-test` 回写：
  - `emotion-thinking`
  - `emotion-pinch`
  - `emotion-shy-legacy`
- 下轮恢复时优先从新 handoff 和 `CONTINUE_VPET_BRIDGE_PROMPT.md` 开始

## Checkpoint 31 - 2026-05-01 DevFlow Migration

### 当前阶段
- 阶段 3：phase 1 正式协议维护；mission 工作流入口从 `context-budget-explore` 迁移到 `devflow`

### 本轮完成内容
- 将 `.explore/desktop-pet-vpet-body-bridge/` 完整复制为 `.devflow/desktop-pet-vpet-body-bridge/`
- 新增 devflow 轻量 plan / tasks：
  - `plans/2026-05-01-devflow-migration-plan.md`
  - `plans/2026-05-01-devflow-migration-light-tasks.md`
- 新增 handoff：
  - `handoffs/2026-05-01-018-devflow-migration.md`
- 更新 `handoffs/index.md`，将最新入口切到 devflow migration handoff
- 更新根目录 `CONTINUE_VPET_BRIDGE_PROMPT.md`，下一轮明确使用 `$devflow`
- 更新 `/dev/quick-test` catalog 路径到 `.devflow/.../quick-tests.json`

### 本轮决策与原因
- 决策：旧 `.explore/desktop-pet-vpet-body-bridge/` 保留为 legacy，不再作为新一轮写入目标
- 原因：避免 devflow 状态、handoff 与真实 quick test 回写分裂到两个工作区

### 下一步
- 新对话恢复时读取 `.devflow/desktop-pet-vpet-body-bridge/` 下的 state / checkpoints / 最新 handoff / protocol / quick-tests
- 当前仍继续 phase 1，不重开 native move，不提前进入 phase 2
- 由用户自己在 `/dev/quick-test` 回写 `emotion-thinking / emotion-pinch / emotion-shy-legacy`

