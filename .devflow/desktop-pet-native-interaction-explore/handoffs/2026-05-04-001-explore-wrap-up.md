# Handoff: 原生桌宠交互探索收尾

## 基础信息

- 创建时间：2026-05-04
- mission：`.devflow/desktop-pet-native-interaction-explore`
- 当前阶段：Explore
- handoff 编号：001
- 是否 superseded：否

## 当前目标

- 基于 VPet 原生源码，理解“像桌宠”的交互逻辑，并沉淀成可供当前项目借鉴的设计文档。

## 当前进度

- 已完成源码探索。
- 已完成设计向文档沉淀。
- 当前没有进入实现，不修改 bridge 主线代码。

## 本轮完成内容

- [x] 新建独立 devflow mission：
  - `.devflow/desktop-pet-native-interaction-explore/`
- [x] 初始化 mission 骨架：
  - `workflow.md`
  - `state.md`
  - `decision-log.md`
- [x] 使用并行子代理分别探索：
  - 自动行为 / 随机行为 / 状态机
  - 移动 / 贴边 / 爬墙 / 窗口行为
  - 用户交互 / 动作 / 资源能力
- [x] 沉淀源码分析文档：
  - `learnings/native-interaction-source-analysis.md`
- [x] 沉淀设计借鉴文档：
  - `learnings/desktop-pet-interaction-design-guide.md`
- [x] 新增文档计划：
  - `plans/2026-05-04-native-desktop-pet-design-document-plan.md`

## 关键决策与原因

| 决策 | 备选方案 | 原因 |
| --- | --- | --- |
| 新开独立 mission 分析原生桌宠交互 | 继续写入现有 bridge mission | 这是设计探索，不应污染已有 bridge 主线 |
| 本轮只做探索和文档沉淀，不进入实现 | 直接开始做 phase 2 或行为引擎实现 | 目前目标是先搞清原生桌宠感从哪里来，再决定实现方向 |
| 后续如要推进实现，应优先进入 Align | 继续在 Explore 阶段直接加代码 | 当前已经有足够探索结论，下一步应先收敛需求和实施边界 |

## 关键文件 / 产物

| 文件 | 作用 | 相关性 |
| --- | --- | --- |
| `.devflow/desktop-pet-native-interaction-explore/learnings/native-interaction-source-analysis.md` | 源码事实分析 | 解释原生逻辑如何工作 |
| `.devflow/desktop-pet-native-interaction-explore/learnings/desktop-pet-interaction-design-guide.md` | 设计借鉴文档 | 说明一个好的桌宠应具备什么，以及当前项目如何借鉴 |
| `.devflow/desktop-pet-native-interaction-explore/plans/2026-05-04-native-desktop-pet-design-document-plan.md` | 文档计划 | 记录本轮文档沉淀路径 |
| `.devflow/desktop-pet-native-interaction-explore/checkpoints.md` | 阶段收口记录 | 查看本轮探索与文档收尾 |
| `.devflow/desktop-pet-native-interaction-explore/state.md` | 当前状态 | 恢复入口的第一真相源 |

## 风险 / 阻塞项 / 开放问题

- [ ] 当前只有探索和设计结论，还没有进入 Align，后续实现目标仍需明确收敛。
- [ ] `graph.catalog / graph.play / behavior.invoke / display.report / display.reset` 只是推荐方向，尚未进入正式 spec 或实现。
- [ ] 当前没有决定下一步是做“后端行为引擎（Behavior Engine）”还是“VPet phase 2 展示控制面（Display Control Surface）”。

## 立即下一步

1. 读取 `state.md` 与 `checkpoints.md`，快速恢复当前 mission 的探索结论。
2. 阅读 `learnings/desktop-pet-interaction-design-guide.md`，确认后续要收敛成哪类实现目标。
3. 如果用户要继续推进，先进入 Align，明确是做行为引擎、phase 2 控制面，还是两者之间的最小子集。

## 恢复指引

1. 先读取 `handoffs/index.md`
2. 再读取本 handoff
3. 然后读取 `state.md`
4. 必要时读取：
   - `learnings/native-interaction-source-analysis.md`
   - `learnings/desktop-pet-interaction-design-guide.md`
   - `plans/2026-05-04-native-desktop-pet-design-document-plan.md`
5. 从“立即下一步”的第 1 条开始继续

## 可从活跃上下文移除的内容

- 子代理的详细中间推理过程
- 单次 `rg` / `Get-Content` 的原始读取输出

