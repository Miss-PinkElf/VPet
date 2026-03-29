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

## Checkpoint 6 - 2026-03-27 Standard 18787 Startup Fix + Long Sequence

### 当前阶段
- 阶段 3：标准启动链路已收口，开始把 sequence/scenario 提升到 4 步长链路联调

### 本轮完成内容
- 将 `backend-agent/run-dev.ps1` 与 `run-dev.sh` 改为默认不带 `uvicorn --reload`
- 为 `run-dev` 补上显式热重载开关：`-Reload` 或 `PET_BACKEND_RELOAD=1`
- 强化 `start-vpet-bridge.ps1`：
  - 清理后端进程时同时合并 `Get-NetTCPConnection` 与 `netstat` 的监听 PID
  - 启动后通过 `/api/dev/scenarios` 与 `sequence-editor` 做 readiness 校验
- 将 `DevSequenceOrchestrator` 的预设场景扩到 6 个，新增两个 4 步场景
- 将 `/dev/control` 默认 sequence JSON 升级成 4 步长链路示例
- 完成验证：
  - 代码内验证 4 步 scenario / custom sequence 事件顺序正确
  - 标准 `18787` 链路下 `/api/dev/scenarios` 与 `/dev/control` 均返回新版本内容
  - 新长链路 scenario 与 4 步自定义 sequence 在 HTTP 层都返回 `accepted`

### 本轮决策与原因
- 决策：标准启动链路默认不再使用 `uvicorn --reload`
- 原因：Windows 下 reload watcher/worker 残留会直接污染第一阶段联调，稳定性优先于热重载体验
- 决策：继续把长链路联调样例下沉到后端 scenario 目录
- 原因：这样 `/dev/control`、后端验证脚本与后续行为层都能复用同一套 4 步编排

### 本轮沉淀经验
- Windows 下 `Get-NetTCPConnection` 不一定能完整枚举 reload 家族监听 PID，和 `netstat` 做并集更稳
- 对标准联调链路，启动后 readiness 校验比单纯 `Start-Sleep 2` 可靠得多
- 对第一阶段身体层桥接，4 步 sequence 已经足够暴露“思考态 -> 位移 -> 说话 -> 恢复”这类关键编排问题

### 待解决问题
- 真实 VPet 运行态下，4 步 sequence 的状态时间线是否还需要额外字段辅助判断
- `move.intent` 何时彻底退出运行时入口
- `emotion -> graph` 是否继续补运行时导出

### 下一步
- 在真实 VPet 上继续采样 `thinking-walk-think` 和 `bubble-move-touch-recover` 的状态回传时间线
- 评估是否需要补 `topmost / hitthrough` 一类最小运行态字段
- 决定 `move.intent` 的最终退场方式

### 可以从活跃上下文中移除的内容
- “标准 18787 链路会随机连到旧页面” 这件事
- “当前长链路只能靠手写临时 JSON 验证” 这件事

## Checkpoint 7 - 2026-03-28 Sleep Handoff

### 当前阶段
- 阶段 3：标准启动链路已收口，准备暂停并在下个对话继续真实 VPet 长链路联调

### 本轮完成内容
- 新增睡前 handoff
- 新增下个新对话可直接粘贴的提示词文件
- 更新 `handoffs/index.md` 与 `state.md`，把最新恢复入口切到 2026-03-28 handoff

### 本轮决策与原因
- 决策：暂停前不再继续扩功能，而是先把恢复入口压到最低成本
- 原因：当前主风险已经从“实现缺失”转到“下次能否零歧义续接真实联调”

### 本轮沉淀经验
- 当实现、验证、文档和 mission 记录都已经完成一轮收口后，单独再补一份睡前 handoff 最省下次恢复成本
- 新对话提示词单独落一个 md，比把恢复指令只塞在 handoff 正文里更好复用

### 待解决问题
- 真实 VPet 上 4 步 scenario 的状态时间线是否需要新字段
- `move.intent` 的最终退场方式
- `emotion -> graph` 的长期收敛方式

### 下一步
- 直接从新的 handoff 和 prompt 文件恢复，继续真实联调

### 可以从活跃上下文中移除的内容
- 这轮提交前的临时收尾动作

## Checkpoint 8 - 2026-03-28 Timeline Observability + Legacy UI Demotion

### 当前阶段
- 阶段 3：真实 VPet 长链路时间线已完成一轮高频采样，开始收口“时间可观测性”和 `move.intent` 退场节奏

### 本轮完成内容
- 重新拉起真实 `18787` 链路，并在真实 VPet 上串行采样：
  - `thinking-walk-think`
  - `bubble-move-touch-recover`
- 将 `start-vpet-bridge.ps1` 调整为默认注入更高频桥接参数：
  - `VPET_AGENT_BRIDGE_INTERVAL_MS=250`
  - `VPET_AGENT_BRIDGE_STATE_INTERVAL_MS=500`
- 在插件状态快照与后端 schema 中新增 `last_event_at`
- `/dev/control` 移除 `move.intent` 手动入口，只保留 `window.move`
- 更新迁移映射文档，明确新的状态字段与 legacy 退场位置

### 本轮决策与原因
- 决策：当前不再补 `topmost / hitthrough` 一类桌宠工作态字段
- 原因：真实采样显示 `left / top / right / bottom + display_animat + bubble_visible + last_event_type/at` 已足够支撑第一阶段联调判断
- 决策：`move.intent` 从联调 UI 继续降级，但运行时暂不直接删除
- 原因：当前已经明确不再是主路径，但保留薄兼容能降低历史调试脚本断裂成本
- 决策：时间可观测性的优先级高于继续补工作态字段
- 原因：本轮的主要盲点不在“状态有没有”，而在“何时消费事件、何时真正切画面”

### 本轮沉淀经验
- `last_event_at` 和状态 `timestamp` 分开后，能够明显区分“事件已消费”和“状态快照稍后才上报”
- `bubble_visible` 更适合表达视觉残留，不适合单独拿来判断事件顺序
- VPet 会在空闲时继续自主移动，所以长时间窗口采样容易混入自然位移；验证 `window.move` 应优先看事件触发后的短窗口
- 对真实桌宠联调来说，默认更高频的 poll/state 回传比继续堆状态字段更有价值

### 待解决问题
- `move.intent` 是否下一轮彻底退到纯文档兼容
- 是否要增加 `event_id / sequence_name` 级别的关联字段
- `emotion -> graph` 是否继续做运行时导出

### 下一步
- 用当前高频链路继续验证更接近演示故事线的 sequence
- 评估是否补事件关联字段
- 决定 `move.intent` 的最终退场方式

### 可以从活跃上下文中移除的内容
- “还不确定是否必须补更多桌宠工作态字段” 这件事
- “`move.intent` 仍然要保留在联调主界面里” 这件事

## Checkpoint 9 - 2026-03-28 Quick Test JSON Catalog Page

### 当前阶段
- 阶段 3：在现有联调页基础上补一个更轻的 JSON 测试目录入口，方便按测试项快速触发

### 本轮完成内容
- 在 `backend-agent/app/api/routes/dev_control.py` 中新增 `/dev/quick-test`
- quick test 页面支持：
  - 读取数组或 `{ "tests": [...] }` 形式的 JSON
  - 将每个测试项渲染成可点击卡片
  - 自动识别 `payload` 是单事件还是 sequence
  - 分别调用 `/api/dev/messages` 或 `/api/dev/sequences`
- 在 `/dev/control` 顶部增加跳转到 `/dev/quick-test` 的入口
- 重启标准 `18787` 链路，使新页面立即可用

### 本轮决策与原因
- 决策：quick test 单独成页，而不是继续往 `/dev/control` 里塞更多控件
- 原因：`/dev/control` 已经承担完整联调功能，quick test 的目标只是快速读取一份测试目录 JSON 并一键执行
- 决策：先让测试项显式带 `payload`
- 原因：这样最简单、最稳定，也最接近你未来从自己后端直接发送的调用面

### 本轮沉淀经验
- 对当前阶段来说，“从 JSON 目录点一个测试直接发”比继续扩传统表单更贴近后端集成使用方式
- quick test 页适合承载你自己的常用测试 catalog，而 `/dev/control` 保留为完整联调页

### 待解决问题
- 是否要给 quick test 再补“导入外部文件”而不是只粘贴 JSON
- 是否要让 quick test 绑定一组更贴近真实后端业务的默认测试样例

### 下一步
- 用 quick test 维护一组标准测试 catalog
- 继续用它验证第一阶段正式协议

### 可以从活跃上下文中移除的内容
- “每次都要在 `/dev/control` 手工改表单或改 sequence 文本” 这件事

## Checkpoint 10 - 2026-03-28 Quick Test File-Backed Catalog

### 当前阶段
- 阶段 3：quick test 已从页面内置样例升级为 mission 文件托管的测试目录

### 本轮完成内容
- 将 quick test catalog 落盘到：
  - `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
- 新增后端接口：
  - `GET /api/dev/quick-test/catalog`
  - `PUT /api/dev/quick-test/catalog`
- `/dev/quick-test` 现已支持：
  - 启动时自动从 mission 文件读取测试目录
  - 将编辑后的 JSON 保存回 mission 文件
  - 再从文件重新加载并渲染测试卡片
- 已验证读取、覆盖保存、恢复默认 catalog 整条链路可用

### 本轮决策与原因
- 决策：quick test catalog 放在 `.explore` 而不是继续内嵌在 HTML
- 原因：这样测试目录本身也成为 mission 真相的一部分，便于迭代和续接
- 决策：先用简单的整文件读写，而不是上更复杂的多文件管理
- 原因：当前目标是方便维护测试目录，不是做完整测试平台

### 本轮沉淀经验
- 对当前阶段最实用的增强不是继续扩 quick test UI，而是让测试 catalog 可被持久化和版本化
- `.explore/.../quick-tests.json` 比散落在页面源码里的默认 JSON 更适合逐步沉淀“你的后端真正会发什么”

### 待解决问题
- 是否要继续提供多个 catalog 文件，而不是只维护一个默认 quick test 文件
- 是否要把真实业务链路样例也沉淀进该 catalog

### 下一步
- 继续把常用测试样例沉淀到 `quick-tests.json`
- 用这些样例验证第一阶段正式协议是否已经足够

### 可以从活跃上下文中移除的内容
- “quick test 默认目录只能靠改 HTML 字符串维护” 这件事

## Checkpoint 11 - 2026-03-28 Current Phase Test Catalog

### 当前阶段
- 阶段 3：当前阶段该测什么，已经从口头列表收口为 quick test catalog

### 本轮完成内容
- 将 `quick-tests.json` 扩成当前阶段测试目录
- 明确写入：
  - 当前阶段测试目的
  - 建议观察字段
  - 单事件测试项
  - 两条核心 sequence 测试项
  - 每条测试的通过标准

### 本轮决策与原因
- 决策：把“当前阶段要测什么”直接写进 quick test catalog，而不是只保留在聊天记录里
- 原因：这样你可以直接在 `/dev/quick-test` 按测试项点，并把结果按同一套目录回传

### 本轮沉淀经验
- 对当前阶段最重要的不是再发散测试面，而是把该测项和通过标准固定下来
- 把测试清单和测试入口绑定在一起，比单独维护一份文字清单更好执行

### 待解决问题
- 你跑完这套当前阶段测试后的实际结果如何
- 哪些项是稳定通过，哪些项还有体感或时间线问题

### 下一步
- 由你按 `quick-tests.json` 逐项测试
- 把实际观察结果回给我
- 我再据此决定是否要继续收口协议或补最小改动

### 可以从活跃上下文中移除的内容
- “当前阶段到底要测哪些项” 这件事

## Checkpoint 12 - 2026-03-28 Quick Test Result Writeback

### 当前阶段
- 阶段 3：quick test 已从“只负责触发测试”升级为“可直接记录并回写测试结果”

### 本轮完成内容
- 在 `/dev/quick-test` 新增“测试结果”编辑区
- 页面现支持：
  - 选择一个测试项
  - 编辑结果状态
  - 记录结果说明
  - 点击 `Save Result` 回写到 `quick-tests.json`
- 已验证：
  - 页面包含结果编辑区与 `Save Result`
  - API 写回后，再读取 `quick-tests.json` 能看到刚保存的结果

### 本轮决策与原因
- 决策：测试结果直接落回 `quick-tests.json`
- 原因：这样你不需要再手动把结果转述给我，我后续直接读取 mission 文件即可

### 本轮沉淀经验
- 对当前阶段最省协作成本的做法，不是再加更多输入框，而是让测试入口和测试结果落在同一份 mission 文件里

### 待解决问题
- 等你实际跑完当前阶段测试后，各项结果是什么
- 哪些测试项还需要调整为更贴近真实后端调用场景

### 下一步
- 由你直接在 `/dev/quick-test` 中执行并保存测试结果
- 我下次直接读 `quick-tests.json` 就能继续判断

### 可以从活跃上下文中移除的内容
- “测试完还要再手工把结果打字发回来” 这件事

## Checkpoint 13 - 2026-03-28 Move Instability Root Cause

### 当前阶段
- 阶段 3：通过 quick test 的真实结果回填，已定位移动不稳定的第一层根因

### 本轮完成内容
- 读取 `quick-tests.json` 中你保存的实际测试结果
- 确认当前问题集中在：
  - `window.move`
  - 含移动的 sequence
- 对照桥接层与原生 move graph 配置定位到根因：
  - `window.move` 处理时同时调用 `DisplayMove()` 和 `MoveWindows(...)`
  - 原生 `DisplayMove()` 会进入 `walk/crawl/fall/climb` 图并带自身运动语义
- 已修正 `AgentBridgePoller`：
  - `window.move` 改为纯位移
  - `move.intent` 也去掉 `DisplayMove()`
- 已通过标准启动链路重新编译并重启 VPet

### 本轮决策与原因
- 决策：显式 `window.move` 不再附带原生移动动作
- 原因：第一阶段里“移动能力”应是可控位移协议，不应再叠加 VPet 自身带方向/速度语义的运动图

### 本轮沉淀经验
- 对“身体层前端”来说，物理位移和视觉动作要分层控制；把二者绑死会直接破坏可预测性
- quick test 结果回写已经足够暴露“说话/动作都稳，只有移动有系统性问题”这种结构性结论

### 待解决问题
- 去掉 `DisplayMove()` 后，移动是否已经稳定
- 若 sequence 仍乱，是否还需要调整移动步与后续 bubble/motion 的间隔

### 下一步
- 优先复测所有含移动的测试项
- 如果单独移动稳定了，再看 sequence 是否仍需要微调 delay

### 可以从活跃上下文中移除的内容
- “移动不稳定可能只是观测问题” 这件事

## Checkpoint 14 - 2026-03-28 Sequence Delay Relaxation

### 当前阶段
- 阶段 3：移动协议问题已基本排除，继续收口 sequence 节奏重合

### 本轮完成内容
- 读取第二轮 quick test 结果，确认：
  - 单独 `window.move` 已变成纯移动
  - 两条长链路 sequence 仍偏快、动作重合
- 调整 `DevSequenceOrchestrator` 中两条核心场景的 delay
- 同步调整：
  - `quick-tests.json`
  - `/dev/control` 默认 sequence 示例
- 重启标准链路，使新的 delay 立即生效

### 本轮决策与原因
- 决策：当前继续调节 delay，而不是再修改正式协议
- 原因：问题已经从“协议语义错”收口到“编排节奏太紧”

### 本轮沉淀经验
- 当单事件能力已经稳定、sequence 只剩重合感问题时，最有效的修正是拉开步间延迟，而不是继续扩状态或扩协议

### 待解决问题
- 新 delay 下，两条核心 sequence 是否已经达到可接受体感

### 下一步
- 只复测两条核心 sequence
- 若仍有轻微重合，再做小幅 delay 微调

### 可以从活跃上下文中移除的内容
- “是否还要继续改 window.move 语义” 这件事

## Checkpoint 15 - 2026-03-28 Smart Move Style

### 当前阶段
- 阶段 3：在移动协议已稳定的基础上，继续收口移动体感

### 本轮完成内容
- 根据你的反馈，将 `window.move` 从“纯瞬移语义”扩成带 style 的移动语义
- 后端 schema 新增：
  - `window.move.style`
- 当前支持的 style：
  - `smart`
  - `smooth` / `walk`
  - `snap` / `teleport`
- 默认策略：
  - 短距离：平滑分步走位
  - 长距离：直接跳位
- 将当前阶段 quick test 中的移动相关测试统一切到 `style=smart`
- 重新编译并重启标准链路

### 本轮决策与原因
- 决策：先做“短距平滑、长距跳位”，暂不承诺“开门闪现”专项视觉
- 原因：当前仓库里没有稳定确认可复用的开门/闪现 graph；先保证行为体感可靠，比临时硬接不稳定视觉更重要

### 本轮沉淀经验
- 当前阶段移动体感的关键不是单纯“有没有移动”，而是：
  - 短距不要生硬
  - 长距不要拖沓
- 这类问题更适合用 style 和默认策略解决，而不是继续把单一 `window.move` 绑定成某一种固定表现

### 待解决问题
- `style=smart` 是否已经达到可接受体感
- 两条 sequence 在新 style + 新 delay 下是否还会重合

### 下一步
- 最小复测：
  - 三条移动单测
  - 两条核心 sequence
- 如果仍有轻微问题，再只做小幅参数微调

### 可以从活跃上下文中移除的内容
- “移动只能是纯瞬移” 这件事

## Checkpoint 16 - 2026-03-28 Sequence Wait-For Gating

### 当前阶段
- 阶段 3：不再继续猜 delay，已把关键 sequence 步骤升级到显式完成门控

### 本轮完成内容
- 在 `backend-agent/app/schemas/events.py` 为 sequence step 新增：
  - `wait_for`
  - `wait_timeout_ms`
  - `settle_ms`
- 在 `DevSequenceOrchestrator` 中落地基于状态回传的最小门控：
  - `event_applied`
  - `move_complete`
  - `motion_complete`
- 将两条核心长链路切到新的门控语义：
  - `thinking-walk-think`：`window.move -> wait_for=move_complete`
  - `bubble-move-touch-recover`：
    - `window.move -> wait_for=move_complete`
    - `motion.play(touch_head) -> wait_for=motion_complete`
- 同步更新：
  - `/dev/control` 默认 sequence 示例
  - `.explore/desktop-pet-vpet-body-bridge/quick-tests.json`
  - `.explore/desktop-pet-vpet-body-bridge/spec/protocol-phase1.md`
- 完成最小验证：
  - `python -m compileall backend-agent/app` 通过
  - 使用 `backend-agent/.venv/Scripts/python.exe` 的模拟状态脚本验证两种核心门控可放行

### 本轮决策与原因
- 决策：本轮先用后端状态门控收口 sequence，而不是立即深改插件或 `GameCore`
- 原因：当前 `window.move` 的真正痛点是“后一步太早发出”，而现有状态回传已经足够支撑最小闭环
- 决策：优先支持 `move_complete` 和 `motion_complete`
- 原因：这两类正好覆盖当前两条核心 sequence 中最容易重合的关键步骤

### 本轮沉淀经验
- `window.move` 这类由桥接显式控制的步骤，不需要额外猜 delay；只要等待 `last_event_at` 更新并核对 `left/top` 落点即可形成稳定门控
- 对短动作，先通过 `display_name/display_type` 进入并退出目标动作态做最小完成判断，已经比固定延迟稳得多
- 当前阶段更该优先做“关键步显式等待”，而不是继续全局拉大每一步 delay

### 待解决问题
- 真实 VPet 上新的 `move_complete / motion_complete` 是否已经把体感重合压到可接受范围
- `motion_complete` 对更多动作是否同样稳定，还是目前只应先用于 `touch_head/touch_body/pinch`
- 是否还需要补 `event_id / sequence_name` 级别的关联字段
- 是否最终需要 `native_walk` 一类由原生 move 系统独占移动权的模式

### 下一步
- 用真实 VPet 最小复测两条核心 sequence
- 将新的真实结果继续回写到 `quick-tests.json`
- 根据复测结果决定：
  - 当前门控是否已足够
  - 还是要进一步下探到原生动作完成回调或 `native_walk`

### 可以从活跃上下文中移除的内容
- “下一轮还只是继续猜 delay” 这件事
- “sequence 完成门控还完全没实现” 这件事

## Checkpoint 17 - 2026-03-29 Sleep Handoff After Sequence Gating

### 当前阶段
- 阶段 3：最小 `wait_for` 门控已落地，准备暂停并把明早恢复入口压到最低成本

### 本轮完成内容
- 复查 `.explore` 与实现文件，确认本轮“sequence 完成门控”已有：
  - `state.md`
  - `checkpoints.md`
  - `protocol-phase1.md`
  - `quick-tests.json`
  - `handoff`
- 继续补齐此前还没明确写入的 spec 记录：
  - `proposal.md`
  - `design.md`
  - `tasks.md`
- 新增睡前 handoff：
  - `2026-03-29-012-sleep-handoff-after-sequence-gating.md`
- 新增明早可直接复制的恢复提示词：
  - `next-chat-prompt-2026-03-29-sequence-gating-retest.md`

### 本轮决策与原因
- 决策：睡前不再继续扩实现，先把恢复入口和文档收口
- 原因：当前主要风险已经不是“门控还没做”，而是明早恢复时是否还会丢上下文或重复分析

### 本轮沉淀经验
- 对这种跨多轮的桥接任务，真正省成本的不是多记一段聊天总结，而是把：
  - 最新 handoff
  - 最新 state
  - 明早可直接复制的 prompt
  一起落到 mission 目录

### 待解决问题
- 真实 VPet 上新的 `wait_for` 门控是否已经让两条核心 sequence 收口
- `motion_complete` 是否需要进一步下探到原生回调
- 是否最终需要 `native_walk`

### 下一步
- 明早直接按新的 prompt 恢复
- 最小复测两条核心 sequence 和三条移动单测
- 继续把真实结果回写到 `quick-tests.json`

### 可以从活跃上下文中移除的内容
- 这轮文档补齐前的零散恢复说明

## Checkpoint 18 - 2026-03-29 Real Retest After Event-Applied + Move Tolerance Fix

### 当前阶段
- 阶段 3：核心 `wait_for` 门控已在真实 VPet 上完成隔离复测

### 本轮完成内容
- 用真实 GUI 链路重新拉起标准 `18787` 联调
- 定位到 sequence 卡死的两层直接原因：
  - 前置关键步未门控，导致后续 `window.move` 的 baseline 可能取到旧状态
  - `move_complete` 的落点容差 `1.5` 在真实状态回传下过紧
- 已修正：
  - `thinking-walk-think` 首步 `mode.switch(thinking)` 改为 `wait_for=event_applied`
  - `bubble-move-touch-recover` 首步 `bubble.show` 改为 `wait_for=event_applied`
  - `move_complete` 容差 `1.5 -> 6.0`
  - `/dev/control` 默认 sequence 与 `quick-tests.json` 同步到新门控
- 在 fresh start / 隔离采样下完成真实复测并回写：
  - `move-right-120`
  - `move-left-120`
  - `move-diagonal`
  - `sequence-thinking-walk-think`
  - `sequence-bubble-move-touch-recover`

### 本轮决策与原因
- 决策：当前不下探 `motion_complete` 到原生回调
- 原因：`touch_head` 在真实 VPet 上已能稳定走完 `A_Start/B_Loop/C_End -> default`，当前证据足够
- 决策：当前不引入 `native_walk`
- 原因：核心 sequence 与 `style=smart` 位移已在 phase 1 范围内验证通过，没有必要提前引入新的移动模式复杂度

### 本轮沉淀经验
- 对依赖状态回传的 `move_complete`，如果前一步也会改变视觉/姿态，前一步至少要有 `event_applied`，否则后一步很容易拿到旧 baseline
- 真实桌宠状态回传存在小幅浮点/落点抖动，位移完成门控不能把容差收得过死
- `bubble_visible` 继续适合作为视觉残留字段，不适合拿来判断 sequence 事件先后

### 待解决问题
- 是否要把这组门控模式扩到更多 story-like sequence
- 是否需要补 `event_id / sequence_name` 一类事件关联字段
- `move.intent` 何时彻底退到纯文档兼容

### 下一步
- 以这轮已通过的 5 条真实测试作为 phase 1 基线
- 如果继续扩长链路，优先补事件关联字段而不是继续扩桌宠工作态
- 仅当后续新动作类型暴露问题时，再重开“原生动作完成回调 / native_walk”话题

### 可以从活跃上下文中移除的内容
- “当前 wait_for 还没有在真实 VPet 上证明可用” 这件事
- “两条核心 sequence 仍然主要靠猜 delay” 这件事

## Checkpoint 19 - 2026-03-29 Event Correlation Fields + Longer Story Sequence

### 当前阶段
- 阶段 3：phase 1 基线已稳定，开始为更长 story sequence 增加最小事件关联能力

### 本轮完成内容
- 在 Python 事件 schema 中新增：
  - `event_id`
  - `sequence_name`
  - `step_index`
- 在状态回传 schema 中新增：
  - `last_event_id`
  - `last_sequence_name`
  - `last_step_index`
- `BehaviorPolicyEngine` 现在会为手动事件自动生成 `event_id`
- `DevSequenceOrchestrator` 现在会为 sequence step 自动附带：
  - `event_id`
  - `sequence_name`
  - `step_index`
- sequence 门控现在优先按 `event_id` 判断事件是否已被消费
- C# 插件已同步接入并回传上述关联字段
- 新增一个更长的 6 步 story sequence 到后端 scenario 与 `quick-tests.json`：
  - `think-speak-move-touch-speak-recover`
- `protocol-phase1.md` 已同步补上“Shared Trace Metadata”说明
- 当前这条新增 6 步 sequence 仅完成定义与目录更新，真实结果未由助手回填，仍等待你自己测试后写回 `quick-tests.json`

### 本轮决策与原因
- 决策：先补事件关联字段，不继续扩更多桌宠内部工作态
- 原因：当前更长链路的主要盲点已经不是“状态字段太少”，而是“重复事件类型下缺少后端步骤和前端消费的稳定对应关系”

### 本轮沉淀经验
- 对更长的 sequence，`last_event_type` 只能回答“刚消费了什么类型”，不能稳定回答“消费的是这条 sequence 的第几步”
- `event_id / sequence_name / step_index` 这组三个字段，比继续堆工作态字段更直接、更贴近后端编排需求
- 插件构建在沙箱内会卡在 MSBuild/项目引用阶段且不给有效错误；这类验证应优先用真实环境构建

### 待解决问题
- 新增 6 步 story sequence 的真实复测结果
- `move.intent` 何时彻底退到纯文档兼容
- 后续是否需要把 `bubble.show` 生命周期也做成更强的完成门控

### 下一步
- 由你在真实 VPet 上最小复测 `sequence-think-speak-move-touch-speak-recover`
- 观察两次 `bubble.show` 是否能通过 `last_event_id / last_step_index` 稳定区分
- 如果这条更长链路也收口，再考虑把关联字段扩到 backend-agent 更正式的调用面

### 可以从活跃上下文中移除的内容
- “phase 1 还没有更长 sequence 的测试目录入口” 这件事
- “当前门控仍只能靠类型和时间猜步骤” 这件事

## Checkpoint 20 - 2026-03-29 Sleep Handoff After Event Correlation

### 当前阶段
- 阶段 3：事件关联字段与 6 步 story sequence 已落地，准备暂停并压低下次恢复成本

### 本轮完成内容
- 检查当前改动与 `.explore` 记录缺口
- 新增 handoff：
  - `2026-03-29-013-sleep-handoff-after-event-correlation.md`
- 更新：
  - `handoffs/index.md`
  - `state.md` 的最新 handoff 入口
  - 根目录 `CONTINUE_VPET_BRIDGE_PROMPT.md`
- 明确把新的协作边界写入恢复提示词：
  - assistant 不替你跑真实联调
  - assistant 负责补测试定义与实现
  - 真实结果由你自己回写到 `quick-tests.json`

### 本轮决策与原因
- 决策：恢复入口要直接切到“事件关联字段已落地，但 6 步 sequence 结果仍待你自己回写”的状态
- 原因：这样下次恢复不会误判这条新增 sequence 已经完成真实验证

### 本轮沉淀经验
- 对长期任务来说，handoff、state 和 continue prompt 三者必须同步；只更新其中一个，恢复时仍然容易偏离真实边界
- 当用户明确要求“我自己测”，这个协作边界也应该写进 handoff 和 continue prompt，而不只是留在聊天里

### 待解决问题
- `sequence-think-speak-move-touch-speak-recover` 的真实联调结果
- `move.intent` 何时彻底退到纯文档兼容
- 是否要把完成门控继续扩到更多步骤

### 下一步
- 由你休息后用 `CONTINUE_VPET_BRIDGE_PROMPT.md` 恢复
- 由你自己做新增 6 步 sequence 的真实联调并回写结果
- 我再基于你回写的 `quick-tests.json` 继续收口实现

### 可以从活跃上下文中移除的内容
- 这轮 handoff 创建前的临时恢复说明
- 这轮关于“助手要不要代跑真实联调”的反复确认
