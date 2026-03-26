# agent-desktop-pet 工作流参考

## 1. 你现在需要做什么

如果你已经完成：

- 桌宠前端展示
- hover 边框与 toolbar
- 拖拽和缩放
- 边框、模型、toolbar 联动缩放

那么当前默认下一步就是：

1. 不再继续打磨前端展示细节
2. 进入“简单对话 + 后端最小闭环”
3. 用 superspec 推进 `Task 5` 和 `Task 6`
4. 为这一轮建立新的专项过程记录

推荐动作顺序：

1. 读取 `.codex/explore/desktop-pet-graduation-roadmap/handoff.md`
2. 读取 `.codex/explore/desktop-pet-graduation-roadmap/state.md`
3. 查看 `openspec/changes/desktop-pet-companion-roadmap/tasks.md`
4. 创建 `.codex/explore/desktop-pet-chat-backend/`
5. 进入 superspec 做：
   - 前端简单对话入口
   - Python 后端最小回复接口
   - 前后端联调

## 2. 新需求工作流

适用场景：

- 新功能
- 新页面
- 新模块
- 新阶段目标

例如：

- 接入简单对话
- 接入记忆系统
- 增加设置页
- 增加答辩模式

流程：

1. 先更新全局 `.codex/explore/desktop-pet-graduation-roadmap/state.md`
2. 读取 OpenSpec：
   - `proposal.md`
   - `design.md`
   - `tasks.md`
3. 如果边界不清楚，先走 superspec 的 Align / Propose
4. 把任务拆进 `tasks.md`
5. 建专项目录：
   - `.codex/explore/desktop-pet-<topic>/`
6. 实现完成后回写：
   - 专项 `state.md`
   - 全局 `state.md`
   - 全局 `decision-log.md`
   - 全局 `learnings.md`
   - OpenSpec `tasks.md`

## 3. Bug 修复工作流

适用场景：

- 页面报错
- 联调失败
- 模型异常
- 状态错乱
- UI 失效

流程：

1. 先判断 bug 是局部问题还是阶段阻塞
2. 建或进入专项 debug 目录
3. 用这个结构记录：
   - 问题现象
   - 根因分析
   - 解决方案
   - 验证结果
4. 如果只是实现问题，直接修
5. 如果暴露设计缺口，先改 OpenSpec 的 `design.md` / `tasks.md`
6. 修完后至少回写：
   - 专项 `state.md`
   - 专项 `handoff.md`
   - 全局 `learnings.md`

## 4. 只记录不开发的工作流

适用场景：

- 更新阶段状态
- 做 checkpoint
- 做 handoff
- 整理论文材料
- 准备答辩材料

流程：

1. 不进入实现
2. 优先更新全局目录：
   - `state.md`
   - `decision-log.md`
   - `learnings.md`
   - `handoff.md`
3. 如果影响阶段完成度，再同步 `tasks.md`

## 5. 阶段切换工作流

适用场景：

- 前端阶段完成，转入后端联调
- 简单对话完成，转入记忆系统
- 开始准备答辩

流程：

1. 修改全局 `state.md` 的“当前阶段”
2. 在 `decision-log.md` 写清楚为什么切换
3. 在 `handoff.md` 更新当前目标和下一步
4. 在 `tasks.md` 标出新的主线任务
5. 为新阶段建立新的专项目录

## 6. 什么情况下要用 superspec

默认要用 superspec：

- 新功能实现
- 前后端联调
- 影响多个文件的 UI/交互改动
- 任何需要 proposal / design / tasks 的实现任务

可以只用 context-budget-explore：

- 纯记录
- 纯进度同步
- 纯经验沉淀
- checkpoint / handoff

一句话判断：

- 要做功能 -> superspec
- 要管阶段和过程 -> context-budget-explore

## 7. 每轮结束最少要做什么

最少补四件事：

1. 本轮完成了什么
2. 本轮为什么这样做
3. 还有什么没解决
4. 下一步是什么

如果这一轮有代码实现，再补：

1. OpenSpec `tasks.md`
2. 专项 `handoff.md`
3. 全局 `learnings.md`

## 8. 推荐开场模板

### 做新功能

> 继续桌宠毕设，这轮做 xxx。先读 `.codex/explore/desktop-pet-graduation-roadmap` 和 OpenSpec，再用 superspec 推进。

### 修 bug

> 继续桌宠毕设，这轮修 xxx。先读全局 roadmap，再建专项 debug 目录处理。

### 只更新记录

> 继续桌宠毕设，这轮不开发，帮我更新阶段状态、任务进度和 handoff。

### 整理论文/答辩材料

> 基于 `.codex/explore/desktop-pet-graduation-roadmap` 和 OpenSpec，帮我整理当前阶段成果和问题，输出论文/答辩可用材料。
