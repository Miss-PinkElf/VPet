# Handoff: Sequence `wait_for` 门控已落地，下一步转真实 VPet 复测

## Session Metadata
- Created: 2026-03-28
- Project: `D:\Users\Mobius\Desktop\mine\AAA-code\VPet`
- Mission: `.explore/desktop-pet-vpet-body-bridge`
- Branch: `shuowang/dev-vpet`
- Session focus: 不再继续猜 delay，给 sequence 落地最小可用的 `wait_for` 完成门控

## Current Goal

继续把 VPet 第一阶段收口成“后端可稳定调用的身体层执行端”。

这一轮已经从“继续调 delay”切到“关键步骤显式等待完成后再继续”。

下一步不是再扩协议面，而是：

1. 用真实 VPet 复测两条核心 sequence
2. 判断新的门控是否已经把重合感压到可接受范围
3. 再决定是否还需要更深的原生动作回调接入或 `native_walk`

## What Was Completed

- 在 `backend-agent/app/schemas/events.py` 为 `DevSequenceStepRequest` 新增：
  - `wait_for`
  - `wait_timeout_ms`
  - `settle_ms`
- 在 `backend-agent/app/services/dev_sequence_orchestrator.py` 落地最小门控实现：
  - `event_applied`
  - `move_complete`
  - `motion_complete`
- 当前门控逻辑：
  - `move_complete`
    - 等待 `last_event_type=window.move`
    - 等待 `last_event_at` 晚于该步下发时刻
    - 如果有基线状态，再核对 `left/top` 是否落到目标位移
  - `motion_complete`
    - 等待 `motion.play` 被消费
    - 等待 `display_name/display_type` 先进入目标动作
    - 再等待其离开该动作态
- 两条核心长链路已切到新语义：
  - `thinking-walk-think`
    - `window.move(style=smart)` 使用 `wait_for=move_complete`
  - `bubble-move-touch-recover`
    - `window.move(style=smart)` 使用 `wait_for=move_complete`
    - `motion.play(touch_head)` 使用 `wait_for=motion_complete`
- 同步更新：
  - `/dev/control` 默认 sequence 示例
  - `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
  - `.explore/desktop-pet-vpet-body-bridge/spec/protocol-phase1.md`

## Validation Evidence

- `python -m compileall backend-agent/app` 通过
- 使用项目虚拟环境 `backend-agent/.venv/Scripts/python.exe` 运行模拟状态脚本通过：
  - `move_complete` 会等待到目标 `left/top` 状态回传后再结束
  - `motion_complete` 会等待到 `touch_head` 动作显示态退出后再结束

## Important Technical Insight

- 这一轮没有深改插件，也没有深改 `GameCore`
- 关键点是：现有状态回传已经足够支撑最小门控，不需要继续靠猜测 delay
- 对当前阶段最关键的两个问题：
  - `window.move` 是否真的走完
  - `touch_head` 这类短动作是否已经结束
  已经都有最小后端等待逻辑

## Current State

- `window.move(dx, dy)` 仍是第一阶段唯一正式移动协议
- `window.move.style=smart|smooth|snap` 保持不变
- 当前 sequence 不再只会按固定 delay 推进
- 但门控覆盖仍是有边界的：
  - 已实装：`move_complete`
  - 已实装：`motion_complete`
  - 已实装：`event_applied`
  - 未承诺：所有 `bubble.show / mode.switch / graph` 生命周期都已具备统一完成门控

## Open Questions

- 真实 VPet 上这套门控是否已经足够稳定
- `motion_complete` 是否适合扩到更多动作
- 是否要补 `event_id / sequence_name` 一类关联字段
- 是否还需要 `native_walk`

## Immediate Next Steps

1. 拉起真实联调链路
2. 在 `/dev/quick-test` 最小复测两条核心 sequence
3. 直接把结果回写到 `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
4. 观察：
   - 是否还会出现“上一步没做完就进下一步”
   - `style=smart` 体感是否仍可接受
5. 再决定是否要继续深挖原生回调或 `native_walk`

## Important Gotchas

- 不要回到“单纯加大 delay 猜完成”的路径
- 不要把原生 `DisplayMove()` 再和桥接显式位移绑回同一次移动
- 如果接下来要改插件并重编，仍然要先停 VPet，避免 DLL 锁住

## Related Files

- `backend-agent/app/schemas/events.py`
- `backend-agent/app/services/dev_sequence_orchestrator.py`
- `backend-agent/app/services/app_services.py`
- `backend-agent/app/api/routes/dev_control.py`
- `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
- `.explore/desktop-pet-vpet-body-bridge/spec/protocol-phase1.md`
- `.explore/desktop-pet-vpet-body-bridge/state.md`
- `.explore/desktop-pet-vpet-body-bridge/checkpoints.md`

## Resume Guidance

恢复时按这个顺序读：

1. `.explore/desktop-pet-vpet-body-bridge/state.md`
2. `.explore/desktop-pet-vpet-body-bridge/checkpoints.md`
3. `.explore/desktop-pet-vpet-body-bridge/handoffs/index.md`
4. 本文件
5. `.explore/desktop-pet-vpet-body-bridge/spec/protocol-phase1.md`
6. `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
