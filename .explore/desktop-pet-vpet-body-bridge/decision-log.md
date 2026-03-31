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

## [2026-03-31] 决策：6 步 story sequence 暴露的是 phase 1 完成门控与过渡体验问题，不是现在就去做全量动画映射
- **背景**：你在 `quick-tests.json` 中回写 `sequence-think-speak-move-touch-speak-recover = mixed`，备注为“动作还没有做完，就继续下一个，有一点点突兀”；同时你继续强调走路体感生硬，以及不应再靠人工扩大所有动画映射。
- **选择**：当前继续留在 phase 1，优先收口：
  - 更长 story sequence 的完成门控
  - `window.move` 的走路体感问题
  不把“所有动画做映射”当成当前阻塞修复手段。
- **原因**：这次真实结果说明，当前主要问题是“过渡不自然”和“动作结束判断不够稳”，而不是“事件关联字段失效”或“现有白名单数量不够”。
- **放弃的方案**：因为 6 步链路仍有突兀，就立刻跳到 phase 2 去扩 `graph.catalog / graph.play / behavior.invoke`，或者继续人工堆更多 `motion / emotion` alias。
- **影响**：下一轮如果开始实现，应先修 phase 1 的门控/移动体验；全量动画暴露与映射保持为 phase 2 专题。

## [2026-03-31] 决策：先增强现有 `motion_complete`，不新增新的 phase 1 门控类型
- **背景**：6 步 story sequence 的主要问题收口为“`touch_head` 刚离开动作态就切进第二次 `bubble.show`，体感仍然突兀”。
- **选择**：继续复用现有 `wait_for=motion_complete`，但把其完成条件增强为：
  - 先看到动作态
  - 再等待离开动作态后稳定一小段时间
  - 同时把 6 步 story sequence 中该步的 `settle_ms` 拉大
- **原因**：这是最小改动，能优先验证问题是否只是“动作结束判断太激进”，而不需要立刻新增新的协议字面量或扩更多状态字段。
- **放弃的方案**：本轮直接新增新的 `wait_for` 类型，或为了过渡问题提前引入原生回调体系。
- **影响**：phase 1 的协议边界不变，但 `motion_complete` 的运行时语义变得更保守，更适合 story-like sequence。

## [2026-03-31] 决策：对更长 story sequence 增加 `motion_recovered`，作为 `motion_complete` 之上的恢复态门控
- **背景**：在增强 `motion_complete` 并拉大 `settle_ms` 后，你的真实反馈变成“好了一点点，不是那么突兀了”。这说明方向正确，但仅靠“动作退出后短暂稳定”仍不够。
- **选择**：为 `motion.play` 增加新的 phase 1 门控：
  - `wait_for=motion_recovered`
  它在 `motion_complete` 之后，继续等待回到更稳定的展示态，再放行下一步。
- **原因**：这样可以把“动作已结束”和“已经适合切到下一段叙事”明确区分开，而不需要现在就引入原生回调或跳到 phase 2。
- **放弃的方案**：继续只调 `settle_ms`，或把“恢复态问题”转嫁成动画全映射问题。
- **影响**：phase 1 的门控集合从：
  - `event_applied / move_complete / motion_complete`
  扩展为：
  - `event_applied / move_complete / motion_complete / motion_recovered`
  其中 `motion_recovered` 优先用于更长的 story-like sequence。

## [2026-03-31] 决策：将 6 步 story sequence 视为 phase 1 已收口到可接受范围，后续主焦点转向走路体感
- **背景**：你在继续收口尾段两步后给出最新真实反馈：“还行流畅度可以，只有一点点卡顿，可以接受”。
- **选择**：不再继续围绕 `sequence-think-speak-move-touch-speak-recover` 做高频微调，将其视为 phase 1 的可接受基线；下一步主焦点转向 `window.move(style=smart)` 的走路体感问题。
- **原因**：当前这条 6 步 chain 已不再构成 phase 1 的主要阻塞，继续投入只会边际收益递减。
- **放弃的方案**：继续围绕这条 chain 做无止境的尾段微调。
- **影响**：phase 1 当前主要剩余体验问题收口为“走路体感生硬”；phase 2 的动画全映射仍保持独立主题。

## [2026-03-31] 决策：phase 1 的 `window.move(style=smart)` 继续保持纯显式位移，但从线性切片改为 eased 位移曲线
- **背景**：当前 `smart move` 虽然已经可控，但插件实现本质上只是固定步数 + 固定节奏的 `MoveWindows(...)` 线性切片，走位体感容易像机械滑块。
- **选择**：不把 `DisplayMove()` 或原生 `walk/crawl/fall/climb` move graph 重新绑回 `window.move`；先把 `smart` 改为“距离感知总时长 + eased 累进位移”的纯位移实现。
- **原因**：当前问题属于 phase 1 纯显式位移路径的节奏曲线过硬，而不是正式协议边界需要回退混入原生 move system。
- **放弃的方案**：重新绑定 `DisplayMove()` 掩盖体感问题，或因为体感仍不够自然就提前跳到 phase 2 控制面扩展。
- **影响**：phase 1 继续维持“`window.move(dx, dy)` 与原生 move system 严格分层”；如果 eased `smart` 仍不够，再单独讨论与 `window.move` 正式语义分开的原生 walk 能力。

## [2026-03-31] 决策：停止继续微调 pure `window.move(style=smart)`，转向独立的原生 walk 能力探索
- **背景**：你对 eased `smart move` 的最新真实反馈是“其实还是单纯的移动，机械滑块感，没有调用任何动作”。这说明问题已经不是 pure move 曲线是否够顺，而是整条路径没有动作层。
- **选择**：不再继续优先微调 pure `window.move` 的曲线；下一步改为探索一个与 `window.move(dx, dy)` 正式语义分开的原生 walk / native move 能力入口。
- **原因**：只要还停留在 `MoveWindows(...)` 纯位移层，再怎么调 easing 也不会自然出现原生 walk 动作表现。
- **放弃的方案**：继续在 pure `window.move` 上反复调步数、时长和 easing，或直接把 `DisplayMove()` 偷偷并回 `window.move`。
- **影响**：phase 1 的正式移动协议边界保持不变；后续如果实现原生 walk，也应先作为独立探索入口，而不是改写 `window.move` 的既有语义。

## [2026-03-31] 决策：原生 walk 的第一轮探索先复用现有 `motion.play(move)`，不先扩新协议字面量
- **背景**：桥接当前已经存在 `motion.play(move) -> Main.DisplayMove()` 这条独立路径；而用户最新反馈已经确认 pure `window.move` 再调曲线也不会产生动作层。
- **选择**：先把 `motion.play(move)` 作为 dev-only 的原生 move system 探索入口，验证它是否足以承接“带动作的走路”体验；暂不先加新的协议字面量。
- **原因**：这是当前成本最低、边界最清晰的探索方式，既不破坏 phase 1 正式协议，也不会把原生 move system 偷偷绑回 `window.move`。
- **放弃的方案**：还没验证现有入口前，就先设计新的 native walk 事件名或新的 dx/dy 协议。
- **影响**：下一轮真实联调焦点应转到 `motion.play(move)`；只有当它不足以承接原生 move 探索时，才需要继续扩 dev-only 入口。

## [2026-03-31] 决策：`motion.play(move)` 已证明原生 move system 可独立进入，但当前仍是环境驱动、非确定性入口
- **背景**：你对 `motion.play(move)` 的最新真实反馈是：会走、会爬、会贴墙爬，甚至可能斜着飞行。这与角色 `vup.lps` 中 `walk/crawl/climb/fall` 多组 move graph 及其边缘/方向触发条件一致。
- **选择**：将 `motion.play(move)` 视为“原生 move system 已被独立触发”的已验证证据，但不把它当成当前已经足够稳定的正式控制入口。
- **原因**：这条路径当前证明了“动作层确实存在且与 `window.move` 分层”，但同时也暴露出它受边缘状态、方向、兼容 move 切换规则影响，天然不是单一确定动作。
- **放弃的方案**：把当前 `motion.play(move)` 的观感直接等同于“已经得到一个稳定可控的 native walk API”。
- **影响**：下一步应先做源码级缩圈，判断能否在不进入 phase 2 的前提下，为原生 move system 增加更窄、更可控的 dev-only 约束入口。

## [2026-03-31] 决策：如果继续探索原生 move system，优先顺序应是 `native.move.direction -> native.move.graph`
- **背景**：本轮源码探索确认两件事：
  - `DisplayMove()` 实际是从 `GraphConfig.Moves` 中随机挑选当前 `Triggered(...)` 为真的 move
  - 原生控制台已经存在按 `SpeedX / SpeedY` 方向筛选 `move.Display(main)` 的调试入口
- **选择**：后续若继续做 dev-only 原生 move 能力，先考虑两层：
  - 第一层：`native.move.direction`
  - 第二层：`native.move.graph`
- **原因**：
  - `direction` 最贴近现有控制台与源码结构，改动最小
  - `graph` 更可控，但角色资源相关性更强，应放在更明确需要时再做
- **放弃的方案**：一上来就把原生 move system 做成新的正式 phase 1 协议，或继续只保留 `motion.play(move)` 这种随机入口
- **影响**：下一轮若开始实现，应优先考虑一个 dev-only 的最小方向入口，而不是立即扩成完整的 graph catalog / play 体系。

## [2026-03-31] 决策：先实现 dev-only `native.move.direction`，暂不直接上 `native.move.graph`
- **背景**：原生控制台现成就有按 `SpeedX / SpeedY` 方向筛选 move 的 helper，这已经足够支撑第一轮“更可控而不改正式协议”的实验。
- **选择**：先实现 `native.move.direction(left|right|up|down)`，只做最小方向约束；`native.move.graph` 暂缓。
- **原因**：这是当前最小、最稳、最贴近现有源码的收口点，能先验证“方向约束是否已经足够有用”。
- **放弃的方案**：在还没证明方向约束有价值前，就先加按 graph 名精确控制入口。
- **影响**：下一轮真实联调的重点应变为四个方向单测及其边缘表现，而不是继续围绕 `motion.play(move)` 的随机入口做判断。

## [2026-03-31] 决策：保留 `native.move.direction` 路线，但下一轮先收紧 move 选择优先级
- **背景**：四条 `native.move.direction` 真实测试均未通过方向预期：左右都会先冲到顶部再贴顶爬，上下都会先冲到左边再贴左爬。
- **选择**：不废弃 `native.move.direction`；下一轮优先修改 `MoveNativeDirection(...)` 的 move 选择优先级：
  - 方向匹配
  - `Triggered(main)` 优先于仅 `Checked(...)`
  - 普通 walk/crawl 优先于带 `LocateType` 的 climb/fall
- **原因**：当前失败已经明确说明问题在“筛选过宽导致贴边 move 抢占”，不是 `native.move.direction` 这个 dev-only 入口本身没有价值。
- **放弃的方案**：因为第一版 direction 失败，就立刻废弃方向入口，或直接跳到新的协议字面量。
- **影响**：`native.move.direction` 仍值得保留并继续收口；`native.move.graph` 继续作为下一层备用增强，而不是立刻替代它。

## [2026-03-31] 决策：native move 分支当前暂停，主线切回 phase 1 正式协议
- **背景**：第一版 `native.move.direction` 已完成实现、真实测试与根因定位；当前用户明确表示“先不管这个了，回头做，先更新文档，做好记录”。
- **选择**：保留现有探索记录与暂停 handoff，不继续 native move 分支的实现或联调；当前主线切回 phase 1 正式协议与稳定基线维护。
- **原因**：当前 native move 分支的技术状态已经足够形成清晰恢复点，继续推进不再是当前回合目标。
- **放弃的方案**：在用户明确要求暂停后，继续沿 native move 分支往下修。
- **影响**：后续若要恢复 native move，直接从 `2026-03-31-016-native-move-direction-paused.md` 继续；未恢复前，不把它视作当前主线阻塞。
