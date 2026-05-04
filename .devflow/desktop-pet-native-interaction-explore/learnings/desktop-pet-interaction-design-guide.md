# 桌宠交互设计借鉴文档

## 文档目的

这份文档回答一个设计问题：

> 如果我们想做一个“像桌宠”的前端执行层，应该从 VPet 的原生交互逻辑里借鉴什么？

它不是源码逐行说明。源码事实已经沉淀在：

- `learnings/native-interaction-source-analysis.md`

本文更偏设计抽象，服务于后续把 VPet 的桌宠感迁移到当前项目的后端行为引擎（Behavior Engine）、展示控制面（Display Control Surface）或第二阶段协议（Phase 2 Protocol）中。

## 一句话结论

一个好的桌宠不只是“随机播放动画”。

它至少需要同时具备：

- 分层状态机（Layered State Machine）
- 数据驱动动作资源（Data-driven Graph Resources）
- 三段式动画语法（Start/Loop/End Animation Grammar）
- 屏幕世界感知（Screen World Awareness）
- 用户输入反馈闭环（User Feedback Loop）
- 带保底的随机行为调度（Probabilistic Behavior Scheduling with Pity）
- 可扩展行为挂点（Extension Hooks）

VPet 原生逻辑做得比较好的地方，是它把这些能力拆开了，而不是把所有交互都写成一个巨大的 `if/else`。

## 一、VPet 原生设计的核心抽象

### 1.1 分层状态机（Layered State Machine）

VPet 不是单个巨型有限状态机（Finite State Machine）。它至少分三层：

| 层次 | 原生概念 | 作用 |
| --- | --- | --- |
| 生理/情绪模式 | 模式类型（ModeType） | 表达角色当前健康、心情、状态好坏 |
| 活动状态 | 工作状态（WorkingState） | 表达现在在正常、工作、睡觉、旅行还是空状态 |
| 动画状态 | 图形类型（GraphType） | 表达当前正在播默认、移动、说话、摸头、睡觉等哪类动画 |

这很关键。

如果只做一个状态，例如 `idle / moving / talking`，桌宠很快会变得机械。因为“身体在做什么”和“心情是什么”会混在一起。VPet 的做法是：

- 心情差时，默认动画、移动速度、说话表现可以变。
- 当前在工作时，默认态应该回到工作动画，而不是普通呼吸。
- 当前在侧边隐藏时，鼠标进入/离开应该触发探头和缩回，而不是普通摸头。

设计建议：

- 后端应该保留类似三层状态：
  - 内在状态（Internal State）：心情、能量、疲劳、亲密度、打扰程度。
  - 活动状态（Activity State）：空闲、说话、执行任务、休息、工作、被拖拽。
  - 展示状态（Display State）：当前 graph、动画阶段、是否气泡可见、是否贴边隐藏。

### 1.2 数据驱动，而不是代码硬编码

VPet 的角色资源、触摸区域、移动规则、工作项都在配置或资源目录里。

这意味着：

- 换角色时，不必大改逻辑代码。
- 新增动作时，不一定要新增协议字段。
- 行为层可以先问“当前角色有什么资源”，再决定调用什么。

这点对当前项目尤其重要。后续如果进入 `graph.catalog`，本质就是把 VPet 已有的资源目录能力正式暴露给后端。

设计建议：

- 不要继续无限扩 `motion.play` 白名单。
- 应先建立资源目录层（Resource Catalog Layer）：
  - 当前角色有哪些 graph
  - 每个 graph 属于什么类型
  - 是否支持 `A_Start / B_Loop / C_End`
  - 是否适合循环
  - 是否和屏幕移动绑定

### 1.3 统一动作语法（Animation Grammar）

VPet 的动画阶段（AnimatType）很朴素，但非常有价值：

- `A_Start`：动作进入
- `B_Loop`：动作持续
- `C_End`：动作退出
- `Single`：一次性演出

这套语法让桌宠动作有“过程感”：

- 摸头不是立刻切图，而是起手、循环、收尾。
- 拖拽不是窗口跟着鼠标走，而是先进入被提起状态，拖动中持续演出，松手后收尾。
- 说话可以先进入说话 graph，再显示气泡，再持续循环。
- 移动可以先起步，再连续走，再停下。

设计建议：

- 后端编排不要只关心“事件是否发出”，还要关心：
  - 动作是否进入
  - 动作是否正在持续
  - 动作是否退出
  - 是否已经恢复到稳定展示态
- 当前 phase 1 已有 `motion_complete / motion_recovered`，后续可以把它推广为正式展示生命周期（Display Lifecycle）概念。

## 二、自动行为设计

### 2.1 主循环不应该太频繁

VPet 的自动行为由主逻辑轮询定时器（EventTimer）驱动，默认约 15 秒一轮。

这说明桌宠不需要每一秒都“想做点事”。太频繁会烦，太少又死板。

好的桌宠应该像这样：

- 大多数时间安静待着。
- 偶尔动一下。
- 长时间不互动时，表现出一点变化。
- 低状态或特殊事件时才主动提醒。

设计建议：

- 后端行为引擎（Behavior Engine）可以有一个低频 tick，例如 10 到 30 秒。
- tick 只负责“是否考虑发起行为”，不是每次都必须行动。
- 行为应有打扰等级（Disturbance Level）：
  - 低：换待机动作、眨眼、轻微位移
  - 中：移动、探头、短气泡
  - 高：主动打断、长气泡、强提醒

### 2.2 随机要带保底

VPet 的随机行为不是完全平均随机。它会受 `CountNomal` 和互动周期（InteractionCycle）影响。

直观效果是：

- 刚做完动作后，不急着再做。
- 普通默认动画循环久了，就更容易触发新动作。

这是一种“随机 + 保底”的设计。

设计建议：

为每类行为维护一个简单的欲望值（Desire Score）：

| 行为 | 欲望增长 | 欲望归零 |
| --- | --- | --- |
| 换待机动作 | 每个空闲 tick 增长 | 播放任意待机动作后归零 |
| 移动 | 长时间停在同一位置增长 | 移动完成后归零 |
| 主动说话 | 有新上下文或长时间未互动增长 | 说话后归零 |
| 贴边探头 | 已在边缘且用户靠近增长 | 探头后归零 |
| 休息/睡觉 | 疲劳增长 | 进入休息后下降 |

这样比纯随机更像有性格。

### 2.3 自动说话要克制

源码探索里一个重要事实是：VPet 原生核心并不强依赖“闲置时随机自言自语”。它更多是随机姿态、移动、状态提醒。

这点值得借鉴。

如果 AI 桌宠一直主动说话，会很快变成噪音。更好的方式是：

- 平时用身体动作表达存在感。
- 有明确理由时才说话。
- 说话内容要和上下文、状态或用户行为有关。

设计建议：

主动说话应来自：

- 用户刚互动后的反馈
- 任务完成
- 状态异常，例如低电量、疲劳、长时间未休息
- 用户近期目标相关提醒
- 重要记忆被触发
- 节日、时间段、连续使用天数

不建议：

- 无上下文随机输出大段话
- 高频打断用户
- 每次移动都说话

## 三、动作系统设计

### 3.1 动作不是表情别名

VPet 的资源能力很丰富：

- 移动（Move）
- 待机（Idel）
- 说话（Say）
- 摸头（Touch_Head）
- 摸身体（Touch_Body）
- 睡觉（Sleep）
- 状态一/二（StateONE / StateTWO）
- 贴边隐藏（SideHide）
- 工作（Work）
- 吃喝礼物（Eat / Drink / Gift）

这说明动作不应该都塞进 `emotion`。

设计建议：

后续协议要区分：

- 情绪（Emotion）：开心、思考、害羞、疲惫。
- 动作（Motion）：摸头、挥手、坐下、睡觉。
- 资源 graph（Graph）：`walk.right`、`Shining`、`Boring`。
- 行为（Behavior）：贴边隐藏、探头、拖拽、吃东西。

这四类不要混用。

### 3.2 动作要有生命周期

一个动作如果只有“播放一次”，会很难和后端编排稳定衔接。

更好的动作模型是：

```text
准备进入 -> 正在持续 -> 退出收尾 -> 恢复稳定态
```

对应到 VPet：

```text
A_Start -> B_Loop -> C_End -> Default / Work / Sleep
```

设计建议：

后端行为事件可以逐步演进成：

```json
{
  "type": "behavior.invoke",
  "behavior": "touch_head",
  "lifecycle": {
    "wait_until": "recovered",
    "settle_ms": 300
  }
}
```

这比单纯 `motion.play(touch_head)` 更适合复杂故事链路。

### 3.3 资源目录比白名单更重要

当前 phase 1 的 `motion.play / emotion.set` 是小白名单，适合稳定基线。

但如果目标是“让 AI 知道桌宠可以做什么”，就必须有资源目录：

- 当前角色有哪些 graph？
- 哪些 graph 是 Move？
- 哪些 graph 是 Say？
- 哪些支持循环？
- 哪些只适合一次性播放？
- 哪些和移动绑定？

设计建议：

phase 2 优先做资源目录（graph.catalog），再做直接点播（graph.play），最后做高层行为调用（behavior.invoke）。

推荐层次：

1. `graph.catalog`
   - 只报告能力，不改变状态。
2. `graph.play`
   - 直接点播资源，用于调试和低层控制。
3. `behavior.invoke`
   - 封装真正有语义的行为。
4. `display.report`
   - 主动回传当前展示状态。
5. `display.reset`
   - 强制回到稳定态。

## 四、屏幕移动与贴边设计

### 4.1 桌宠需要屏幕世界模型

VPet 的移动之所以有桌宠感，是因为它知道自己和屏幕边缘的关系。

它不是“从 A 点移动到 B 点”的普通 UI 动画，而是在一个桌面世界里活动：

- 离左边还有多远
- 离右边还有多远
- 离顶部还有多远
- 离底部还有多远
- 是否越界
- 是否需要回正
- 是否可以贴边隐藏

设计建议：

当前项目可以抽一个屏幕世界模型（Screen World Model）：

```text
window_rect
screen_rect
move_area_rect
distance_left
distance_right
distance_top
distance_bottom
is_near_edge
is_partially_outside
side_hidden_direction
```

所有移动行为都依赖这个模型，而不是直接散落读写 `left/top`。

### 4.2 移动应该是规则驱动，不是命令驱动

VPet 的 `walk/crawl/climb/fall` 都来自移动规则（Move Rule）：

- graph 名
- 速度
- 触发条件
- 继续条件
- 贴边定位
- 可用情绪状态
- 随机持续长度

设计建议：

可以为后端定义类似结构：

```json
{
  "id": "walk.right",
  "graph": "walk.right",
  "kind": "walk",
  "speed": { "x": 14, "y": 0 },
  "trigger": { "right_gt": 200 },
  "continue": { "right_gt": 100 },
  "allowed_modes": ["happy", "normal"],
  "distance_bias": 7
}
```

这比 `window.move(dx=100)` 更能产生自然桌宠感。

但要注意：这不应替代 phase 1 的 `window.move(dx, dy)`。两者用途不同：

- `window.move`：外部显式位移，稳定、可验证。
- 原生移动规则：角色自己在桌面世界里活动，表现自然但不完全确定。

### 4.3 贴边隐藏是独立行为，不是移动副作用

VPet 的侧边隐藏（SideHide）不是普通移动失败后的随便停住。它有独立 graph：

- `SideHide_Left_Main`
- `SideHide_Left_Rise`
- `SideHide_Right_Main`
- `SideHide_Right_Rise`

这说明贴边隐藏应被设计成高层行为：

```text
进入隐藏 -> 隐藏循环 -> 探头 -> 收回 -> 回正
```

设计建议：

后续如果要做 `behavior.invoke`，可以把这些能力列为第一批候选：

- `sidehide.left`
- `sidehide.right`
- `peek.left`
- `peek.right`
- `recover_from_sidehide`

它们不应只是 `graph.play(SideHide_Left_Rise)`，因为真正行为还包含窗口定位和鼠标进入/离开的状态转换。

### 4.4 移动需要纠偏

桌宠会移动，就必然有边界问题。

VPet 在移动结束时会检查位置，必要时回正，避免窗口长期卡在屏幕外。

设计建议：

任何桌宠移动系统都需要：

- 允许轻微越界
- 禁止完全跑丢
- 结束后做纠偏
- 用户拖拽后也要检查是否贴边或回正
- 提供“重置位置”能力

## 五、用户交互设计

### 5.1 交互区应数据化

VPet 的摸头、摸身体、提起拖拽、捏脸都来自触摸区域（TouchArea）配置。

这比在代码里写：

```text
if y < 200 then touch_head
```

更好。

原因：

- 不同角色体型不同。
- 同一角色不同状态下热点可能不同。
- 新角色只需要配资源和热点。
- 插件或后端可以查询当前可互动区域。

设计建议：

后续可以考虑暴露互动区域目录（Touch Catalog）：

```json
{
  "touch_areas": [
    {
      "id": "head",
      "action": "touch_head",
      "rect": { "x": 159, "y": 16, "w": 189, "h": 178 },
      "trigger": "click"
    },
    {
      "id": "raised",
      "action": "raised",
      "rect": { "x": 0, "y": 50, "w": 500, "h": 200 },
      "trigger": "press"
    }
  ]
}
```

### 5.2 输入要影响状态

VPet 的摸头/摸身体不是只播动画。它还会：

- 统计次数
- 改心情
- 扣一点体力
- 更新模式
- 显示数值变化提示
- 可能触发台词

这就是反馈闭环（Feedback Loop）。

设计建议：

当前项目如果引入用户互动，不要只做：

```text
click head -> play touch_head
```

而应做：

```text
click head
-> play touch_head
-> update relationship / mood
-> maybe trigger memory
-> maybe speak short response
-> reduce future idle silence
```

### 5.3 连续动作比单次点击更有生命力

VPet 通过鼠标划过头部/身体区域触发类似抚摸的效果。这说明好的桌宠不只响应点击，还响应“靠近、停留、拖动、划过”。

设计建议：

可设计输入类型：

- 点击（Click）
- 长按（Press）
- 拖拽（Drag）
- 悬停（Hover）
- 划过（Wave）
- 离开（Leave）
- 靠近屏幕边缘（Near Edge）

其中悬停、划过、离开非常适合低打扰反馈。

### 5.4 右键菜单是工具，不是主体验

VPet 对本体右键是工具栏，对托盘右键是完整菜单。

这说明桌宠的主体验应该在身体交互里完成，菜单只是配置与管理入口。

设计建议：

- 主体验：摸、拖、说话、移动、贴边、探头。
- 工具入口：置顶、鼠标穿透、重置位置、设置、退出。
- 不要让用户为了触发常用桌宠行为频繁打开菜单。

## 六、一个好的桌宠可以做到什么

下面按能力层分类。

### 6.1 基础存在感

最低限度应该具备：

- 默认呼吸或待机循环
- 偶尔切换待机动作
- 能说话
- 能响应点击
- 能被拖动
- 能恢复默认状态

### 6.2 桌面世界能力

更像桌宠的能力：

- 自主走动
- 爬墙
- 贴顶
- 下落
- 贴边隐藏
- 鼠标靠近时探头
- 离开时缩回
- 防止跑出屏幕
- 支持自定义移动范围

### 6.3 用户互动能力

有互动感的能力：

- 摸头
- 摸身体
- 捏脸
- 提起拖拽
- 长按反馈
- 鼠标划过反馈
- 点击说话
- 根据互动次数和近期状态调整回应

### 6.4 生活感能力

更完整的桌宠能力：

- 吃饭
- 喝水
- 收礼物
- 工作
- 学习
- 玩耍
- 睡觉
- 升级
- 节日演出
- 生日演出
- 状态异常提醒

### 6.5 AI 项目增强能力

当前项目可以比原生 VPet 多做：

- 根据记忆选择动作
- 根据对话情绪选择 graph
- 根据任务状态改变待机行为
- 根据用户专注状态降低打扰
- 根据长期互动形成习惯
- 根据屏幕位置选择合适表现

## 七、迁移到当前项目的推荐架构

### 7.1 四层架构

建议把桌宠交互拆成四层：

```text
行为决策层（Behavior Decision Layer）
展示资源层（Display Resource Layer）
屏幕移动层（Screen Movement Layer）
用户反馈层（User Feedback Layer）
```

### 7.2 行为决策层（Behavior Decision Layer）

负责回答：

- 现在要不要做点什么？
- 做什么不会打扰用户？
- 当前行为是否和用户上下文有关？
- 是否需要说话？
- 是否只做身体动作？

输入：

- 用户最近互动
- 对话上下文
- 记忆召回
- 当前心情/能量
- 当前展示状态
- 屏幕位置
- 当前打扰预算

输出：

- `bubble.show`
- `graph.play`
- `behavior.invoke`
- `window.move`
- `display.reset`

### 7.3 展示资源层（Display Resource Layer）

负责回答：

- 当前角色有哪些 graph？
- 哪些可循环？
- 哪些适合说话？
- 哪些适合移动？
- 哪些只是一次性演出？

建议从 `graph.catalog` 开始。

### 7.4 屏幕移动层（Screen Movement Layer）

负责回答：

- 当前窗口在哪里？
- 离边缘多远？
- 能不能走？
- 能不能贴边？
- 是否需要回正？
- 当前移动是外部显式控制，还是桌宠自主行为？

关键边界：

- `window.move` 是确定性位移。
- 原生移动规则是表现性行为。
- 两者不要混在一个语义里。

### 7.5 用户反馈层（User Feedback Layer）

负责回答：

- 用户做了什么？
- 这次互动影响哪些状态？
- 是否触发短回应？
- 是否写入记忆？
- 是否改变后续行为概率？

建议事件结构：

```json
{
  "input": "touch_head",
  "source": "user",
  "effect": {
    "mood_delta": 1,
    "energy_delta": -1,
    "relationship_delta": 0.2
  },
  "response": {
    "behavior": "touch_head",
    "say": "嘿嘿。"
  }
}
```

## 八、不建议直接照搬的部分

### 8.1 不建议把原生移动直接塞回 `window.move`

原因：

- `window.move(dx, dy)` 是确定性协议。
- 原生 move system 是环境驱动的表现系统。
- 混在一起会导致“我只想移动 120 像素，结果它开始爬墙”。

建议：

- 保留 `window.move` 的确定性。
- 另开 `behavior.invoke(native_walk)` 或 `graph.play(walk.right)` 这类表现入口。

### 8.2 不建议继续堆 emotion alias

原因：

- `shy`、`think`、`pinch` 这类词很容易变成跨角色不稳定语义。
- 角色资源不同，graph 名不同。
- 扩 alias 会掩盖“资源目录缺失”的真正问题。

建议：

- phase 1 保持小 alias。
- phase 2 用 catalog 和 graph play 解决资源可见性。

### 8.3 不建议让 AI 高频主动说话

原因：

- 桌宠的存在感主要来自身体表现，不是一直输出文字。
- 主动说话容易打扰用户。
- 无上下文说话会削弱人格可信度。

建议：

- 多用低打扰动作。
- 有理由时再说话。
- 说话要短，并可被用户打断或忽略。

### 8.4 不建议只做菜单型交互

原因：

- 桌宠主体验应来自身体交互。
- 菜单只能作为配置工具。

建议：

- 把常见互动设计在角色身体上。
- 菜单只放设置、重置、退出、置顶、鼠标穿透。

## 九、后续路线建议

### 9.1 短期：补设计理解，不急着实现

当前已经有 phase 1 稳定协议，不需要马上改代码。

短期更适合继续梳理：

- 哪些原生能力要进入 phase 2
- 哪些能力只做 dev-only
- 哪些能力应该由后端行为引擎调度
- 哪些能力仍由 VPet 原生保持自主

### 9.2 中期：先做 graph catalog

推荐下一步如果进入实现：

1. `graph.catalog`
2. `graph.play`
3. `display.report`
4. `display.reset`
5. `behavior.invoke`

原因：

- 没有 catalog，后端不知道身体层能做什么。
- 没有 report，后端不知道身体层做到哪了。
- 没有 reset，长链路容易卡在中间态。

### 9.3 长期：建立后端行为引擎

最终可以形成：

```text
记忆/任务/对话上下文
-> 行为决策层
-> 展示资源选择
-> 动作生命周期编排
-> VPet 执行
-> 状态回传
-> 更新后续行为概率
```

这时 VPet 就不只是“被后端点播动画”，而是一个有身体、有位置、有习惯、有反馈的桌宠执行层。

## 十、最小可复刻模型

如果只想先做一个最小但像样的桌宠，可以先实现这 8 个能力：

1. 默认呼吸循环
2. 低频随机待机动作
3. 触摸区域配置
4. 摸头反馈
5. 长按拖拽
6. 确定性窗口移动
7. 贴边隐藏 + 探头
8. 动作生命周期等待

这 8 个比“做 100 个表情 alias”更重要。

## 总结

VPet 原生设计最值得借鉴的不是某个具体动画，而是一套组合方式：

- 用状态让角色有内在变化。
- 用资源目录让角色能力可枚举。
- 用三段式动画让动作有过程。
- 用屏幕边缘让角色活在桌面世界里。
- 用输入反馈让用户行为改变角色。
- 用低频随机和保底机制让它偶尔主动，但不烦。

当前项目如果沿这个方向走，后续 phase 2 应该围绕 `graph.catalog / graph.play / behavior.invoke / display.report / display.reset` 展开，而不是继续把所有能力压进 `motion.play` 和 `emotion.set`。
