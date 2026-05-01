# Handoff: Smart Move 已落地，下一步切到 Sequence 完成门控

## Session Metadata
- Created: 2026-03-28
- Project: `D:\Users\Mobius\Desktop\mine\AAA-code\VPet`
- Mission: `.explore/desktop-pet-vpet-body-bridge`
- Branch: `shuowang/dev-vpet`
- Session focus: 收口移动体感，落地 `window.move.style`，并明确下一步要从 delay 编排切到动作完成门控

## Current Goal

继续把 VPet 身体层第一阶段收口为“你的后端可以把它当作前端执行层稳定调用”。

当前这个阶段已经完成：

1. `window.move` 从“乱走/乱爬”收口到可控语义
2. `/dev/quick-test` 已经成为当前阶段测试与结果回写入口
3. `window.move.style` 已经落地为 `smart / smooth / snap`

下一步真正该做的，不再是继续猜 delay，而是：

1. 给 sequence 增加“动作/位移完成后再继续”的门控
2. 再决定是否要引入更正式的 `native_walk` 一类原生移动模式

## Current State

- `VPet.Plugin.AgentBridge` 仍是唯一桥接实现
- `window.move(dx, dy)` 仍是第一阶段唯一正式移动协议
- 当前 `window.move` 已支持：
  - `style=smart`
  - `style=smooth|walk`
  - `style=snap|teleport`
- 当前默认 quick test 与示例 sequence 都已切到 `style=smart`
- 当前 `sequence/scenario` 仍是：
  - 基于 `delay_ms`
  - 不是基于“完成事件”

## What Was Completed Recently

- 修复 `window.move` 之前同时调用 `DisplayMove()` 与 `MoveWindows(...)` 导致的乱走/乱爬
- quick test 第二轮结果确认：
  - 单独移动已变成纯移动
  - sequence 主要剩“太快、重合”
- 放松两条核心 sequence 的 delay
- 根据新的需求，将移动语义扩到 `style=smart`
- 重新编译并重启标准链路
- 继续完善 `.explore`、协议文档和 quick test catalog

## Validation Evidence

- `quick-tests.json` 中第二轮结果显示：
  - `window.move` 单测：`mixed`，但描述已变成“纯移动不带任何动作”
  - 两条核心 sequence：`mixed`，描述已变成“确实做了，但是有点快，有点重合了”
- 这说明：
  - 协议语义错误已经基本修掉
  - 问题已经收敛到编排门控和节奏层
- `python -m compileall backend-agent/app` 通过
- `.\start-vpet-bridge.ps1` 重新编译并启动通过

## Key Decisions

- `window.move` 不再附带原生 `DisplayMove()`
  - 原因：不能让桥接层位移和 VPet 原生 move 系统同时控制移动
- `window.move.style` 先落地成 `smart / smooth / snap`
  - 原因：先把体感可靠性做对，再考虑更丰富视觉包装
- 暂不承诺“开门闪现”专项视觉
  - 原因：当前仓库里没有稳定确认可直接复用的专项 graph 入口
- 下一步优先做“完成门控”
  - 原因：当前 sequence 的主要缺陷已经不是能力缺失，而是上一步没做完就进下一步

## Important Technical Insight

当前仓库里其实有两套能力：

1. 动作完成回调链
   - `Display(..., EndAction)`
   - `DisplayCEndtoNomal(...)`
   - `DisplayStopForce(...)`

2. 原生 move 系统
   - `walk.left / walk.right`
   - `crawl.left / crawl.right`
   - `fall.left / fall.right`
   - 以及相关 trigger/check/speed/distance 规则

关键结论：

- 原生 move graph 不是普通过场动画，而是“桌宠自己的运动系统”
- 如果桥接层自己位移，就不能再同时让原生 move 系统控制同一次移动
- 所以下一步不能粗暴把 `DisplayMove()` 再塞回来

## Open Questions

- 如何给 sequence 增加最小“完成门控”
- 是否需要新增类似：
  - `wait_for: move_complete`
  - `wait_for: display_normal`
  的编排语义
- 是否值得在下一轮引入 `native_walk` 一类“原生移动模式”
- `move.intent` 是否最终退到纯文档兼容

## Immediate Next Steps

1. 先不要继续广撒网测试
2. 优先设计“完成门控”最小实现
3. 让一条 sequence 至少能做到：
   - 发 `window.move(style=smart)`
   - 等位移完成
   - 再 `bubble.show`
4. 再决定是否把短距离移动升级成更正式的 `native_walk`

## Important Gotchas

- 改插件前必须先停 VPet 再重编，否则 DLL 会锁住
- 当前 quick test 结果是重要真相源，继续优先保存在：
  - `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
- 不要再回到“只靠加大 delay 猜动作完成”的路径上
- 不要把原生 move graph 和桥接显式位移重新绑到同一次移动上

## Related Files

- `.explore/desktop-pet-vpet-body-bridge/state.md`
- `.explore/desktop-pet-vpet-body-bridge/checkpoints.md`
- `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
- `.explore/desktop-pet-vpet-body-bridge/spec/protocol-phase1.md`
- `VPet.Plugin.AgentBridge/AgentBridgePoller.cs`
- `backend-agent/app/services/dev_sequence_orchestrator.py`
- `backend-agent/app/schemas/events.py`
- `backend-agent/app/services/behavior_policy_engine.py`

## Resume Guidance

恢复时按这个顺序读：

1. `.explore/desktop-pet-vpet-body-bridge/state.md`
2. `.explore/desktop-pet-vpet-body-bridge/checkpoints.md`
3. `.explore/desktop-pet-vpet-body-bridge/handoffs/index.md`
4. 本文件
5. `.explore/desktop-pet-vpet-body-bridge/spec/protocol-phase1.md`
6. `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
