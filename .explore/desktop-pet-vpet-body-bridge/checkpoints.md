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
