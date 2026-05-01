# Handoff: Phase 1 Sequence Acceptable, Walk Next

## Session Metadata
- Created: 2026-03-31
- Project: `E:\Learn\Vs\Code\VPet`
- Mission: `.explore/desktop-pet-vpet-body-bridge`
- Branch: `shuowang/dev-vpet`
- Continues from: `2026-03-30-014-display-control-surface-and-rest-handoff.md`
- Session focus: 继续 phase 1，收口 6 步 story sequence 的完成门控与尾段节奏，并在休息前把恢复入口切到“sequence 已可接受、下一步转向走路体感”

## Current State Summary

当前 mission 仍然保持“两条主线并行，但优先级明确”的状态：

1. phase 1 最小正式协议仍是当前主线：
   - `bubble.show`
   - `motion.play`
   - `mode.switch`
   - `emotion.set`
   - `window.move`
2. phase 1 的 sequence 门控已从原来的最小集合扩到：
   - `event_applied`
   - `move_complete`
   - `motion_complete`
   - `motion_recovered`
3. `sequence-think-speak-move-touch-speak-recover` 已完成多轮真实联调收口：
   - 当前结果可视为 `pass`
   - 你的最新反馈是“还行流畅度可以，只有一点点卡顿，可以接受”
4. 因此当前 phase 1 的主要剩余体验问题，已经不再是这条 6 步 sequence，而是：
   - `window.move(style=smart)` 的走路体感仍然生硬
5. phase 2 仍保持独立：
   - `graph.catalog`
   - `graph.play`
   - `behavior.invoke`
   当前不要因为走路问题或 sequence 问题而提前跳过去

## Important Context

- 当前方向仍然冻结：
  - `VPet` 是身体层 / 前端执行层
  - `Python backend-agent` 是大脑
  - 第一阶段不要深改 `GameCore`
- 当前必须区分两个文档边界：
  - `protocol-phase1.md`
    - 记录“当前已正式承诺的最小协议”
  - `display-control-surface-and-full-control-plan.md`
    - 记录“展示层全控专题设计”
- 当前移动协议仍然只承诺：
  - `window.move(dx, dy)`
- 原生 `walk/crawl/fall/climb` 仍不能重新和显式 `window.move` 绑回同一次移动里
- “所有动画做映射”仍然不是 phase 1 当前修复手段

## What Was Confirmed This Session

- 6 步 story sequence 已从 `mixed` 收口到可接受：
  - `sequence-think-speak-move-touch-speak-recover = pass`
- 为了收口这条链路，本轮已新增并落地：
  - `wait_for=motion_recovered`
- 当前 `motion.play` 相关完成门控分层变为：
  - `motion_complete`
    - 动作退出显示态即可放行
  - `motion_recovered`
    - 动作完成后还要回到更稳定的展示态再放行
- 对 6 步 chain 的尾段还做了节奏收口：
  - `touch_head` 的 `settle_ms` 逐步拉大到 `520`
  - 第二次 `bubble.show` 也补了 `settle_ms=520`
- 当前用户侧最新真实结论是：
  - 这条链路已可接受
  - 当前剩余体验问题主要转向走路体感生硬

## Validation Evidence

- `quick-tests.json` 已回写：
  - `sequence-think-speak-move-touch-speak-recover.result.status = pass`
- 后端代码已同步支持：
  - `motion_recovered`
- 已完成本地非真实联调验证：
  - `backend-agent/app` 的 `compileall` 通过
- assistant 没有替用户跑真实 GUI 联调；真实结论来自用户回写和口头反馈

## Critical Files

- `.explore/desktop-pet-vpet-body-bridge/state.md`
- `.explore/desktop-pet-vpet-body-bridge/decision-log.md`
- `.explore/desktop-pet-vpet-body-bridge/checkpoints.md`
- `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
- `.explore/desktop-pet-vpet-body-bridge/spec/protocol-phase1.md`
- `.explore/desktop-pet-vpet-body-bridge/spec/display-control-surface-and-full-control-plan.md`
- `.explore/desktop-pet-vpet-body-bridge/handoffs/index.md`
- `CONTINUE_VPET_BRIDGE_PROMPT.md`
- `backend-agent/app/schemas/events.py`
- `backend-agent/app/services/dev_sequence_orchestrator.py`
- `backend-agent/app/api/routes/dev_control.py`

## Immediate Next Steps

恢复后先只做一条主线，不要两条一起发散：

1. 继续 phase 1：
   - 先读取最新 handoff、`state.md`、`protocol-phase1.md`、`quick-tests.json`
   - 不再继续死抠 6 步 sequence
   - 直接转向 `window.move(style=smart)` 的走路体感问题
   - 重点讨论和实现：
     - 现在的“平滑分步位移”为什么看起来生硬
     - 是否需要单独的原生 walk 能力，但不要改坏 `window.move` 正式语义
2. phase 2 继续保持冻结，不提前展开：
   - `graph.catalog`
   - `graph.play`
   - `behavior.invoke`

## Potential Gotchas

- 不要把 `motion_recovered` 误当成“所有动作都已经有统一恢复门控”
- 不要因为 6 步 chain 已可接受，就误判“走路体感问题也已经解决”
- 不要因为当前开始讨论走路体感，就把原生 `DisplayMove()` 重新绑回 `window.move`
- 如果要改插件并重编，先停掉 VPet，否则 DLL 会被锁住
- 当前工作树里仍有运行产物变更：
  - `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/VPet.Plugin.AgentBridge.dll`
  这不应进入提交

## Commit Intent

本轮提交应覆盖：

- `.explore/desktop-pet-vpet-body-bridge/` 下的记录更新
- 新增 handoff
- 更新后的 `CONTINUE_VPET_BRIDGE_PROMPT.md`
- `backend-agent/app/` 下的 sequence 门控实现

不应包含：

- `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/VPet.Plugin.AgentBridge.dll`
- 其他运行产物
- 用户无关改动

## Resume Guidance

恢复时优先打开：

1. `CONTINUE_VPET_BRIDGE_PROMPT.md`
2. `.explore/desktop-pet-vpet-body-bridge/handoffs/2026-03-31-015-phase1-sequence-acceptable-walk-next.md`
3. `.explore/desktop-pet-vpet-body-bridge/state.md`
4. `.explore/desktop-pet-vpet-body-bridge/spec/protocol-phase1.md`
5. `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
