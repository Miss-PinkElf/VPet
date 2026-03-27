# 当前状态

## 当前阶段
阶段 2：第一阶段最小桥接 POC 已联调并收敛为插件，准备继续补身体层控制

## 已确认的事实
- 当前 VPet 仓库已经可以在本机启动。
- `VPet-Simulator.Windows/MainWindow.cs` 中存在 `RunAction(string action)`，可作为低成本动作入口。
- `VPet-Simulator.Core/Display/MainLogic.cs` 中存在 `Main.Say(...)` 和 `Main.SayRnd(...)`，可作为说话入口。
- `VPet-Simulator.Core/Handle/IController.cs` 与 `VPet-Simulator.Windows/Function/MWController.cs` 提供窗口移动控制能力。
- `VPet-Simulator.Windows.Interface/MainPlugin.cs` 提供插件生命周期，适合作为长期桥接层载体。
- `VPet-Simulator.Windows.Interface/TalkBox.xaml.cs` 中已有 `DisplayThink()` 等思考态复用入口。
- 当前仓库里没有现成的 `openspec/changes/desktop-pet-companion-roadmap/tasks.md`，本轮先以 `.codex/explore` 和 `docs/agent-desktop-pet/migration` 为主要记录真相源。
- 第一阶段最小桥接已收敛为独立插件工程 `VPet.Plugin.AgentBridge/`，并产出到 `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/`。
- 桥接当前通过 HTTP 轮询 `http://127.0.0.1:18787/vpet/events/next` 拉取单条事件，支持后端主动推送的单条事件消费。
- 桥接现由 `MainPlugin.GameLoaded()` 启动，`EndGame()` 释放，不再内置在主工程生命周期钩子里。
- 新增代码已通过 `VPet-Simulator.Windows` 的 x64 Debug 编译。
- 现有 `backend-agent` 已补齐 `GET /vpet/events/next`，并保留原有 `/dev/control` 测试页。
- 已输出动作/表情映射清单：`docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`。
- 当前桥接已扩展支持：
  - `motion.play(idle|move|normal|touch_head|touch_body|sleep|raised|state_one|pinch|thinking)`
  - `mode.switch(thinking|normal)`
  - `emotion.set`
  - `bubble.show` 附带 `motion` / `expression` / `graph`
- 其中 `bubble.show + touch_head/touch_body/pinch/thinking` 已改为更接近 VPet 原生的动作+说话编排。

## 工作假设
- 第一阶段不需要重构深层 GameCore，也能验证路线成立。
- 第一阶段只要打通外部事件到动作/气泡，就足够证明“Python 大脑 -> VPet 身体层”是可行的。
- POC 可以先内置桥接，验证通过后再回收为 `MainPlugin` 插件。

## 待解决的问题
- `window.move` 和最小状态回传准备在哪一轮补齐。
- `emotion -> graph` 是否要继续做运行时导出，而不是只靠源码确认与人工映射。
- 第二阶段插件化时，MOD 壳目录和输出拷贝流程如何最省事。

## 下一步
- 在插件化版本上继续验证组合事件体感。
- 补 `window.move`。
- 再补最小状态回传，形成“Python 大脑 -> VPet 身体层”更完整闭环。

## 最小活跃上下文摘要
当前方向已冻结：VPet 只做身体层，Python 做大脑。第一阶段桥接已经完成插件化收敛；当前重点从“桥能否跑通”转到“继续补身体层控制能力”，尤其是 `window.move` 和最小状态回传。
