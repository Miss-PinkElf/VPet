# 任务工作流

## 任务目标
- 分析 VPet 原生桌宠交互逻辑（Native Desktop Pet Interaction Logic），理解它如何做到随机动作、自动移动、贴边、触摸反馈、拖拽和状态切换。
- 将源码事实整理成后续可借鉴的桌宠设计模型（Desktop Pet Design Model）。

## 范围边界
- 范围内：
  - 原生自动行为（Autonomous Behavior）
  - 随机动作与状态机（Random Action and State Machine）
  - 移动与贴边（Movement and Side Hide）
  - 用户交互（User Interaction）
  - 动作资源与播放管线（Graph and Animation Pipeline）
- 范围外：
  - 不修改现有桥接插件（AgentBridge）
  - 不实现新协议
  - 不替用户做真实 GUI 联调
  - 不进入 phase 2 控制面实现

## 当前阶段
- 阶段：Explore
- 路径：devflow 纯探索分支（Explore Branch）

## 成功标准
- 能用源码事实说明 VPet 原本的桌宠交互模型。
- 能回答“一个好的桌宠可以做到什么、怎么做到”。
- 能沉淀可借鉴能力清单和后续可进入 Align 的候选方向。

