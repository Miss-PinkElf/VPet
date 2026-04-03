---
name: superpowers-dispatching-parallel-agents
description: 在内置 spark-workflow 中，当 tasks.md 里的任务边界清晰、彼此独立且不会共享可变状态时使用并行代理模式。
---

# Superpowers Parallel Agents（内置版）

只有当任务边界真实存在时，并行才有价值。

## 适用场景

- 两个或更多任务相互独立
- 不会同时编辑同一批文件
- 集成顺序清晰

## 步骤

1. 按独立领域拆分 `tasks.md`
2. 给每个 agent 一个聚焦任务、验收标准和明确边界
3. 把共享文件或共享接口交给一个协调者负责
4. 汇总后检查冲突
5. 合并后再做集成验证

## 不要使用的场景

- 任务高度耦合
- 工作需要一个持续演进的单一设计上下文
- 多个 agent 很可能同时改同一批文件
