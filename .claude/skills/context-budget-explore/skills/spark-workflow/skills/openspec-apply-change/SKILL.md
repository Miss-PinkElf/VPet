---
name: openspec-apply-change
description: 在内置 spark-workflow 中用于按当前 mission 的 tasks.md 实现已批准任务，并严格执行调试、审查与验证门禁。
---

# OpenSpec Apply（内置版）

根据 `tasks.md` 实施已批准变更。

## 输入

- 已批准的 `proposal.md`
- 已批准的 `design.md`
- 已批准的 `tasks.md`

## 步骤

1. 编码前重新读取所有当前 artifact
2. 选择执行模式：
   - 顺序模式：适合耦合任务
   - 并行模式：适合独立任务
   - 子代理模式：适合更大、更隔离的单元
3. 对每个任务：
   - 先标记为 `in_progress`
   - 只实现该任务范围
   - 按验收标准自检
   - 只有拿到证据后才标记完成
4. 如果出现失败，立即转到 [../superpowers-systematic-debugging/SKILL.md](../superpowers-systematic-debugging/SKILL.md)
5. 如果任务属于纯逻辑或纯变换单元，可选用 [../superpowers-test-driven-development/SKILL.md](../superpowers-test-driven-development/SKILL.md)
6. 如果任务之间明显独立，可考虑 [../superpowers-dispatching-parallel-agents/SKILL.md](../superpowers-dispatching-parallel-agents/SKILL.md)
7. 如果工作量大且适合隔离实现/审查循环，可考虑 [../superpowers-subagent-driven-development/SKILL.md](../superpowers-subagent-driven-development/SKILL.md)
8. 完成当前 Apply 阶段后，回到外层主 skill 更新 `state.md`、`decision-log.md`、`learnings.md`

## 停止条件

出现以下情况时，暂停 Apply 并回到 Propose：

- 暴露出设计缺陷
- 任务边界拆错
- 新用户约束使当前设计失效

## 约束

- 不要凭记忆实现，要按 artifact 实现
- 不要把无关修复塞进同一个任务
- 多次失败后不要继续猜修
