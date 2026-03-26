# 当前状态

## 当前阶段
阶段 1：架构冻结与文档沉淀

## 已确认的事实
- 当前 VPet 仓库已经可以在本机启动。
- `VPet-Simulator.Windows/MainWindow.cs` 中存在 `RunAction(string action)`，可作为低成本动作入口。
- `VPet-Simulator.Core/Display/MainLogic.cs` 中存在 `Main.Say(...)` 和 `Main.SayRnd(...)`，可作为说话入口。
- `VPet-Simulator.Core/Handle/IController.cs` 与 `VPet-Simulator.Windows/Function/MWController.cs` 提供窗口移动控制能力。
- `VPet-Simulator.Windows.Interface/MainPlugin.cs` 提供插件生命周期，适合作为长期桥接层载体。
- `VPet-Simulator.Windows.Interface/TalkBox.xaml.cs` 中已有 `DisplayThink()` 等思考态复用入口。
- 当前仓库里没有现成的 `openspec/changes/desktop-pet-companion-roadmap/tasks.md`，本轮先以 `.codex/explore` 和 `docs/agent-desktop-pet/migration` 为主要记录真相源。
- `.codex` 目录带有显式拒绝写入 ACL，记录文件写入需要提权。

## 工作假设
- 第一阶段不需要重构深层 GameCore，也能验证路线成立。
- 第一阶段只要打通外部事件到动作/气泡，就足够证明“Python 大脑 -> VPet 身体层”是可行的。
- POC 可以先内置桥接，验证通过后再回收为 `MainPlugin` 插件。

## 待解决的问题
- 第一版桥接具体采用内置轮询还是直接插件化开局。
- Python 后端第一版用 HTTP 轮询还是 WebSocket 推送。
- 插件项目的输出目录和 MOD 壳的组织方式如何最省事。

## 下一步
- 让 AI 按 migration 文档实现第一阶段最小桥接 POC。
- 第一版只做 `bubble.show`、`motion.play(idle)`、`motion.play(move)`。
- 验证通过后再收敛为插件。

## 最小活跃上下文摘要
当前方向已冻结：VPet 只做身体层，Python 做大脑。优先用现有动作入口和说话入口做最小事件桥，不先重构深层逻辑。
