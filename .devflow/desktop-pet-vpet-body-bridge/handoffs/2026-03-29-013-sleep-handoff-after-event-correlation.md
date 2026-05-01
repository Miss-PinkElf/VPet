# Handoff: Sleep Handoff After Event Correlation

## Session Metadata
- Created: 2026-03-29
- Project: `D:\Users\Mobius\Desktop\mine\AAA-code\VPet`
- Mission: `.explore/desktop-pet-vpet-body-bridge`
- Branch: `shuowang/dev-vpet`
- Continues from: `2026-03-29-012-sleep-handoff-after-sequence-gating.md`
- Session focus: 为更长 sequence 增加最小事件关联字段，补 6 步 story sequence，更新联调默认示例与测试目录，并在休息前收口记录与恢复入口

## Current State Summary

当前 phase 1 身体层桥接已经进一步收口到下面这个状态：

1. `bubble.show / motion.play / mode.switch / emotion.set / window.move` 已可用
2. `window.move` 主协议保持为显式 `dx/dy/style`
3. sequence 最小完成门控已落地：
   - `event_applied`
   - `move_complete`
   - `motion_complete`
4. 当前两条核心 4 步链路仍作为 phase 1 基线：
   - `thinking-walk-think`
   - `bubble-move-touch-recover`
5. 本轮新增了最小事件关联字段：
   - 事件侧：`event_id / sequence_name / step_index`
   - 状态侧：`last_event_id / last_sequence_name / last_step_index`
6. 本轮新增了更长的 6 步 story sequence：
   - `think-speak-move-touch-speak-recover`

## Important Context

- 方向仍然冻结：
  - `VPet` 是身体层 / 前端执行层
  - `Python backend-agent` 是大脑
  - 第一阶段不要深改 `GameCore`
- 当前不要做的事：
  - 不要再把 `DisplayMove()` 和桥接显式位移绑在同一次移动里
  - 不要回到“主要靠调大 delay 猜动作完成”的路径
  - 不要把 `move.intent` 重新拉回主协议
- 真实联调协作边界已明确：
  - assistant 负责补测试定义、payload、观察字段、通过标准
  - 真实 VPet 联调与结果回写由你自己完成
- 如果后续需要改插件并重编：
  - 先停掉 VPet
  - 再编译
  - 否则 DLL 会被锁住

## What Was Confirmed This Session

- Python 后端已完成事件关联字段贯通：
  - `backend-agent/app/schemas/events.py`
  - `backend-agent/app/services/behavior_policy_engine.py`
  - `backend-agent/app/services/dev_sequence_orchestrator.py`
- C# 插件已完成事件关联字段接收与状态回传：
  - `VPet.Plugin.AgentBridge/AgentBridgeEvent.cs`
  - `VPet.Plugin.AgentBridge/AgentBridgePoller.cs`
  - `VPet.Plugin.AgentBridge/AgentBridgeStateSnapshot.cs`
- `/dev/control` 默认自定义 sequence 示例已切到新的 6 步 story sequence
- `quick-tests.json` 已新增 6 步测试项，但结果保持 `untested`
- `protocol-phase1.md` 已新增 `Shared Trace Metadata`
- `.explore` 主记录已同步到当前状态：
  - `state.md`
  - `checkpoints.md`
  - `decision-log.md`

## Validation Evidence

- `python -m compileall backend-agent/app` 通过
- `quick-tests.json` JSON 解析通过
- `dotnet build VPet.Plugin.AgentBridge/VPet.Plugin.AgentBridge.csproj -c Debug` 在真实环境下通过

## Important Technical Insight

- 对更长的 sequence，`last_event_type` 只能回答“刚消费了什么类型”，不能稳定回答“消费的是这条 sequence 的第几步”
- 当前 `event_id / sequence_name / step_index` 的价值，主要在于重复事件类型，例如同一条链里出现两次 `bubble.show`
- 当前门控已优先按 `event_id` 对齐；如果运行时没有该字段，再回退到 `last_event_type + last_event_at`

## Critical Files

- `.explore/desktop-pet-vpet-body-bridge/state.md`
- `.explore/desktop-pet-vpet-body-bridge/checkpoints.md`
- `.explore/desktop-pet-vpet-body-bridge/decision-log.md`
- `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
- `.explore/desktop-pet-vpet-body-bridge/spec/protocol-phase1.md`
- `backend-agent/app/schemas/events.py`
- `backend-agent/app/services/behavior_policy_engine.py`
- `backend-agent/app/services/dev_sequence_orchestrator.py`
- `backend-agent/app/api/routes/dev_control.py`
- `VPet.Plugin.AgentBridge/AgentBridgeEvent.cs`
- `VPet.Plugin.AgentBridge/AgentBridgePoller.cs`
- `VPet.Plugin.AgentBridge/AgentBridgeStateSnapshot.cs`
- `CONTINUE_VPET_BRIDGE_PROMPT.md`

## Immediate Next Steps

1. 先读取：
   - `state.md`
   - `decision-log.md`
   - `checkpoints.md`
   - `handoffs/index.md`
   - 本 handoff
   - `protocol-phase1.md`
   - `quick-tests.json`
2. 不要重新做大范围分析
3. 由你自己在真实 VPet 上测试：
   - `sequence-think-speak-move-touch-speak-recover`
4. 在 `quick-tests.json` 回写真实结果
5. 再根据真实结果判断：
   - 两次 `bubble.show` 是否已能稳定区分
   - 是否需要补更强关联字段
   - 是否需要把完成门控继续扩到更多步骤

## Potential Gotchas

- `bubble_visible` 依然更适合观察视觉残留，不适合单独判断事件顺序
- 长时间窗口采样会混入 VPet 自主移动噪声；验证位移应优先看短窗口
- `mode.switch(normal)` 后视觉可能存在短残留，判断 sequence 时优先看 `last_event_id / last_step_index`
- `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/` 是运行产物目录，不应作为源码提交对象

## Commit Intent

本轮提交应覆盖：

- 后端事件关联字段与 sequence 编排改动
- 插件事件接收与状态回传改动
- 联调默认示例与测试目录更新
- `.explore` 记录、handoff 与继续提示词

不应包含：

- `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/`
- 用户自己的无关改动，如 `.codex/AGENTS.md`、`zzz-cmd.md`

## Resume Guidance

恢复时直接优先打开：

1. `CONTINUE_VPET_BRIDGE_PROMPT.md`
2. `.explore/desktop-pet-vpet-body-bridge/handoffs/2026-03-29-013-sleep-handoff-after-event-correlation.md`
