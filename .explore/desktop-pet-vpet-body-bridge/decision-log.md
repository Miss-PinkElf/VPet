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

## [2026-03-27] 决策：第一阶段状态快照先扩到“可联调”，不扩到“全状态导出”
- **背景**：`window.move` 闭环打通后，仅有 `left / top / display_name / mode` 已不足以判断组合事件的真实体感。
- **选择**：先补 `right / bottom / display_animat / working_state / work_name / work_type / bubble_visible`。
- **原因**：这些字段都可以从现有公开对象低成本拿到，能显著提升联调可观察性，又不需要深改 `GameCore`。
- **放弃的方案**：继续只保留原最小状态，或直接做更大范围的运行时状态导出。
- **影响**：后续组合联调将优先围绕扩展后的状态快照做判断。

## [2026-03-27] 决策：`move.intent` 降级为 legacy 验证入口
- **背景**：显式 `window.move` 已成为第一阶段主协议，但现有代码里仍保留了 `move.intent` 的运行时兼容。
- **选择**：保留运行时最薄兼容，同时在联调页和流程上明确把它降级为 legacy 入口。
- **原因**：这样既不会立刻打断旧调用，也能避免新一轮联调继续围绕 intent 扩散。
- **放弃的方案**：继续把 `move.intent` 当一等入口，或这轮就直接从代码里彻底删除。
- **影响**：第一阶段所有新联调都应优先使用 `window.move`。

## [2026-03-27] 决策：最小 sequence/scenario 编排下沉到后端
- **背景**：`/dev/control` 上一轮已经有组合按钮，但步骤和延迟都硬编码在浏览器脚本里，难以复用。
- **选择**：增加后端 `sequence/scenario` 入口，由 `backend-agent` 负责预设场景目录和自定义 sequence 的调度。
- **原因**：这比继续堆前端 `wait(...)` 更接近后续行为编排层，也更适合和后端策略逻辑复用。
- **放弃的方案**：继续只在浏览器里拼步骤，或立刻设计更重的编排系统。
- **影响**：后续组合联调和短链路演示应优先走后端 `sequence/scenario` 入口。

## [2026-03-27] 决策：标准 18787 启动链路默认关闭 `uvicorn --reload`
- **背景**：Windows 下 `uvicorn --reload` 会留下 watcher/worker 残留，导致 `18787` 可能继续服务旧版 `/dev/control`。
- **选择**：将 `backend-agent/run-dev.*` 的默认行为改为稳定进程；只有显式 `-Reload` 或 `PET_BACKEND_RELOAD=1` 才启用热重载。
- **原因**：第一阶段联调的优先级是“每次都连到当前后端”，不是热重载体验。
- **放弃的方案**：继续默认 `--reload`，仅靠手工清理旧进程。
- **影响**：`start-vpet-bridge.ps1` 现在能稳定拉起标准 `18787` 链路，并把热重载退回显式调试选项。

## [2026-03-27] 决策：长链路联调先固定为 4 步预设 scenario
- **背景**：最小 2 步 sequence 已经不足以覆盖“思考态 -> 移动 -> 说话 -> 恢复”这类真实身体层编排。
- **选择**：先把后端预设 scenario 扩到两个 4 步样例，并让 `/dev/control` 默认 JSON 也采用 4 步模板。
- **原因**：4 步已经足以验证第一阶段最重要的编排切换，又不会把协议复杂度推高到不可控。
- **放弃的方案**：继续只保留 2 步场景，或立刻上更重的行为树/任务图。
- **影响**：下一轮联调应优先围绕 `thinking-walk-think` 与 `bubble-move-touch-recover` 做真实状态采样。

## [2026-03-28] 决策：显式 `window.move` 与 VPet 原生 move graph 彻底分层
- **背景**：`window.move` 早期实现里同时调用了桥接显式位移和 `DisplayMove()`，把外部控制位移与 VPet 原生 `walk/crawl/fall/climb` 运动系统混在了一起。
- **选择**：`window.move` 只保留桥接显式位移；原生 move graph 不再附带进入这条主路径。
- **原因**：原生 move graph 带方向、速度、边界和触发条件，属于“桌宠自己的运动系统”，不能再被当成桥接层的普通过场动画随手叠加。
- **放弃的方案**：继续让 `DisplayMove()` 跟着 `window.move` 一起触发，或继续靠调 delay 掩盖混用问题。
- **影响**：phase 1 已建立“两类移动”的边界：
  - 桥接位移：`window.move`
  - 原生位移：保留给未来独占移动权模式，不再混入当前主协议

## [2026-03-28] 决策：sequence 从“调 delay”切到“关键步完成门控”
- **背景**：移动协议收口后，两条核心 sequence 的主要问题已经不再是“事件语义错”，而是“上一步没做完就进下一步”。
- **选择**：在后端 sequence 层新增最小 `wait_for` 门控，优先支持：
  - `event_applied`
  - `move_complete`
  - `motion_complete`
- **原因**：当前已有状态回传已经足以支撑最小闭环，没有必要为了 phase 1 立即深改插件或 `GameCore`。
- **放弃的方案**：继续主要依赖全局拉大 `delay_ms`，或直接跳到更重的原生回调体系。
- **影响**：phase 1 的编排模式正式从“固定延迟驱动”升级为“关键步骤显式等待驱动”。

## [2026-03-29] 决策：phase 1 暂不引入 `native_walk`，先把当前门控模式固化
- **背景**：在“桥接位移”和“原生位移”分层之后，理论上可以继续增加 `native_walk` 一类由原生 move system 独占移动权的模式。
- **选择**：当前先不实现 `native_walk`，优先把显式 `window.move` + `wait_for` 门控这条主链做成 phase 1 稳定基线。
- **原因**：真实 GUI 隔离复测已经证明：
  - 三条 `window.move(style=smart)` 单测可通过
  - 两条核心 sequence 可通过
  在这组证据下，继续引入 `native_walk` 只会提前增加协议复杂度。
- **放弃的方案**：在当前主链已可用的情况下，立即把原生走路/爬行能力重新拉回 phase 1 主实现。
- **影响**：后续是否引入 `native_walk`，将不再由“当前链路能不能跑”驱动，而只由“更长 story sequence 是否确实需要独占原生移动权”驱动。

## [2026-03-29] 决策：phase 1 增加最小事件关联字段，而不是继续扩更多桌宠工作态
- **背景**：当前 4 步核心 sequence 已经能跑，但一旦进入更长链路，单靠 `last_event_type / last_event_at` 很难把“后端发的第几步”和“VPet 实际消费到的哪一步”稳定对上，尤其是在同一条 sequence 里出现两次 `bubble.show` 这类重复事件类型时。
- **选择**：在 phase 1 增加最小关联字段：
  - 事件侧：`event_id / sequence_name / step_index`
  - 状态侧：`last_event_id / last_sequence_name / last_step_index`
- **原因**：这组字段可以在不深改 `GameCore` 的前提下，把后端编排步骤和前端执行消费建立一一对应关系。
- **放弃的方案**：继续只依赖 `last_event_type / last_event_at` 猜测当前步骤，或为了关联问题去提前扩更多桌宠内部工作态。
- **影响**：后续更长的 story sequence 联调将优先围绕“事件关联 + 完成门控”推进，而不是继续补大量状态字段。

## [2026-03-30] 决策：展示层全控扩展应采用“catalog + graph.play + behavior.invoke”分层方案
- **背景**：本轮源码级梳理确认：当前桥接直接暴露的 `motion.play / emotion.set / mode.switch` 白名单，只覆盖了 `VPet` 展示层真实能力的一小部分；而 `Main.Display(string name, AnimatType, ...)` 与 `Main.Say(text, graphname, force)` 已经说明，展示层大部分资源本体上都可被点播。
- **选择**：将展示层全控扩展分为三层：
  - `graph.catalog`：导出当前角色真实 graph 目录
  - `graph.play`：按 graph 名和动画阶段直接点播
  - `behavior.invoke`：封装贴边、探头、摸头、拖拽等复杂行为
- **原因**：这样能把“资源点播”和“行为语义”严格分离，既不破坏 phase 1 最小协议，也能避免继续扩大手写白名单带来的失真和维护成本。
- **放弃的方案**：继续只扩大 `motion.play / emotion.set` 的硬编码 switch，把所有 graph 和行为都塞进少量语义字段。
- **影响**：phase 1 的正式承诺边界保持不变；若进入下一阶段控制面扩展，应优先从 `graph.catalog` 开始，而不是先加更多 alias。
