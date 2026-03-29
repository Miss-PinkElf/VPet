# Handoff: Display Control Surface And Rest Handoff

## Session Metadata
- Created: 2026-03-30
- Project: `D:\Users\Mobius\Desktop\mine\AAA-code\VPet`
- Mission: `.explore/desktop-pet-vpet-body-bridge`
- Branch: `shuowang/dev-vpet`
- Continues from: `2026-03-29-013-sleep-handoff-after-event-correlation.md`
- Session focus: 梳理 `VPet` 展示层本体可控范围，确认“当前桥接暴露面”和“前端真实展示能力”的差口，产出全控可行性方案，并在休息前收口文档与恢复入口

## Current State Summary

当前 mission 已经进入“两条主线并行”的状态：

1. phase 1 最小正式协议已经稳定：
   - `bubble.show`
   - `motion.play`
   - `mode.switch`
   - `emotion.set`
   - `window.move`
2. phase 1 的关键 sequence 门控已经落地：
   - `event_applied`
   - `move_complete`
   - `motion_complete`
3. 更长的 6 步 story sequence 已经定义完成，但真实联调结果仍应由你自己回写
4. 本轮新增了一条 phase 2 预研结论：
   - `VPet` 展示层本体真实可控面远大于当前桥接白名单
   - 如果要继续扩控制面，不应继续只扩大 `motion.play / emotion.set` 的手写映射
   - 应改为：
     - `graph.catalog`
     - `graph.play`
     - `behavior.invoke`

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
- 这两个文档不要混写，否则 phase 1 边界会被污染
- 当前桥接暴露面仍是“小白名单”
- 但源码和资源目录已确认：
  - `Main.Display(string name, AnimatType, ...)` 可按 graph 名播放
  - `Main.Say(text, graphname, force)` 可带说话 graph
  - `StateTWO / SideHide_* / WORK / IDEL / MOVE / Say` 等展示能力本体上都存在

## What Was Confirmed This Session

- 当前 `VPet` 展示层本体可控范围已重新梳理完成
- 当前 `vup` 角色资源已确认存在这些重要展示分类：
  - `IDEL`
  - `MOVE`
  - `WORK`
  - `Say`
  - `Think`
  - `Pinch`
  - `Sleep`
  - `State`
  - `Switch`
  - `SideHide_Left_Main`
  - `SideHide_Left_Rise`
  - `SideHide_Right_Main`
  - `SideHide_Right_Rise`
  - `StartUP`
  - `Shutdown`
  - `Music`
  - `LevelUP`
  - `BDay`
- 当前桥接仍只正式暴露了少量 alias：
  - `motion.play` 的小白名单
  - `emotion.set` 的小白名单
  - `mode.switch` 的小白名单
- 本轮已新增专题设计文档：
  - `.explore/desktop-pet-vpet-body-bridge/spec/display-control-surface-and-full-control-plan.md`
- `.explore` 记录已同步更新：
  - `state.md`
  - `decision-log.md`
  - `learnings.md`
  - `checkpoints.md`
  - `session-tasks.md`
  - `spec/proposal.md`
  - `spec/design.md`

## Validation Evidence

- 新专题文档已写入 mission `spec/`
- `proposal.md` 与 `design.md` 已挂接到新专题文档
- `state.md` 已同步记录：
  - 新文档位置
  - phase 2 候选方向
  - 下一步优先顺序
- 当前工作树中存在一个与本轮无关的用户改动：
  - `zzz-cmd.md`
  - 不应纳入本轮提交

## Important Technical Insight

- “当前桥接能控什么”和“前端展示层本体能点出什么”是两个不同问题
- 如果目标是“视觉上把现有资源都点出来”，现有底层能力已经足够
- 如果目标是“让后端稳定全控展示层”，必须分层，而不是继续堆 alias
- 最重要的边界是：
  - `graph.play` 适合资源点播
  - `behavior.invoke` 适合贴边、探头、摸头、拖拽这类复杂行为

## Critical Files

- `.explore/desktop-pet-vpet-body-bridge/state.md`
- `.explore/desktop-pet-vpet-body-bridge/decision-log.md`
- `.explore/desktop-pet-vpet-body-bridge/learnings.md`
- `.explore/desktop-pet-vpet-body-bridge/checkpoints.md`
- `.explore/desktop-pet-vpet-body-bridge/session-tasks.md`
- `.explore/desktop-pet-vpet-body-bridge/spec/protocol-phase1.md`
- `.explore/desktop-pet-vpet-body-bridge/spec/display-control-surface-and-full-control-plan.md`
- `.explore/desktop-pet-vpet-body-bridge/handoffs/index.md`
- `CONTINUE_VPET_BRIDGE_PROMPT.md`
- `VPet.Plugin.AgentBridge/AgentBridgePoller.cs`
- `VPet-Simulator.Core/Graph/GraphInfo.cs`
- `VPet-Simulator.Core/Graph/GraphCore.cs`
- `VPet-Simulator.Core/Display/MainDisplay.cs`
- `VPet-Simulator.Core/Display/MainLogic.cs`

## Immediate Next Steps

恢复时先做下面两件事之一，不要两条线同时发散：

1. 如果继续 phase 1：
   - 先读取最新 handoff、`state.md`、`protocol-phase1.md`
   - 等你自己回写更长 story sequence 的真实结果
   - 再决定是否继续扩 `wait_for` 或事件关联

2. 如果开启 phase 2 控制面扩展：
   - 先读取新专题文档
   - 先做 `graph.catalog`
   - 再做 `graph.play`
   - 最后再做 `behavior.invoke`

## Potential Gotchas

- 不要把新专题文档误当成“当前已经实现的正式协议”
- 不要把 `graph` 资源存在误判成“已有稳定高层行为协议”
- 不要把 `StateTWO / SideHide_* / WORK / IDEL` 这类本体能力，因为桥接没暴露，就误判成前端不支持
- 如果要提交，记得排除与本轮无关的 `zzz-cmd.md`
- 如果后续要改插件并重编，先停掉 VPet，否则 DLL 会被锁住

## Commit Intent

本轮提交应覆盖：

- `.explore/desktop-pet-vpet-body-bridge/` 下的记录更新
- 新增的 `display-control-surface-and-full-control-plan.md`
- 新增 handoff
- 更新后的 `CONTINUE_VPET_BRIDGE_PROMPT.md`

不应包含：

- 用户自己的无关改动，例如 `zzz-cmd.md`
- 运行产物目录，例如 `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/`

## Resume Guidance

恢复时优先打开：

1. `CONTINUE_VPET_BRIDGE_PROMPT.md`
2. `.explore/desktop-pet-vpet-body-bridge/handoffs/2026-03-30-014-display-control-surface-and-rest-handoff.md`
3. `.explore/desktop-pet-vpet-body-bridge/spec/display-control-surface-and-full-control-plan.md`
