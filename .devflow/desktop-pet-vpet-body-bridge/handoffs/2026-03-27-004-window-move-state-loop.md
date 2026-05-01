# Handoff: VPet 身体层桥接 `window.move` 与最小状态回传闭环

## Session Metadata
- Created: 2026-03-27
- Project: `E:\Learn\Vs\Code\VPet`
- Mission: `.explore/desktop-pet-vpet-body-bridge`
- Branch: `shuowang/dev-vpet`
- Session focus: 补 `window.move`、打通最小状态回传、完成真实联调验证

## Current State Summary

这一轮已经不再停留在“测试页有 move 但 VPet 不消费”的状态。桥接协议正式收敛为显式 `window.move(dx, dy)`，插件已将其映射到 `MW.Core.Controller.MoveWindows(...)`。后端同时新增了 `POST /vpet/state` 和 `GET /api/dev/state`，`/dev/control` 现在既能发送 `window.move`，也能展示 VPet 的最新状态快照。2026-03-27 本地联调已做过一轮真实验证：发送 `dx=120, dy=-40` 后，状态从 `left=1105.6, top=1188.8` 变为 `left=1225.6, top=1148.8`，增量与请求一致。

## Codebase Understanding

### Architecture Overview

- `backend-agent/` 继续作为大脑与联调入口
- `VPet.Plugin.AgentBridge/` 是身体层桥接插件
- `window.move` 现在走显式位移协议，不再依赖模糊 intent
- 状态回传由插件主动 POST 到后端保存，测试页再从后端拉取显示

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `VPet.Plugin.AgentBridge/AgentBridgePoller.cs` | 事件轮询、分发、状态回传 | `window.move` 和 `state report` 主入口 |
| `VPet.Plugin.AgentBridge/AgentBridgeStateSnapshot.cs` | 状态回传 JSON 模型 | 保证字段名和后端 schema 对齐 |
| `backend-agent/app/schemas/events.py` | 事件与状态 schema | 新增 `window.move` 和 `VPetStateSnapshot` |
| `backend-agent/app/api/routes/events.py` | 轮询/状态接口 | 新增 `/vpet/state` 与 `/api/dev/state` |
| `backend-agent/app/api/routes/dev_control.py` | 联调测试页 | 已切到显式 move 协议并展示状态 |
| `VPet-Simulator.Windows/bin/x64/Debug/net8.0-windows/Setting.lps` | 当前本地联调运行设置 | 本轮为验证额外补了 `onmod:|agentbridge:|` |

### Key Patterns Discovered

- 对窗口位移这类身体层能力，显式协议比 intent 协议更稳
- 最小状态回传接通后，可以直接用状态差值验证位移效果
- 本地联调若发现事件队列不消费，先检查运行中的 `Setting.lps` 是否启用了目标 mod

## Work Completed

### Tasks Finished

- [x] 引入 `window.move(dx, dy)` 并接到 VPet 身体层
- [x] 保留 `move.intent` 的最薄 legacy 兼容
- [x] 打通最小状态回传
- [x] 更新 `/dev/control` 测试页
- [x] 完成一次真实位移联调验证

### Validation Evidence

- 后端应用可成功加载以下新路由：
  - `/vpet/state`
  - `/api/dev/state`
- 插件项目已成功编译：
  - `VPet.Plugin.AgentBridge -> ...\bin\x64\Debug\net8.0-windows\VPet.Plugin.AgentBridge.dll`
- 实际联调结果：
  - before: `left=1105.6`, `top=1188.8`
  - request: `dx=120`, `dy=-40`
  - after: `left=1225.6`, `top=1148.8`
  - delta: `+120`, `-40`
  - `last_event_type=window.move`
  - `display_name=walk.right`

## Pending Work

### Immediate Next Steps

1. 继续验证 `window.move` 与 `bubble.show / motion.play` 的组合体感
2. 判断最小状态回传是否要补边界距离或工作态字段
3. 评估 `move.intent` 是否只保留文档层 legacy 提示，而不再鼓励继续使用

### Blockers/Open Questions

- `move.intent` 要保留多久
- 状态回传是否需要继续扩容
- `emotion -> graph` 是否要走运行时导出

## Context for Resuming Agent

### Important Context

- 当前 `.explore/desktop-pet-vpet-body-bridge/` 仍是唯一真相源
- 当前移动协议已经收敛为 `window.move(dx, dy)`，不要再回头扩散 `follow_cursor` 一类 intent
- 如果本地联调发现事件队列不消费，优先检查：
  - `VPet-Simulator.Windows/bin/x64/Debug/net8.0-windows/Setting.lps`
  - 是否包含 `onmod:|agentbridge:|`

### Potential Gotchas

- `VPet.Plugin.AgentBridge.dll` 在 VPet 运行时会被锁住，改插件后必须先停 VPet 再重编
- 插件状态回传 JSON 字段名必须保持 snake_case，否则后端会 422 丢弃
- 旧 `.codex/explore/desktop-pet-vpet-body-bridge/` 不再是最新事实来源

## Related Resources

- `.explore/desktop-pet-vpet-body-bridge/state.md`
- `.explore/desktop-pet-vpet-body-bridge/checkpoints.md`
- `.explore/desktop-pet-vpet-body-bridge/decision-log.md`
- `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`
