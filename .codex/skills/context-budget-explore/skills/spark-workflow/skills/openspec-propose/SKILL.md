---
name: openspec-propose
description: 在内置 spark-workflow 中用于将已确认方向写成当前 mission 的 proposal.md、design.md 和 tasks.md。
---

# OpenSpec Propose（内置版）

把已确认方向转成可执行 artifact。

## 输入

- Align 或 Mini Align 的确认结论
- 相关代码上下文
- 用户提供的 PRD、设计说明、系统分析或截图说明
- 当前 mission 工作区与 `spec/` 目录位置

## 步骤

1. 确认当前子任务名称与产物位置
2. 确认当前 mission 的 `spec/` 目录已存在
3. 读取模板：
   - [../../assets/templates/proposal-template.md](../../assets/templates/proposal-template.md)
   - [../../assets/templates/design-template.md](../../assets/templates/design-template.md)
   - [../../assets/templates/tasks-template.md](../../assets/templates/tasks-template.md)
4. 如果存在外部规格说明，使用 [../../references/spec-to-artifact-mapping.md](../../references/spec-to-artifact-mapping.md) 做映射
5. 写出：
   - `proposal.md`：做什么、为什么做、范围、非目标、边界场景、开放问题
   - `design.md`：结构、接口、数据流、复用点、风险
   - `tasks.md`：小而可验证的任务与验收点
6. 除非用户已明确授权直接实现，否则请求用户确认 artifact
7. 完成后回到外层主 skill，同步状态记录

## 质量标准

- proposal 覆盖所有重要变更点和异常路径
- design 能解释关键技术路径，而不是空泛描述
- tasks 足够原子、有顺序且可独立验证
- 仍有不确定项时，要显式写出来

## 约束

- 不要因为任务感觉简单就跳过 artifact
- 一旦 artifact 已存在，不要继续把聊天历史当最终真相源
- 如果实际上尚未达成一致，应返回 Align
