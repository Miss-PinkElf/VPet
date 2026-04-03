---
name: superpowers-verification-before-completion
description: 在内置 spark-workflow 中，在任何完成声明、任务关闭或归档前使用，强制拿到新的验证证据。
---

# Superpowers Verification Before Completion（内置版）

没有新证据，就不要声称完成。

## 必过门禁

1. 先识别哪个命令或检查能够证明当前结论
2. 现在就运行它
3. 读取真实输出与退出状态
4. 把结果与 `proposal.md` 和 `tasks.md` 对齐
5. 只有这样，才能说明哪些通过了、哪些还没通过

## 证据清单

- 任务清单状态
- 编译、类型检查、测试、lint 或构建输出（按需）
- 改动流程的运行时行为证据
- 空状态、加载态、错误态、边界态的人工 spot-check（如适用）

## 约束

- “应该可以”不是证据
- 局部验证不足以支持全局完成声明
- 如果验证失败，根据失败来源回到 Apply 或 Propose
