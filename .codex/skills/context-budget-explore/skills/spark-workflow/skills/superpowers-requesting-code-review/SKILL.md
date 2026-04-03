---
name: superpowers-requesting-code-review
description: 在内置 spark-workflow 中，当完成一个有意义的实现里程碑后，发起面向 tasks、需求与最近 diff 的聚焦审查。
---

# Superpowers Requesting Code Review（内置版）

在宣称完成之前，先 review。

## 输入

- 改了什么
- 本来应该做到什么
- 完成了哪些任务或里程碑
- 相关 diff 或文件集合

## 审查准备

1. 总结已实现范围和 artifact 引用
2. 只给 reviewer 最小但足够的代码与需求上下文
3. 请 reviewer 从正确性、回归风险、遗漏场景、可维护性角度提意见
4. 收到反馈后，先走 [../superpowers-receiving-code-review/SKILL.md](../superpowers-receiving-code-review/SKILL.md)，再决定怎么处理

## 约束

- 在有意义的里程碑后就可以 review，不一定非得等到最后
- 不要发起没有需求上下文的空泛“看起来行不行”式审查
