# 当前状态

## 当前阶段
- 阶段：Explore
- 当前目标：已完成原生桌宠交互逻辑探索；当前等待后续 Align，决定实现方向。

## 已确认事实
- 本 mission 与 `.devflow/desktop-pet-vpet-body-bridge/` 分离。
- 本轮只做源码探索和设计理解，不进行代码实现。
- 用户允许使用并行子代理（Subagents），并指定可使用 `gpt-5.4` 与 high 思考。
- VPet 原生桌宠感主要来自分层状态机（Layered State Machine），而不是单个巨型状态机。
- 自动行为由主逻辑轮询定时器（EventTimer）驱动，移动由位移动画定时器（MoveTimer）执行真实窗口位移。
- 动作系统以图形类型（GraphType）和动画阶段（AnimatType）组织，核心语法是 `A_Start -> B_Loop -> C_End`。
- 移动系统由移动配置（GraphConfig.Moves）、窗口控制器（IController/MWController）和移动规则（Move）共同实现。
- 触摸、拖拽、捏脸等交互通过触摸区域（TouchArea）数据化注册，不直接写死在点击分支里。

## 当前探索问题
- VPet 原生如何随机行动、随机说话或切换动作？
- VPet 如何通过 move graph 实现走路、爬行、跌落和贴边？
- 用户交互如何触发摸头、摸身体、拖拽、菜单等反馈？
- 哪些机制值得后端桌宠项目借鉴？

## 下一步
- 如需进入实现方向，先进入 Align，讨论是否把 VPet 的原生交互机制抽象成后端行为引擎（Behavior Engine）或 phase 2 展示控制方案。

## 最新沉淀
- `learnings/native-interaction-source-analysis.md`
- `learnings/desktop-pet-interaction-design-guide.md`

## 最新 handoff
- `handoffs/2026-05-04-001-explore-wrap-up.md`
