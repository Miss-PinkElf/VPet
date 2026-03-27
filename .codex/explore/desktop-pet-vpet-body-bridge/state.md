# 当前状态

## 当前阶段
阶段 2：最小桥接 POC 已实现并编译通过

## 已确认的事实
- 动作入口首选 `MainWindow.RunAction(string action)`。
- 说话入口首选 `Main.Say(...)`。
- 窗口控制入口首选 `MW.Core.Controller.MoveWindows(...)`。
- 长期实现应优先挂在 `MainPlugin` 生命周期中。
- 第一阶段最小桥接代码已经新增到 `VPet-Simulator.Windows/AgentBridge/`。
- 当前 POC 通过 HTTP 轮询 `http://127.0.0.1:18787/vpet/events/next` 获取单条事件。
- 当前已实现事件：
  - `bubble.show` -> `Main.Say(text, force: true)`
  - `motion.play(name=idle)` -> `RunAction("DisplayIdel")`
  - `motion.play(name=move)` -> `RunAction("DisplayMove")`
- 轮询器在 `MainWindow.GameLoaded()` 之后启动，并在主窗口关闭时释放。
- `VPet-Simulator.Windows` x64 Debug 已编译通过。
- 已补齐 `backend-agent` 轮询出口和测试页联调链路，默认端口已切到 `18787`。
- 已新增动作/表情映射清单文档：
  - `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`
- 当前桥接扩展支持：
  - `motion.play(idle|move|normal|touch_head|touch_body|sleep|raised|state_one|pinch|thinking)`
  - `mode.switch(thinking|normal)`
  - `emotion.set(emotion|graph)`
  - `bubble.show(text, motion?, expression?, graph?)`
- `shy -> pinch` 当前是临时近似映射，不是源码级确认的原生表情语义。

## 当前推荐事件
- `bubble.show`
- `motion.play`
- `mode.switch`
- `window.move`

## 下一步
- 本地启动 VPet 与 `backend-agent`，在 `/dev/control` 验证 `say / motion / mode / emotion` 组合事件。
- 运行联调通过后，把当前 `AgentBridge` 目录下的实现收敛成 `MainPlugin` 插件。
- 下一轮再补 `window.move`、`mode.switch` 或最小状态回传。

## 最小活跃上下文摘要
专项目标不是解耦整个 VPet，而是先把外部事件桥做通。当前桥接已经支持动作、mode 和表情映射，下一步是验证联调体验并继续收敛到插件。
