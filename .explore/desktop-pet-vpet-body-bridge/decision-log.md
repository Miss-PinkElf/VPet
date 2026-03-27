# 决策日志

## [2026-03-27] 决策：VPet 固定为身体层，Python backend-agent 固定为大脑
- **背景**：毕设主线需要一个高桌宠感执行层，同时又要保留 Python 侧的对话、记忆与策略能力。
- **选择**：保留 VPet 的窗口行为和动画表现，把高层决策外移给 Python。
- **原因**：VPet 的优势在于身体层表现，不在于现有内部业务逻辑。
- **放弃的方案**：继续 Electron 前端主线、全面重构 VPet、先深改 `GameCore`。
- **影响**：桥接优先，解耦和底层重构延后。

## [2026-03-27] 决策：先 POC，再收敛到 `MainPlugin`
- **背景**：一开始最主要风险不是结构优雅，而是链路能不能跑通。
- **选择**：先做最小桥接 POC，联调稳定后再收敛成插件。
- **原因**：先证明链路，再回收结构，风险最小。
- **放弃的方案**：直接从零设计完整插件架构后再验证。
- **影响**：当前已完成插件化收敛，后续只在插件版本上继续迭代。

## [2026-03-27] 决策：`bubble.show + touch_head/touch_body/pinch/thinking` 走更接近原生的编排
- **背景**：简单地“先播 motion，再 `Say(...)`”会和 VPet 显示状态机打架，动作没放完就被说话态覆盖。
- **选择**：对这些原生交互动作优先走 `DisplayStopForce(...) -> Say(text, graph, force: true)`。
- **原因**：这更接近 VPet 自己的动作+说话编排方式，观感稳定得多。
- **放弃的方案**：固定延迟后再说话、完全禁止 `bubble.show + motion`。
- **影响**：当前测试页可以直接验证这些组合事件体感。

## [2026-03-27] 决策：mission 工作区迁移到仓库根目录 `.explore/`
- **背景**：`context-budget-explore` 已升级到以 `.explore/` 为统一工作区的新规范。
- **选择**：将本专项记录迁移到 `.explore/desktop-pet-vpet-body-bridge/`。
- **原因**：后续需求、探索、实施、handoff 都要走同一套标准结构。
- **放弃的方案**：继续把新增记录写回 `.codex/explore/`。
- **影响**：新的真相源已经切换到 `.explore/desktop-pet-vpet-body-bridge/`。

## [2026-03-27] 决策：窗口移动协议收敛为 `window.move(dx, dy)`
- **背景**：测试页里原有 `move.intent` 没有接到 VPet，且 `follow_cursor` 一类 intent 语义过虚。
- **选择**：正式引入显式 `window.move(dx, dy)`，并仅保留 `move.intent` 的最薄兼容层。
- **原因**：VPet 当前最稳定的移动入口就是 `MW.Core.Controller.MoveWindows(...)`，显式位移协议最直接、最可验证。
- **放弃的方案**：继续围绕 `move.intent` 扩语义，或为了移动协议去深改 `GameCore`。
- **影响**：测试页、后端 schema、插件消费逻辑都统一转向显式位移协议。
