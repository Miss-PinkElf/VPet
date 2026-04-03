---
name: openspec-explore
description: 在内置 spark-workflow 中用于纯讨论、需求探索、方案比较或代码调查，但暂不开始实现时使用。
---

# OpenSpec Explore（内置版）

这是内置 spark-workflow 的纯探索分支。

## 适用场景

- 用户想先讨论思路
- 需求仍然模糊
- 需要做方案比较、权衡分析或代码调查
- 当前还不应该开始实现

## 工作姿态

- 只探索，不实现
- 可以自由读取代码和文档
- 提问要帮助暴露约束与边界
- 图表、表格能帮助理解时可以使用
- 可以把结论整理成后续可进入 proposal 的摘要，但不要强推实现

## 输出目标

探索结束时，最好留下以下之一：

- 更清晰的需求定义
- 方案比较及推荐
- 已识别的风险与未知项
- 是否进入 Align / Propose 的明确建议

## 约束

- 本模式下不要写实现代码
- 如果讨论已经收敛到明确方向，转入 spark-workflow 的 Align 或 Propose
- 如果问题本质上是 bug 排查，转到 [../superpowers-systematic-debugging/SKILL.md](../superpowers-systematic-debugging/SKILL.md)
- 如果探索结论会影响后续行动，回到外层主 skill 更新 `state.md`、`decision-log.md` 或 `learnings.md`
