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
