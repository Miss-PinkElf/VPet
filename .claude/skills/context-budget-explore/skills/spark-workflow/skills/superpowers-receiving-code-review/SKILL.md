---
name: superpowers-receiving-code-review
description: 在内置 spark-workflow 中，当收到审查反馈后，逐条进行技术核验，再决定修复、驳回或回退流程。
---

# Superpowers Receiving Code Review（内置版）

反馈是输入，不是命令。

## 处理顺序

1. 先冷静读完全部反馈
2. 对含糊项做重述或澄清
3. 逐条对照代码与已批准 artifact 做核验
4. 技术上成立的问题，一次修一个
5. 对不正确或超范围反馈，用证据说明并拒绝盲改

## 回退规则

如果反馈意味着需求或设计变化，应回到 Propose，而不是静默打补丁。

## 约束

- 不要表演式认同
- 关键项不清楚时，不要做半套实现
- 不要盲目接受会破坏现有行为或违反计划的建议
