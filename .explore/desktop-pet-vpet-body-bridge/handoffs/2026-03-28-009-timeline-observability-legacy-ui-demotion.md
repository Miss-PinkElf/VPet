# Handoff: VPet 时间线可观测性补强与 legacy UI 退场

## Session Metadata
- Created: 2026-03-28
- Project: `D:\Users\Mobius\Desktop\mine\AAA-code\VPet`
- Mission: `.explore/desktop-pet-vpet-body-bridge`
- Branch: `shuowang/dev-vpet`
- Session focus: 在真实 VPet 上验证长链路时间线，补时间可观测性，并把 `move.intent` 从联调 UI 进一步降级

## Current Goal

把第一阶段身体层桥接继续收口到“可稳定演示且可解释”。这一轮已经完成：

1. 真实 VPet 上的串行长链路采样
2. `last_event_at` 的落地
3. `/dev/control` 对 `move.intent` 的 UI 退场

接下来主要只剩两个判断：

1. `move.intent` 是否从运行时也退到纯文档兼容
2. 是否需要事件关联字段，而不是继续补更多桌宠工作态

## Current State

- `VPet.Plugin.AgentBridge` 仍是唯一桥接实现
- `window.move(dx, dy)` 仍是第一阶段唯一主移动协议
- `move.intent` 当前状态：
  - 运行时仍保留最薄兼容
  - `/dev/control` 已不再暴露
  - 文档中已明确其 legacy 身份
- 当前联调链路默认高频参数：
  - `VPET_AGENT_BRIDGE_INTERVAL_MS=250`
  - `VPET_AGENT_BRIDGE_STATE_INTERVAL_MS=500`
- 当前状态快照字段已包含：
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
  - `last_event_at`

## What Was Completed This Session

- 读取并遵循当前 `.explore` 真相源与迁移映射文档
- 用标准链路启动真实 VPet
- 修正一次错误的并行采样方式，改为串行单场景采样
- 确认现有边界距离字段已经足够，不再追加更多边界字段
- 确认 `working_state / work_name / work_type` 在当前 4 步长链路里的增益有限
- 新增 `last_event_at` 到插件状态快照与后端 schema
- 调整 `start-vpet-bridge.ps1`，让默认 dev 启动链路更适合真实联调采样
- 从 `/dev/control` 移除 `move.intent` 手动入口
- 更新迁移映射文档
- 重新编译插件并完成真实联调验证

## Validation Evidence

- `python -m compileall backend-agent/app` 通过
- `.\start-vpet-bridge.ps1` 重新编译并启动通过
- `GET /dev/control` 验证：
  - `sequence-editor` 存在
  - 不再暴露 `move.intent (legacy)` 选项
- `GET /api/dev/state` 验证：
  - 新字段 `last_event_at` 已返回
- 真实串行采样结果：
  - `thinking-walk-think` 可从状态中读出：
    - `mode.switch`
    - `window.move`
    - `bubble.show`
    - `mode.switch`
  - `bubble-move-touch-recover` 可从状态中读出：
    - `bubble.show`
    - `window.move`
    - `motion.play`
    - `mode.switch`
  - `motion.play(touch_head)` 在真实链路中能稳定映射到 `display_name=touch_head`
  - `last_event_at` 明确表明事件消费时间早于若干后续状态上报

## Key Decisions

- 不继续补 `topmost / hitthrough`
  - 原因：第一阶段联调判断的主要盲点不是桌宠工作态覆盖不够，而是时间线不够清晰
- `move.intent` 从联调 UI 退场
  - 原因：避免再把 legacy 协议和 `window.move` 并列展示，干扰主路径
- 当前若还要补字段，应优先补事件关联性
  - 原因：`last_event_at` 已经证明“时间可观测性”比新增更多 work 字段更有效

## Open Questions

- `move.intent` 是否从运行时也退到纯文档兼容
- 是否要在状态里增加：
  - `event_id`
  - `sequence_name`
  以便把后端 sequence 和 VPet 观察到的状态严格对应
- `emotion -> graph` 是否继续做运行时导出

## Important Gotchas

- 不要再用并行触发多个 scenario 的方式采样状态时间线，结果会互相污染
- 插件 DLL 仍会被运行中的 VPet 锁住；改插件前必须先停 VPet 再重编
- VPet 空闲时会继续自主移动，长窗口采样会混入自然位移
- `bubble_visible` 更像视觉残留标志，不要把它直接当作事件先后顺序判据

## Immediate Next Steps

1. 基于当前高频链路，设计一条更接近最终演示话术的 sequence
2. 判断是否真的需要 `event_id / sequence_name` 级别的关联字段
3. 决定 `move.intent` 是否只剩文档兼容
4. 如果继续暂停，再从本 handoff 恢复

## Resume Guidance

恢复时按这个顺序读：

1. `.explore/desktop-pet-vpet-body-bridge/state.md`
2. `.explore/desktop-pet-vpet-body-bridge/checkpoints.md`
3. `.explore/desktop-pet-vpet-body-bridge/handoffs/index.md`
4. 本文件
5. `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`
