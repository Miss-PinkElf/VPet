# Handoff: Native Move Direction Paused

## Session Metadata
- Created: 2026-03-31
- Project: `E:\Learn\Vs\Code\VPet`
- Mission: `.explore/desktop-pet-vpet-body-bridge`
- Branch: `shuowang/dev-vpet`
- Continues from: `2026-03-31-015-phase1-sequence-acceptable-walk-next.md`
- Session focus: 在不改 `window.move(dx, dy)` 正式语义的前提下，探索原生 move system；完成第一版 `native.move.direction` 后，因结果仍不够可控，当前决定暂停此分支，只更新文档与恢复入口

## Current State Summary

当前 mission 的主结论已经分成三块：

1. phase 1 最小正式协议仍然稳定：
   - `bubble.show`
   - `motion.play`
   - `mode.switch`
   - `emotion.set`
   - `window.move`
2. `window.move(style=smart)` 已确认不再继续深抠：
   - 真实结果仍是纯拖窗
   - 无法自然带出原生走路动作层
3. 原生 move system 已确认独立存在，但当前探索分支先暂停：
   - `motion.play(move)` 能进入原生 move system
   - 第一版 `native.move.direction` 已实现
   - 但真实结果显示当前 move 选择策略过宽，方向约束仍会被贴边 `climb.*` move 抢占

## What Was Confirmed

- `motion.play(move)` 不是纯位移：
  - 会进入原生 `walk/crawl/climb/fall` move graph
- `DisplayMove()` 的本体语义是：
  - 从 `GraphConfig.Moves` 里随机起点遍历
  - 找到第一个 `Triggered(main)` 为真的 move
  - 再执行 `move.Display(main)`
- 原生控制台里已存在更窄的方向 helper：
  - 左：`SpeedX < 0 && Checked(...)`
  - 右：`SpeedX > 0 && Checked(...)`
  - 上：`SpeedY < 0 && Checked(...)`
  - 下：`SpeedY > 0 && Checked(...)`
- 已据此实现第一版 dev-only：
  - `native.move.direction(left|right|up|down)`

## Latest Real Test Results

`quick-tests.json` 当前已回写：

- `move-smart-medium-right-80 = fail`
  - 仍是纯位移，机械滑块感，没有动作层
- `motion-native-move = mixed`
  - 会走、会爬、会贴墙爬，甚至可能斜飞
- `native-move-left = fail`
  - 会先到顶部，再贴顶向左爬
- `native-move-right = fail`
  - 会先到顶部，再贴顶向右爬
- `native-move-up = fail`
  - 会先到左边，再贴左向上爬
- `native-move-down = fail`
  - 会先到左边，再贴左向下爬

## Root Cause Summary

第一版 `native.move.direction` 失败的直接根因已经明确：

- 当前实现只按：
  - `SpeedX / SpeedY`
  - `Checked(...)`
  做最小筛选
- 但 `move.Display(main)` 在 `LocateType` 存在时，会先 reposition 到对应边缘
- 所以当前方向入口会被带 `LocateType` 的 `climb.*` move 抢占
- 当前问题不是协议名字错，而是 move 选择优先级不够严格

## Critical Files

- `.explore/desktop-pet-vpet-body-bridge/state.md`
- `.explore/desktop-pet-vpet-body-bridge/decision-log.md`
- `.explore/desktop-pet-vpet-body-bridge/checkpoints.md`
- `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
- `backend-agent/app/schemas/events.py`
- `backend-agent/app/services/behavior_policy_engine.py`
- `backend-agent/app/api/routes/dev_control.py`
- `VPet.Plugin.AgentBridge/AgentBridgeEvent.cs`
- `VPet.Plugin.AgentBridge/AgentBridgePoller.cs`
- `VPet-Simulator.Core/Display/MainDisplay.cs`
- `VPet-Simulator.Core/Graph/GraphHelper.cs`
- `VPet-Simulator.Windows/WinDesign/winConsole.xaml.cs`

## Validation Evidence

- `python -m compileall backend-agent/app` 通过
- `quick-tests.json` 通过 JSON 解析校验
- 插件完整 `dotnet build` 曾因：
  - `mod/1200_AgentBridge/plugin/VPet.Plugin.AgentBridge.dll`
  被运行中的 VPet 锁住而无法完成复制
- 这不影响当前“文档已收口”的状态，但若恢复实现，仍需先停掉 VPet 再重新 build

## Decisions Made

- 当前不再继续微调 pure `window.move(style=smart)`
- 当前不把原生 `DisplayMove()` 重新绑回 `window.move`
- `native.move.direction` 路线保留，但当前先暂停，不继续往下修
- 若未来恢复此分支，下一步应优先收紧 move 选择优先级，而不是换协议字面量

## Immediate Next Steps

恢复时只做以下判断，不要重新做大范围路线比较：

1. 先决定是否真的要重开 native move 分支
2. 如果要重开，先修 `MoveNativeDirection(...)` 的选择优先级：
   - 方向匹配
   - `Triggered(main)` 优先于仅 `Checked(...)`
   - 普通 `walk/crawl` 优先于带 `LocateType` 的 `climb/fall`
3. 如果暂时不重开，就继续把 native move 保持为 paused 分支，不影响 phase 1 主协议

## Potential Gotchas

- 不要把当前 `native.move.direction` 的失败误判成“原生 move system 完全没价值”
- 不要因为当前分支暂停，就把 `DisplayMove()` 重新绑回 `window.move`
- 不要把 dev-only 原生 move 探索直接升级成 phase 1 正式协议
- 若要重新 build 插件，先停掉 VPet，否则 DLL 仍会被锁住

## Resume Guidance

恢复时优先打开：

1. `.explore/desktop-pet-vpet-body-bridge/handoffs/2026-03-31-016-native-move-direction-paused.md`
2. `.explore/desktop-pet-vpet-body-bridge/state.md`
3. `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
4. `VPet.Plugin.AgentBridge/AgentBridgePoller.cs`
5. `VPet-Simulator.Core/Display/MainDisplay.cs`
6. `VPet-Simulator.Core/Graph/GraphHelper.cs`
