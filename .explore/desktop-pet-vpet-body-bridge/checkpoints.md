# Checkpoints

## Checkpoint 1 - 2026-03-27 Mission Migration

### 当前阶段
- 阶段 3：桥接已联调并收敛为 `MainPlugin` 插件

### 本轮完成内容
- 将桥接实现从主工程内置目录收敛到 `VPet.Plugin.AgentBridge/`
- 补齐 `mod/1200_AgentBridge/` 插件壳
- 把旧 `.codex/explore/desktop-pet-vpet-body-bridge/` 记录迁移到新的 `.explore/desktop-pet-vpet-body-bridge/` 结构

### 本轮决策与原因
- 决策：新 truth source 切换到 `.explore/desktop-pet-vpet-body-bridge/`
- 原因：统一适配新的 `context-budget-explore` 工作流，避免后续记录继续分散

### 本轮沉淀经验
- 插件化收敛完成后，应立刻切换 mission 真相源，避免“代码和记录已经迁了，文档还留旧目录”的双轨状态

### 待解决问题
- `window.move`
- 最小状态回传
- `emotion -> graph` 的长期确认方式

### 下一步
- 在插件化版本上继续验证组合事件体感
- 补 `window.move`

### 可以从活跃上下文中移除的内容
- 旧 `.codex/explore/desktop-pet-vpet-body-bridge/` 作为真相源的身份
- “是否还要继续内置桥接”的反复讨论

## Checkpoint 2 - 2026-03-27 Window Move + State Loop

### 当前阶段
- 阶段 3：插件桥接已补齐显式窗口位移与最小状态回传

### 本轮完成内容
- 将测试页未接线的移动协议收敛为显式 `window.move(dx, dy)`
- 在 `VPet.Plugin.AgentBridge` 中补上 `window.move` 到 `MW.Core.Controller.MoveWindows(...)` 的映射
- 保留 `move.intent` 的最薄边界兼容，仅支持可明确映射到边界位移的 intent
- 补上 `POST /vpet/state` 与 `GET /api/dev/state`
- 让 `/dev/control` 可直接展示最新 VPet 状态回传
- 完成一次真实联调验证：`dx=120, dy=-40` 导致状态增量 `+120 / -40`

### 本轮决策与原因
- 决策：不再继续围绕 `move.intent` 扩语义，正式以 `window.move(dx, dy)` 作为第一阶段移动协议
- 原因：`move.intent` 语义过虚，难以稳定映射到 VPet 的具体窗口位移能力

### 本轮沉淀经验
- 对桌宠窗口控制这类底层能力，协议要尽量显式，优先传具体位移而不是抽象意图
- 最小状态回传一旦接通，联调就可以从“靠肉眼猜”切到“看前后状态差值”
- 本地联调前要确认运行中的 `Setting.lps` 已启用目标 mod，否则很容易误判为代码未生效

### 待解决问题
- 是否继续扩最小状态字段
- `move.intent` legacy 兼容是否要保留
- `emotion -> graph` 长期映射如何收敛

### 下一步
- 继续验证 `window.move` 与其他动作/说话事件的组合体感
- 评估状态回传的长期字段集合

### 可以从活跃上下文中移除的内容
- “测试页的 move 事件还没接到 VPet” 这件事
- “当前没有状态回传闭环” 这件事

## Checkpoint 3 - 2026-03-27 Combo Validation + State Expansion

### 当前阶段
- 阶段 3：`window.move` 基础闭环之后，继续完成组合体感验证与状态扩展

### 本轮完成内容
- 扩充 VPet 状态回传，新增 `right / bottom / display_animat / working_state / work_name / work_type / bubble_visible`
- 在 `/dev/control` 增加组合场景按钮，用于直接验证 `move -> bubble`、`bubble -> move`、`move -> motion` 和 `move -> bubble.touch`
- 在联调页与文案上把 `move.intent` 明确降级为 legacy 入口
- 给 `start-vpet-bridge.ps1` 增加 `Setting.lps` 自动启用 `agentbridge` mod 的兜底
- 完成一轮新的真实联调采样，记录组合场景的状态时间线

### 本轮决策与原因
- 决策：最小状态回传先补“边界距离 + 动画阶段 + 工作态 + 气泡可见性”，不继续深挖 `GameCore`
- 原因：这些字段都能从现有公开对象低成本拿到，已经足够支撑第一阶段组合联调
- 决策：`move.intent` 继续保留运行时薄兼容，但退出第一阶段主验证面
- 原因：legacy 不一定要立即删掉，但新的联调入口不能再把它和 `window.move` 并列对待

### 本轮沉淀经验
- `move -> bubble` 可以成立，但节奏不能太紧；本轮采样里约 `450ms` 间隔明显比 `280ms` 稳
- `bubble -> move` 与 `move -> motion.play` 的体感更稳定，状态也更容易读
- `bubble_visible` 和 `display_animat` 对组合联调很有用，能看出“事件已经消费”与“视觉状态真正切换”之间的时间差
- 本地启动链路里，`Setting.lps` 的 `onmod:|agentbridge:|` 应该由脚本兜底，而不是每轮靠人工记忆

### 待解决问题
- 是否还要继续补极少量桌宠运行态字段
- `move.intent` 何时彻底退到纯文档兼容
- 更长链路的动作编排是否需要后端场景层来接手，而不是全靠手点测试页

### 下一步
- 用扩展后的状态字段继续验证更长链路的编排组合
- 判断当前状态字段集是否足够
- 决定 `move.intent` 的最终退场节奏

### 可以从活跃上下文中移除的内容
- “联调页还只能单条发事件” 这件事
- “最小状态只能看 left/top 和 display” 这件事

## Checkpoint 4 - 2026-03-27 Sequence / Scenario Entry

### 当前阶段
- 阶段 3：在已有 `window.move + state` 闭环上补最小 sequence/scenario 联调入口

### 本轮完成内容
- 在 `backend-agent` 新增最小编排层：
  - `GET /api/dev/scenarios`
  - `POST /api/dev/scenarios/{scenario_id}`
  - `POST /api/dev/sequences`
- 新增 `DevSequenceOrchestrator`，让后端而不是浏览器脚本负责步骤延迟和事件顺序
- `/dev/control` 改成从后端读取 scenario 目录，并增加自定义 sequence JSON 入口
- 更新迁移文档，补充 sequence/scenario 用法和扩展后的状态字段
- 更新启动脚本，尝试进一步清理 `uvicorn --reload` 家族进程

### 本轮决策与原因
- 决策：组合场景要下沉到后端，而不是继续写死在浏览器脚本里
- 原因：这样同一套短编排可以被测试页和后端逻辑复用，也更接近后续行为层
- 决策：最小 sequence 继续复用现有单事件 schema，不另起一套动作协议
- 原因：第一阶段重点是编排顺序，不是重新设计底层事件模型

### 本轮沉淀经验
- 对“说话 -> 位移 -> 动作”这类短链路，后端 sequence 比前端 `wait(...)` 更容易复用和记录
- `DevSequenceOrchestrator` 这种薄编排层已经足够支撑第一阶段联调，不需要立刻上更重的行为树或任务系统
- 本会话里标准 18787 链路仍然可能被旧 `uvicorn --reload` 进程劫持；隔离到 18788 端口可以证明当前代码本身是新的

### 待解决问题
- 标准 18787 启动链路为什么仍可能服务旧 backend
- 当前 sequence/scenario 是否还需要少量状态字段配合
- `move.intent` 退场节奏

### 下一步
- 用新的 backend sequence/scenario 入口继续做更长链路编排验证
- 排查 18787 标准启动链路的旧 backend 残留问题
- 评估是否补少量桌宠运行态字段

### 可以从活跃上下文中移除的内容
- “组合场景必须写死在 `/dev/control` 前端脚本里” 这件事
- “还没有自定义 sequence 联调入口” 这件事

## Checkpoint 5 - 2026-03-27 Context Save

### 当前阶段
- 阶段 3：sequence/scenario 已落地，开始为下一轮收口上下文和启动链路问题

### 本轮完成内容
- 把最新 sequence/scenario 进展同步回 `.explore`
- 新增 handoff，准备在新对话里直接续接
- 在迁移实施文档里补上 `18787` 旧 `uvicorn --reload` 进程残留的联调注意事项

### 本轮决策与原因
- 决策：当前先做 handoff，而不是继续扩新功能
- 原因：当前上下文已偏长，且 sequence/scenario 主功能已经完成，需要先保证恢复成本足够低

### 本轮沉淀经验
- 当联调链路里存在旧进程抢端口的问题时，必须把“功能是否实现”和“默认端口是否连到正确进程”分开记录
- `.explore` 的 handoff 要把“已完成功能”和“残留环境问题”明确拆开写，否则下次容易误判成功/失败边界

### 待解决问题
- 标准 `18787` 启动链路的旧 backend 残留问题
- 现有状态字段是否还需要少量补充
- `move.intent` 的最终退场节奏

### 下一步
- 从最新 handoff 继续，先处理 `18787` 启动链路问题，再回到更长链路 sequence 编排验证

### 可以从活跃上下文中移除的内容
- 这轮详细的路由设计推导
- 这轮逐次验证时的临时端口操作细节
