# Handoff: VPet 身体层桥接组合体验验证与状态扩展

## Session Metadata
- Created: 2026-03-27
- Project: `D:\Users\Mobius\Desktop\mine\AAA-code\VPet`
- Mission: `.explore/desktop-pet-vpet-body-bridge`
- Branch: `shuowang/dev-vpet`
- Session focus: 继续验证 `window.move` 与 `bubble.show / motion.play` 的组合体感，评估状态字段补充，并进一步下调 `move.intent`

## Current State Summary

这一轮没有回到路线讨论，而是直接沿着 `window.move + state` 闭环继续做联调打磨。插件状态回传已经从“最小可用”扩到“足够支撑组合联调”：除了原来的 `left / top / zoom_ratio / display_* / mode / last_event_type` 之外，又补了 `right / bottom / display_animat / working_state / work_name / work_type / bubble_visible`。`/dev/control` 也新增了组合场景按钮，不再只适合单条事件测试；同时 `move.intent` 在联调页中被明确标成 legacy 入口，不再作为第一阶段主路径。

## Work Completed

### Code Changes

- `VPet.Plugin.AgentBridge/AgentBridgeStateSnapshot.cs`
  - 扩状态字段：`right / bottom / display_animat / working_state / work_name / work_type / bubble_visible`
- `VPet.Plugin.AgentBridge/AgentBridgePoller.cs`
  - 在状态采集中读取边界距离、动画阶段、工作态与气泡可见性
- `backend-agent/app/schemas/events.py`
  - 对齐后端 `VPetStateSnapshot` schema
- `backend-agent/app/api/routes/dev_control.py`
  - 联调页新增组合场景按钮
  - `move.intent` 视觉降级为 legacy
  - 组合场景默认节奏按本轮实测结果调整
- `start-vpet-bridge.ps1`
  - 自动确保运行目录 `Setting.lps` 包含 `onmod:|agentbridge:|`

### Validation Evidence

- 2026-03-27 本地重新编译并启动成功：
  - `VPet.Plugin.AgentBridge -> ...\bin\x64\Debug\net8.0-windows\VPet.Plugin.AgentBridge.dll`
  - `VPet-Simulator.Windows -> ...\bin\x64\Debug\net8.0-windows\VPet-Simulator.Windows.dll`
- 2026-03-27 后端 `GET /api/dev/state` 已返回扩展字段：
  - `right`
  - `bottom`
  - `display_animat`
  - `working_state`
  - `work_name`
  - `work_type`
  - `bubble_visible`
- 2026-03-27 组合场景联调结论：
  - `bubble -> move` 稳定：移动发生时 `bubble_visible=true`，`last_event_type=window.move`
  - `move -> motion.play(touch_head)` 稳定：位移完成后可观察到 `display_type=Touch_Head`，`last_event_type=motion.play`
  - `move -> bubble` 不是不能用，但节奏过紧会不稳；本轮采样里约 `450ms` 间隔明显优于 `280ms`
  - `move -> bubble.touch_body` 可用，但切进原生触摸态比 plain bubble 更慢
- 2026-03-27 legacy 兼容仍有效：
  - 发送 `move.intent=dock_right`
  - 状态收敛到 `right=-0.8`
  - `last_event_type=move.intent`

## Key Decisions

- 第一阶段状态快照先扩到“可联调”，不做更大范围状态导出
- `move.intent` 继续保留运行时薄兼容，但退出第一阶段主验证面
- 启动脚本要主动兜底 `Setting.lps` 的 mod 启用状态

## Open Questions / Risks

- 当前状态字段是否已经足够，还是还要补极少量桌宠运行态如 `topmost / hitthrough`
- `move.intent` 何时彻底退到纯文档兼容
- 更长链路的动作编排是否需要后端显式 sequence/scenario 层，而不只是手动点测试页

## Immediate Next Steps

1. 基于扩展后的状态字段继续验证更长链路的组合编排
2. 判断当前状态字段集是否已经足够支撑第一阶段
3. 决定 `move.intent` 是继续保留运行时薄兼容，还是下一轮彻底退到文档层

## Context for Resuming Agent

### Important Context

- 当前 `.explore/desktop-pet-vpet-body-bridge/` 仍是唯一真相源
- `window.move(dx, dy)` 仍是第一阶段唯一主移动协议
- `/dev/control` 已经具备组合场景按钮，可以直接用于这类联调
- `start-vpet-bridge.ps1` 已经会自动补 `Setting.lps` 的 `onmod:|agentbridge:|`

### Potential Gotchas

- 插件 DLL 仍然会被运行中的 VPet 锁住；改插件前先停 VPet 再编译
- `bubble.show` 的 UI 生效晚于事件入队消费，判断组合体感时要结合 `bubble_visible` 和 `display_animat` 看时间差
- `move -> bubble` 的节奏如果压得太紧，体感会明显劣化；当前联调页已按 `450ms` 调整默认 gap
