# Handoff: VPet 身体层桥接 sleep resume ready

## Session Metadata
- Created: 2026-03-28
- Project: `D:\Users\Mobius\Desktop\mine\AAA-code\VPet`
- Mission: `.explore/desktop-pet-vpet-body-bridge`
- Branch: `shuowang/dev-vpet`
- Session focus: 收口标准 `18787` 启动链路，补长链路 sequence/scenario 样例，并为下次继续真实联调准备恢复入口

## Current Goal

继续把 VPet 身体层第一阶段桥接打磨到“可稳定演示”。本阶段已经不再卡在启动链路，而是进入：

1. 用 4 步 sequence/scenario 验证真实 VPet 运行态的状态时间线
2. 判断当前状态字段是否还要补极少量桌宠运行态
3. 决定 `move.intent` 从运行时入口退场的最终节奏

## Current State

- `VPet.Plugin.AgentBridge` 仍是唯一桥接实现
- `window.move(dx, dy)` 仍是第一阶段唯一主移动协议
- `move.intent` 仅保留最薄 legacy 兼容
- 最小状态快照仍是：
  - `left`
  - `top`
  - `right`
  - `bottom`
  - `zoom_ratio`
  - `display_name`
  - `display_type`
  - `display_animat`
  - `mode`
  - `working_state`
  - `work_name`
  - `work_type`
  - `bubble_visible`
  - `last_event_type`
- `backend-agent` 当前编排入口：
  - `GET /api/dev/scenarios`
  - `POST /api/dev/scenarios/{scenario_id}`
  - `POST /api/dev/sequences`
- 当前预设 scenario 共 6 个：
  - `move-then-bubble`
  - `bubble-then-move`
  - `move-then-motion`
  - `move-then-bubble-touch`
  - `thinking-walk-think`
  - `bubble-move-touch-recover`

## What Was Completed This Session

- 将 `backend-agent/run-dev.ps1` 和 `run-dev.sh` 改为默认不带 `uvicorn --reload`
- 增加显式热重载开关：
  - PowerShell: `-Reload`
  - 环境变量: `PET_BACKEND_RELOAD=1`
- 强化 `start-vpet-bridge.ps1`：
  - 清理旧后端时同时合并 `Get-NetTCPConnection` 与 `netstat` 的监听 PID
  - 启动后必须通过 `/api/dev/scenarios` 与 `/dev/control` 的 `sequence-editor` 校验
- 扩展 `DevSequenceOrchestrator`，增加两个 4 步长链路 scenario
- 将 `/dev/control` 默认 sequence JSON 升级成 4 步样例
- 已将 `.explore`、迁移文档和映射文档同步到当前真实状态

## Validation Evidence

- `python -m compileall backend-agent/app` 通过
- 代码内验证通过：
  - `thinking-walk-think` 返回 `step_count=4`
  - 自定义 4 步 sequence 返回 `step_count=4`
  - 事件总线收到的顺序与延迟编排一致
- 标准 `18787` 链路验证通过：
  - `.\start-vpet-bridge.ps1 -SkipBuild` 可正常启动
  - `GET http://127.0.0.1:18787/api/dev/scenarios` 返回 6 个场景
  - `GET http://127.0.0.1:18787/dev/control` 可见新的 `sequence-editor`
  - `POST /api/dev/scenarios/thinking-walk-think` 返回 `accepted`
  - `POST /api/dev/sequences` 的 4 步请求返回 `accepted`

## Key Decisions

- 标准启动链路默认关闭 `uvicorn --reload`
  - 原因：Windows 下 reload watcher/worker 残留会污染 `18787` 联调
- 长链路联调先固定为 4 步样例
  - 原因：足以覆盖“思考态 -> 位移 -> 说话 -> 恢复”这类第一阶段关键编排

## Open Questions

- 真实 VPet 运行态下，4 步 sequence 的状态时间线是否还需要补 `topmost / hitthrough` 一类字段
- `move.intent` 是继续保留最薄兼容，还是下一轮从 UI 和运行时都进一步退场
- `emotion -> graph` 是否需要继续做运行时导出，而不是只靠人工映射

## Immediate Next Steps

1. 重新启动真实 VPet 链路：`.\start-vpet-bridge.ps1 -SkipBuild`
2. 在真实 VPet 窗口上依次触发：
   - `thinking-walk-think`
   - `bubble-move-touch-recover`
3. 采样 `GET /api/dev/state` 的时间线，重点看：
   - `mode`
   - `display_animat`
   - `bubble_visible`
   - `last_event_type`
   - `working_state / work_name / work_type`
4. 判断是否还需要补少量桌宠运行态字段
5. 决定 `move.intent` 的退场方式

## Important Gotchas

- 不要再把 `18787` 上看到旧页面默认理解成代码没改进去；先确认是否误开了 reload
- 构建产物目录 `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/` 不应提交
- 当前工作区还有无关文件：
  - `.codex/AGENTS.md`
  - `zzz-cmd.md`
  这两者都不要误提交

## Resume Guidance

恢复时按这个顺序读：

1. `.explore/desktop-pet-vpet-body-bridge/state.md`
2. `.explore/desktop-pet-vpet-body-bridge/handoffs/index.md`
3. 本文件
4. `.explore/desktop-pet-vpet-body-bridge/next-chat-prompt-2026-03-28.md`
5. `docs/agent-desktop-pet/migration/2026-03-27-vpet-body-bridge-implementation-guide.md`
6. `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`

