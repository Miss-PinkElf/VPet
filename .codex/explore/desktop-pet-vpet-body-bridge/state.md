# 当前状态

## 当前阶段
阶段 3：桥接已完成联调并收敛为 MainPlugin 插件

## 已确认的事实
- 动作入口优先复用 `MW.Main` 现成显示方法与 graph 播放能力。
- 说话入口首选 `Main.Say(...)`。
- 窗口控制入口首选 `MW.Core.Controller.MoveWindows(...)`。
- 长期实现应优先挂在 `MainPlugin` 生命周期中。
- 第一阶段临时内置桥接已收敛到独立插件工程 `VPet.Plugin.AgentBridge/`。
- 当前 POC 通过 HTTP 轮询 `http://127.0.0.1:18787/vpet/events/next` 获取单条事件。
- 插件通过 `MainPlugin.GameLoaded()` 启动轮询器，并在 `EndGame()` 释放。
- `VPet-Simulator.Windows` x64 Debug 已编译通过。
- `VPet.Plugin.AgentBridge.dll` 已输出到 `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/`。
- 已补齐 `backend-agent` 轮询出口和测试页联调链路，默认端口已切到 `18787`。
- 已新增动作/表情映射清单文档：
  - `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`
- 当前桥接扩展支持：
  - `motion.play(idle|move|normal|touch_head|touch_body|sleep|raised|state_one|pinch|thinking)`
  - `mode.switch(thinking|normal)`
  - `emotion.set(emotion|graph)`
  - `bubble.show(text, motion?, expression?, graph?)`
- `bubble.show + touch_head/touch_body/pinch/thinking` 已改为更接近原生的编排：
  `DisplayStopForce(...) -> Say(text, graph, force: true)`。
- `shy -> pinch` 当前是临时近似映射，不是源码级确认的原生表情语义。

## 当前推荐事件
- `bubble.show`
- `motion.play`
- `mode.switch`
- `window.move`

## 下一步
- 在插件化版本上继续验证 `bubble.show + touch_head/touch_body/pinch/thinking` 的实际手感。
- 下一轮补 `window.move`。
- 再补最小状态回传，形成更完整的身体层闭环。

## 最小活跃上下文摘要
专项目标不是解耦整个 VPet，而是先把外部事件桥做通。当前桥接已经插件化，并保留了动作、mode、表情与原生式消息编排；下一步重点是 `window.move` 和最小状态回传。
