# VPet 原生桌宠交互逻辑源码分析

## 结论摘要

VPet 的桌宠感不是靠一个“随机动作函数”实现的，而是由几层机制叠加出来：

- 分层状态机（Layered State Machine）
- 周期行为调度（Periodic Behavior Scheduling）
- 数据驱动动作资源（Data-driven Graph Resources）
- 条件移动规则（Conditional Move Rules）
- 屏幕边缘感知（Screen Edge Awareness）
- 热点交互与反馈闭环（Touch Hotspot and Feedback Loop）

## 核心源码事实

### 1. 自动行为

- 主逻辑轮询定时器（EventTimer）定义在 `VPet-Simulator.Core/Display/MainLogic.cs`。
- 空闲判定（IsIdle）成立时，`EventTimer_Elapsed()` 会随机选择：
  - 移动（Move）
  - 普通待机（Idle）
  - 待机状态一（StateONE）
  - 一次性睡觉动画（Sleep）
  - 扩展随机交互（RandomInteractionAction）
- 这里不是纯随机，`CountNomal` 与互动周期（InteractionCycle）会让“太久没发生新动作”之后更容易触发变化。

### 2. 动作系统

- 动作资源通过图形核心（GraphCore）组织：
  - `GraphType -> graph 名集合`
  - `graph 名 -> AnimatType -> IGraph 列表`
- 图形类型（GraphType）定义了动作类别，例如：
  - `Default`
  - `Move`
  - `Idel`
  - `Touch_Head`
  - `Touch_Body`
  - `Sleep`
  - `Say`
  - `StateONE`
  - `StateTWO`
  - `SideHide_Left_Main`
  - `SideHide_Right_Main`
- 动画阶段（AnimatType）统一为：
  - `Single`
  - `A_Start`
  - `B_Loop`
  - `C_End`

## 移动与贴边

### 移动链路

VPet 的移动不是随机瞬移，而是：

1. 从移动配置（GraphConfig.Moves）中随机挑一个候选移动。
2. 用触发条件（Triggered）判断当前屏幕位置是否允许。
3. 播放移动 graph 的起始阶段（A_Start）。
4. 如果允许真实移动，启动位移动画定时器（MoveTimer）。
5. 定时调用窗口控制器（IController/MWController）的 `MoveWindows(...)`。
6. 移动过程中用继续条件（Checked）判断是否还能走。
7. 结束前可能选择方向兼容的下一段移动。
8. 播放结束阶段（C_End），回默认态或进入贴边隐藏。

### 贴边与探头

- 屏幕距离不直接散落在行为代码里，而是统一通过窗口控制器（IController）读取：
  - 左边距离
  - 右边距离
  - 顶部距离
  - 底部距离
- 当移动或拖拽结束后，会检查是否靠边过深。
- 如果左/右边越界并且存在侧边隐藏 graph，就进入侧边隐藏（SideHide）。
- 鼠标进入侧边隐藏区域时，切到探头（Rise）动画。
- 鼠标离开后，播放收回动画，再回隐藏主循环。
- 点击隐藏状态下的本体，会把窗口拉回屏内并恢复正常。

## 用户交互

### 热点配置

VPet 的触摸区域（TouchArea）不是硬编码在点击函数里，而是从角色配置中读入：

- 摸头区域（Touch Head）
- 摸身体区域（Touch Body）
- 提起拖拽区域（Raised）
- 捏脸区域（Pinch）

核心角色 `vup` 的热点配置在 `VPet-Simulator.Windows/mod/0000_core/pet/vup.lps`。

### 输入分流

- 左键按下后先等待长按阈值（Press Length）。
- 长按命中长按区域时，触发拖拽或捏脸。
- 普通点击命中头部/身体时，触发摸头/摸身体。
- 鼠标在头部/身体区域反复划过，也会触发类似抚摸的反馈。
- 右键本体显示工具栏；托盘右键提供完整系统菜单。

## 当前角色 vup 可做什么

### 移动类

- `walk.left`
- `walk.right`
- `walk.left.slow`
- `walk.right.slow`
- `walk.left.faster`
- `walk.right.faster`
- `crawl.left`
- `crawl.right`
- `climb.left`
- `climb.right`
- `climb.top.left`
- `climb.top.right`
- `fall.left`
- `fall.right`

### 交互类

- 摸头
- 摸身体
- 提起拖拽
- 捏脸
- 侧边隐藏
- 探头

### 状态与演出类

- 默认呼吸
- 普通待机
- StateONE / StateTWO
- 睡觉
- 说话
- 思考
- 开机 / 关机
- 升级
- 音乐
- 节日 / 生日演出

### 工作与物品类

- 工作
- 学习
- 玩耍
- 吃饭
- 喝水
- 送礼

## 可借鉴设计模型

如果要做一个“好的桌宠”，最值得借鉴的是：

1. 分层状态机（Layered State Machine）
   - 生理/情绪模式（ModeType）
   - 活动状态（WorkingState）
   - 当前动画状态（GraphType）

2. 数据驱动资源目录（Data-driven Graph Catalog）
   - 动作、触摸区、移动规则、持续时间都放配置。
   - 换角色时尽量不改行为代码。

3. 三段式动作语法（Start/Loop/End Animation Grammar）
   - 所有动作都尽量拆成起手、循环、收尾。
   - 后端编排也应理解“动作完成”和“恢复稳定态”的区别。

4. 屏幕世界感（Screen World Awareness）
   - 行为要知道屏幕边缘、移动范围和窗口位置。
   - 走路、爬墙、贴边、探头都来自这个世界模型。

5. 反馈闭环（Feedback Loop）
   - 用户输入不只是播放动画。
   - 它应同时影响情绪、数值、台词、统计和后续行为概率。

6. 扩展槽（Extension Hooks）
   - 随机行为、说话处理、触摸区域、时间轮询都应可挂载扩展。

## 对当前项目的启发

当前 bridge mission 的 phase 1 已经有 `bubble.show / motion.play / mode.switch / emotion.set / window.move`，但如果要真正复刻桌宠感，后续不应只继续扩白名单。

更合理的方向是把能力分成：

- 行为决策层（Behavior Decision Layer）
- 展示资源层（Display Resource Layer）
- 屏幕移动层（Screen Movement Layer）
- 用户反馈层（User Feedback Layer）

这和既有 phase 2 预研里的 `graph.catalog -> graph.play -> behavior.invoke` 是一致的。
