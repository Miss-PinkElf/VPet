---
name: superpowers-subagent-driven-development
description: 在内置 spark-workflow 中，用于更大的 Apply 阶段；通过实现者与审查者分离的循环提升质量并控制上下文体积。
---

# Superpowers Subagent-Driven Development（内置版）

当任务足够大，以至于隔离执行与审查比单会话硬撑更划算时，使用这个模式。

## 模式

对每个任务：

1. 给一个实现者完整任务文本、artifact 上下文和验收标准
2. 让实现者完成任务并自检
3. 做一次面向 spec 的符合性审查
4. 做一次代码质量审查
5. 两个门都通过后，任务才算关闭

## 最适合的场景

- 任务多，耦合低或中等
- 代码面很大
- 需要明确区分实现和审查

## 约束

- 没有协调时，不要让多个实现者同时改同一批文件
- 不要因为实现者说“好了”就跳过审查
- 如果反复审查失败暴露任务或设计有问题，应回到 Propose
