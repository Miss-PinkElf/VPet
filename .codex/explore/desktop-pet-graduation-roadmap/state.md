# 当前状态

## 当前阶段
阶段 2：第一阶段最小桥接 POC 已落地，等待本地运行联调

## 已确认的事实
- 当前 VPet 仓库已经可以在本机启动。
- `VPet-Simulator.Windows/MainWindow.cs` 中存在 `RunAction(string action)`，可作为低成本动作入口。
- `VPet-Simulator.Core/Display/MainLogic.cs` 中存在 `Main.Say(...)` 和 `Main.SayRnd(...)`，可作为说话入口。
- `VPet-Simulator.Core/Handle/IController.cs` 与 `VPet-Simulator.Windows/Function/MWController.cs` 提供窗口移动控制能力。
- `VPet-Simulator.Windows.Interface/MainPlugin.cs` 提供插件生命周期，适合作为长期桥接层载体。
- `VPet-Simulator.Windows.Interface/TalkBox.xaml.cs` 中已有 `DisplayThink()` 等思考态复用入口。
- 当前仓库里没有现成的 `openspec/changes/desktop-pet-companion-roadmap/tasks.md`，本轮先以 `.codex/explore` 和 `docs/agent-desktop-pet/migration` 为主要记录真相源。
- 第一阶段最小桥接 POC 已在 `VPet-Simulator.Windows/AgentBridge/` 落地，当前包含 `AgentBridgeConfig`、`AgentBridgeEvent`、`AgentBridgePoller`。
- 桥接当前通过 HTTP 轮询 `http://127.0.0.1:18787/vpet/events/next` 拉取单条事件，支持后端主动推送的单条事件消费。
- 桥接启动时机已经接到 `MainWindow.GameLoaded()` 之后，且只在主窗口启动；关闭窗口时会释放轮询器。
- 新增代码已通过 `VPet-Simulator.Windows` 的 x64 Debug 编译。
- 现有 `backend-agent` 已补齐 `GET /vpet/events/next`，并保留原有 `/dev/control` 测试页。
- 已输出动作/表情映射清单：`docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`。
- 当前桥接已扩展支持：
  - `motion.play(idle|move|normal|touch_head|touch_body|sleep|raised|state_one|pinch|thinking)`
  - `mode.switch(thinking|normal)`
  - `emotion.set`
  - `bubble.show` 附带 `motion` / `expression` / `graph`

## 工作假设
- 第一阶段不需要重构深层 GameCore，也能验证路线成立。
- 第一阶段只要打通外部事件到动作/气泡，就足够证明“Python 大脑 -> VPet 身体层”是可行的。
- POC 可以先内置桥接，验证通过后再回收为 `MainPlugin` 插件。

## 待解决的问题
- `window.move` 和最小状态回传准备在哪一轮补齐。
- `emotion -> graph` 是否要继续做运行时导出，而不是只靠源码确认与人工映射。
- 第二阶段插件化时，MOD 壳目录和输出拷贝流程如何最省事。

## 下一步
- 本地运行 VPet 并用一个最小 Python/HTTP mock backend 验证 `bubble.show`、`motion.play(idle)`、`motion.play(move)` 三条链路。
- 用 `backend-agent/dev/control` 实测“消息 + 动作 + 表情”组合事件，例如 `bubble.show + touch_body + shy`。
- 如果运行联调通过，把当前主工程内置桥接收敛为 `MainPlugin` 插件项目。
- 再补 `window.move` 与最小状态回传，形成“Python 大脑 -> VPet 身体层”最小闭环。

## 最小活跃上下文摘要
当前方向已冻结：VPet 只做身体层，Python 做大脑。第一阶段桥接已经不再只有 `say/idle/move`，而是扩展到了动作、mode 和表情映射；当前重点是本地联调和后续插件化收敛。
