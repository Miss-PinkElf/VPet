---
name: openspec-archive-change
description: 在内置 spark-workflow 中用于在审查与验证都通过后，归档或正式关闭当前 mission 下的一个已完成子变更。
---

# OpenSpec Archive（内置版）

只有在变更真正完成后，才关闭生命周期。

## 前置条件

- proposal 中承诺的内容已经实现
- tasks 已完成，或有明确处置结论
- 已有验证证据
- review 发现已解决或已明确接受

## 步骤

1. 确认当前归档的是哪个子变更
2. 重新检查 artifact 与任务完成状态
3. 判断是否需要把 delta spec 同步回主规格集合
4. 在当前较轻量的 mission 工作流中记录关闭状态，或执行项目所需的归档动作
5. 总结本次交付内容、通过的证据，以及同步了什么
6. 回到外层主 skill 更新状态、决策与经验记录

## 约束

- 不要从“看起来实现完了”直接归档
- 如果验证失败，回到 Apply
- 如果 review 反馈意味着设计或范围变化，回到 Propose
