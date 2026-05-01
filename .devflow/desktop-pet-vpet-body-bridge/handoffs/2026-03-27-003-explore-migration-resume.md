# Handoff: VPet 身体层桥接 `.explore` 迁移后续接

## Session Metadata
- Created: 2026-03-27
- Project: `E:\Learn\Vs\Code\VPet`
- Mission: `.explore/desktop-pet-vpet-body-bridge`
- Branch: `shuowang/dev-vpet`
- Session focus: 插件化收敛后的工作区迁移、记录体系切换与后续续接准备

## Current State Summary

当前 VPet 身体层桥接已经不再是主工程内置 POC，而是独立的 `MainPlugin` 插件 `VPet.Plugin.AgentBridge/`。真实联调已经完成一轮，`bubble.show / motion.play / mode.switch / emotion.set` 可用，`bubble.show + touch_head/touch_body/pinch/thinking` 已调整为更接近 VPet 原生的动作+说话编排。新一版 `context-budget-explore` 已启用，本专项与全局 roadmap 的 mission 文档已经迁移到仓库根目录 `.explore/`，旧 `.codex/explore/` 仅作为 legacy 参考。下一步不是再证明路线成立，而是直接补 `window.move` 和最小状态回传。

## Codebase Understanding

### Architecture Overview

- `backend-agent/` 继续作为外部大脑和联调入口，负责 `/vpet/events/next` 与 `/dev/control`
- `VPet.Plugin.AgentBridge/` 是新的身体层桥接插件项目
- `VPet-Simulator.Windows/mod/1200_AgentBridge/` 是插件 mod 壳，`plugin/` 目录承载编译产物
- `VPet` 主工程继续作为身体层执行环境，不再内置桥接启动逻辑

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `VPet.Plugin.AgentBridge/AgentBridgePlugin.cs` | 插件生命周期入口 | `GameLoaded()` 启动桥接，`EndGame()` 释放 |
| `VPet.Plugin.AgentBridge/AgentBridgePoller.cs` | 事件轮询与分发核心 | 后续补 `window.move` 的第一入口 |
| `VPet.Plugin.AgentBridge/AgentBridgeConfig.cs` | 桥接配置 | 轮询地址和超时配置 |
| `backend-agent/app/api/routes/dev_control.py` | 联调测试页 | 当前已是下拉式页面 |
| `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md` | 动作 / 表情映射清单 | 后续修图谱时的协议真相源 |
| `.explore/desktop-pet-vpet-body-bridge/state.md` | 新专项状态真相源 | 新对话恢复时优先读取 |
| `.explore/desktop-pet-vpet-body-bridge/handoffs/index.md` | 新 handoff 索引 | 管理多次续接 |

### Key Patterns Discovered

- 这条线已经进入“身体层能力补齐”阶段，不再讨论“VPet 能不能做身体层”
- 对原生交互动作，优先复用 VPet 自己的显示编排，不做粗暴的双命令硬拼
- 新增过程记录统一写入 `.explore/`，不要再回写旧 `.codex/explore/`

## Work Completed

### Tasks Finished

- [x] 将桥接实现收敛到 `VPet.Plugin.AgentBridge/`
- [x] 将主工程内置桥接启动钩子摘除
- [x] 构建并验证插件版桥接可运行
- [x] 将专项与全局 roadmap mission 迁移到 `.explore/`
- [x] 为新 mission 结构补齐 `workflow / state / decision-log / learnings / checkpoints / session-tasks / spec / handoffs/index`

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `.explore/desktop-pet-vpet-body-bridge/*` | 新建专项 mission 工作区 | 切换到新的 `context-budget-explore` 结构 |
| `.explore/desktop-pet-graduation-roadmap/*` | 新建全局 mission 工作区 | 让毕设主线和专项记录统一 |
| `.explore/desktop-pet-vpet-body-bridge/handoffs/2026-03-27-003-explore-migration-resume.md` | 新 handoff | 为长上下文续接准备清晰恢复点 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 新 truth source 切到 `.explore/` | 继续用 `.codex/explore/`、双轨并行 | 新 skill 已明确以 `.explore/` 为标准工作区 |
| 旧 `.codex/explore/` 保留但降级为 legacy | 直接删除、继续写旧目录 | 先保留参考，避免历史信息丢失 |
| 下一步直接做 `window.move` | 继续扩动作语义、重做映射表 | `move.intent` 目前测试页可发但 VPet 不消费，是最明显缺口 |

## Pending Work

### Immediate Next Steps

1. 在 `VPet.Plugin.AgentBridge/AgentBridgePoller.cs` 中补 `window.move` 或 `move.intent` 到 `MW.Core.Controller.MoveWindows(...)` 的映射
2. 更新 `/dev/control`，把未接线事件标明或与新实现对齐
3. 设计并实现最小状态回传

### Blockers/Open Questions

- [ ] `window.move` 协议形态还未最终确定，是继续用 `move.intent` 还是改为更明确的位移参数
- [ ] 最小状态回传应只返回位置 / mode / display type，还是同时返回更多工作态信息
- [ ] `emotion -> graph` 长期是否需要运行时导出能力

### Deferred Items

- 更完整的情绪语义映射
- 论文 / 答辩叙事材料的系统整理

## Context for Resuming Agent

### Important Context

新的续接入口已经不是 `.codex/explore/desktop-pet-vpet-body-bridge/`，而是 `.explore/desktop-pet-vpet-body-bridge/`。如果开新对话继续，优先读：

1. `.explore/desktop-pet-vpet-body-bridge/state.md`
2. `.explore/desktop-pet-vpet-body-bridge/handoffs/index.md`
3. 本 handoff
4. `VPet.Plugin.AgentBridge/AgentBridgePoller.cs`

现在不要再花时间重新分析“VPet 身体层路线”本身。路线、插件化和首轮联调都已经完成，真正的下一步是补身体层控制缺口。

### Assumptions Made

- 当前分支仍是 `shuowang/dev-vpet`
- `backend-agent/.venv` 仍可用
- `VPet.Plugin.AgentBridge.dll` 可通过主工程构建继续产出到 mod 壳目录
- 后续会继续沿用 `18787` 端口

### Potential Gotchas

- 测试页里 `move.intent` 当前仍可能是“页面可发、VPet 未消费”的状态，别误判为页面 bug
- 构建前如果 VPet 正在运行，`Core.dll` 与 `Interface.dll` 可能会被锁住
- 旧 `.codex/explore/` 仍在仓库里，恢复时不要误把它当最新真相源

## Environment State

### Tools/Services Used

- `.NET 8`
- `backend-agent/.venv`
- `start-vpet-bridge-dev.ps1`
- `start-vpet-bridge-fast.ps1`

### Active Processes

- 上一轮通常会启动 VPet 和后端；恢复时先检查是否仍在运行

### Environment Variables

- `PET_BACKEND_HOST`
- `PET_BACKEND_PORT`
- `VPET_AGENT_BRIDGE_URL`
- `VPET_AGENT_BRIDGE_ENABLED`
- `VPET_AGENT_BRIDGE_INTERVAL_MS`
- `VPET_AGENT_BRIDGE_TIMEOUT_MS`

## Related Resources

- `.explore/desktop-pet-vpet-body-bridge/state.md`
- `.explore/desktop-pet-vpet-body-bridge/workflow.md`
- `.explore/desktop-pet-vpet-body-bridge/learnings.md`
- `.explore/desktop-pet-vpet-body-bridge/checkpoints.md`
- `.explore/desktop-pet-graduation-roadmap/state.md`
- `VPet.Plugin.AgentBridge/AgentBridgePlugin.cs`
- `VPet.Plugin.AgentBridge/AgentBridgePoller.cs`
- `backend-agent/app/api/routes/dev_control.py`
- `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`
