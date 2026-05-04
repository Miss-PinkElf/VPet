# 下一次对话提示词：desktop-pet-native-interaction-explore

把下面整段复制到新对话即可：

```text
继续 VPet 原生桌宠交互探索工作。使用 $devflow，并把 `.devflow/desktop-pet-native-interaction-explore/` 作为当前 mission 真相源。先走 devflow resume 路径，不要重新做大范围重复探索。

优先读取：
1. `.devflow/desktop-pet-native-interaction-explore/state.md`
2. `.devflow/desktop-pet-native-interaction-explore/checkpoints.md`
3. `.devflow/desktop-pet-native-interaction-explore/handoffs/index.md`
4. `.devflow/desktop-pet-native-interaction-explore/handoffs/2026-05-04-001-explore-wrap-up.md`
5. `.devflow/desktop-pet-native-interaction-explore/learnings/native-interaction-source-analysis.md`
6. `.devflow/desktop-pet-native-interaction-explore/learnings/desktop-pet-interaction-design-guide.md`
7. `.devflow/desktop-pet-native-interaction-explore/plans/2026-05-04-native-desktop-pet-design-document-plan.md`

当前进度：
- 已完成 VPet 原生桌宠交互逻辑源码探索
- 已完成设计借鉴文档沉淀
- 当前结论是：VPet 的桌宠感主要来自
  - 分层状态机（Layered State Machine）
  - 数据驱动动作资源（Data-driven Graph Resources）
  - 三段式动作语法（Start/Loop/End Animation Grammar）
  - 屏幕世界感知（Screen World Awareness）
  - 用户输入反馈闭环（User Feedback Loop）
- 当前不在实现阶段

未完成任务：
- 还没有进入 Align
- 还没有决定下一步实现目标到底是：
  - 后端行为引擎（Behavior Engine）
  - VPet phase 2 展示控制面（Display Control Surface）
  - 或两者之间的最小可实现子集

注意事项：
- 这个 mission 与 `.devflow/desktop-pet-vpet-body-bridge/` 分离，不要混写
- 当前探索结论已经够用，下轮优先收敛方向，不要无目的继续加大范围探索
- 如果准备开始实现，必须先做 Align，再写 Plan

建议下次优先处理：
1. 基于 `desktop-pet-interaction-design-guide.md` 讨论“当前项目最值得先复刻的 3 个桌宠能力”
2. 在 Align 中明确后续目标边界
3. 如达成一致，再落新的实施计划
```

