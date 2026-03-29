# VPet 展示层可控范围与全控方案

## 目的

这份文档服务于 `desktop-pet-vpet-body-bridge` mission 的进一步探索，回答三个问题：

1. `VPet` 前端展示层本体里，到底有哪些东西能被“点出来”
2. 当前桥接为什么只暴露了其中一小部分
3. 如果目标是“尽量把展示层都纳入后端控制”，技术上是否可行，以及应该怎样做

这份文档不是 phase 1 正式协议清单的替代品。

- `protocol-phase1.md` 负责记录“当前已经正式承诺的最小协议”
- 本文负责记录“展示层真实控制面、缺口分析和扩展方案”

## 结论摘要

- 以“视觉上把现有展示资源都点出来”为目标，基本可行，且现有 `VPet` 底层能力已经足够支撑
- 以“把所有展示能力都包装成稳定的后端控制协议”为目标，也可行，但不能继续只靠当前 `motion.play / emotion.set / mode.switch` 的少量硬编码白名单
- 最合理的方向不是继续扩大当前白名单，而是把控制能力分成三层：
  - 资源目录层：告诉后端“当前角色到底有哪些 graph”
  - 直接点播层：允许后端按 graph 名和动画阶段直接播放
  - 行为语义层：对贴边、探头、摸头、拖拽等复杂行为做高层封装

## 事实来源

本轮结论主要来自以下真相源：

- `VPet.Plugin.AgentBridge/AgentBridgePoller.cs`
- `VPet.Plugin.AgentBridge/AgentBridgeEvent.cs`
- `VPet-Simulator.Core/Graph/GraphInfo.cs`
- `VPet-Simulator.Core/Graph/GraphCore.cs`
- `VPet-Simulator.Core/Display/MainDisplay.cs`
- `VPet-Simulator.Core/Display/MainLogic.cs`
- `VPet-Simulator.Core/Display/Main.xaml.cs`
- `VPet-Simulator.Windows/MainWindow.cs`
- `VPet-Simulator.Windows/WinDesign/winConsole.xaml`
- `VPet-Simulator.Windows/WinDesign/winConsole.xaml.cs`
- `VPet-Simulator.Windows/mod/0000_core/pet/vup.lps`
- `VPet-Simulator.Windows/mod/0000_core/pet/vup/`

本轮没有只依赖迁移文档或人工映射，而是回到源码和当前角色资源目录做了核对。

## 一、前端展示层本体的真实可控面

### 1.1 类型级展示能力

`GraphInfo.GraphType` 定义了展示层里存在的主要类型。

当前与身体层控制最相关的类型包括：

- `Default`
- `Move`
- `Touch_Head`
- `Touch_Body`
- `Idel`
- `Sleep`
- `Say`
- `StateONE`
- `StateTWO`
- `StartUP`
- `Shutdown`
- `Work`
- `Switch_Up`
- `Switch_Down`
- `Switch_Hunger`
- `Switch_Thirsty`
- `Raised_Dynamic`
- `Raised_Static`
- `SideHide_Left_Main`
- `SideHide_Left_Rise`
- `SideHide_Right_Main`
- `SideHide_Right_Rise`
- `Common`

这些类型意味着：前端展示层并不只是“几个动作和几个表情”，而是已经具备移动、待机、工作、侧边隐藏、探头、睡眠、启动、关机、切换提示等完整表现域。

### 1.2 当前角色 `vup` 的资源级展示能力

当前 `vup` 角色资源目录已确认存在以下展示分类：

- `BDay`
- `Default`
- `Drink`
- `Eat`
- `Gift`
- `IDEL`
- `LevelUP`
- `MOVE`
- `Music`
- `newyear`
- `Pinch`
- `Raise`
- `Say`
- `Shutdown`
- `SideHide_Left_Main`
- `SideHide_Left_Rise`
- `SideHide_Right_Main`
- `SideHide_Right_Rise`
- `Sleep`
- `StartUP`
- `State`
- `Switch`
- `Think`
- `Touch_Body`
- `Touch_Head`
- `WORK`

这说明当前角色资源本身已经覆盖：

- 基础默认态
- 多种待机态
- 多种移动态
- 交互态
- 贴边隐藏与探头态
- 工作 / 学习 / 玩耍态
- 特殊演出态
- 物品演出态

### 1.3 当前角色的具体 graph 名

以下 graph 名已经从资源目录和配置文件中确认存在，适合后续作为 `graph.play` 或 catalog 的候选项。

#### 1.3.1 `MOVE`

- `climb.left`
- `climb.right`
- `climb.top.left`
- `climb.top.right`
- `crawl.left`
- `crawl.right`
- `fall.left`
- `fall.right`
- `walk.left`
- `walk.left.faster`
- `walk.left.slow`
- `walk.right`
- `walk.right.faster`
- `walk.right.slow`

#### 1.3.2 `IDEL`

- `amusement_B`
- `aside`
- `Boring`
- `Bubbles`
- `Meow`
- `meowlook`
- `Squat`
- `Tennis`
- `yawning`

#### 1.3.3 `WORK`

- `WorkONE`
- `WorkClean`
- `WorkTWO`
- `Study`
- `StudyTWO`
- `PlayONE`
- `RemoveObject`
- `RopeSkipping`
- `Calligraphy`
- `StudyPaint`

#### 1.3.4 `Say`

- `Self`
- `Serious`
- `Shining`
- `Shy`

#### 1.3.5 其他重要分类

- `Think`
- `Pinch`
- `Touch_Head`
- `Touch_Body`
- `Sleep`
- `StartUP`
- `Shutdown`
- `StateONE`
- `StateTWO`
- `Switch.Up`
- `Switch.Down`
- `Switch.Hunger`
- `Switch.Thirsty`
- `SideHide_Left_Main`
- `SideHide_Left_Rise`
- `SideHide_Right_Main`
- `SideHide_Right_Rise`
- `Music`
- `BDay`
- `LevelUP`

说明：

- 上述部分名字来自目录名，部分来自 `vup.lps` 中的 `graph#...`
- 实际运行时仍应以 `GraphCore` 注册进来的 graph 目录为准，而不是只信任文件夹名字

## 二、当前桥接已经暴露了什么

当前桥接正式识别的事件类型有：

- `bubble.show`
- `emotion.set`
- `motion.play`
- `mode.switch`
- `window.move`
- `move.intent`

当前桥接中已经做成直接白名单的动作 / 表情 / 模式包括：

### 2.1 `motion.play`

- `idle`
- `move`
- `normal`
- `touch_head`
- `touch_body`
- `sleep`
- `raised`
- `state_one`
- `pinch`
- `thinking`

### 2.2 `emotion.set`

- `think`
- `thinking`
- `pinch`
- `shy -> pinch`

### 2.3 `mode.switch`

- `thinking`
- `normal`

### 2.4 `bubble.show`

除 `text` 外，还可带：

- `motion`
- `expression`
- `emotion`
- `graph`

当前插件里最重要的事实是：

- `bubble.show` 已支持直接传 `graph`
- `emotion.set` 仍只做了很小的语义映射
- 桥接白名单远小于前端展示层本体能力

## 三、哪些能力“本体能做，但当前桥接还没正式暴露”

以下能力已经能从 `VPet` 本体和当前角色资源中确认存在，但当前桥接协议还没有正式暴露成稳定入口。

### 3.1 类型级能力存在，但没有高层桥接 alias

- `StateTWO`
- `StartUP`
- `Shutdown`
- `LevelUP`
- `Music`
- `Switch_Up`
- `Switch_Down`
- `Switch_Hunger`
- `Switch_Thirsty`
- `SideHide_Left_Main`
- `SideHide_Left_Rise`
- `SideHide_Right_Main`
- `SideHide_Right_Rise`

### 3.2 资源级 graph 存在，但只能靠底层点播

- 全部 `IDEL` graph
- 全部 `MOVE` graph
- 全部 `WORK` graph
- 大部分 `Say` graph

### 3.3 行为级能力存在，但当前没有统一外部协议

- 贴边隐藏
- 左探头 / 右探头
- 侧边隐藏后的恢复
- 拖拽中状态
- 更细粒度的工作态视觉切换
- 进入 `StateTWO`

## 四、哪些能力可以“直接点播”，哪些能力需要“行为封装”

这一步非常关键。

如果不把两类能力分开，后续协议一定会混乱。

### 4.1 适合直接点播的能力

这类能力可以近似理解为“知道 graph 名，就可以点出来”。

适合纳入 `graph.play` 的能力：

- `IDEL` 细分待机 graph
- `MOVE` 细分移动 graph
- `WORK` 细分工作 graph
- `Say` graph
- `Think`
- `Pinch`
- `Music`
- `LevelUP`
- `StartUP`
- `Shutdown`
- `Switch_*`
- `SideHide_*`

原因：

- `Main.Display(string name, AnimatType, ...)` 已支持按 graph 名播放
- `GraphCore` 已支持按 graph 名查找资源
- 当前控制台工具本身就可以枚举 graph 并播放

### 4.2 不适合只靠直接点播的能力

这类能力即使表面上能靠 graph 名“播出外观”，也不等于真正完成了原行为。

应纳入 `behavior.invoke` 的能力：

- `touch_head`
- `touch_body`
- `pinch`
- `raised`
- `sleep`
- `state_one`
- `state_two`
- `sidehide_left`
- `sidehide_right`
- `peek_left`
- `peek_right`
- `recover_from_sidehide`

原因：

- `DisplayTouchHead` / `DisplayTouchBody` 包含循环续播与数值变更
- `DisplayRaised` 依赖鼠标位置与拖拽过程
- `MoveSideHideCheck()` 不只是播图，还伴随窗口重定位
- `MainGrid_MouseEnter / Leave` 管理探头与收回
- `StateONE -> StateTWO` 原本就是一段内部状态流转，不只是单图展示

### 4.3 暂不建议纳入第一批统一协议的能力

- `Eat`
- `Drink`
- `Gift`

原因：

- 这三类是物品演出，通常包含前景 / 后景叠层与额外资源
- 它们更适合后续单独设计为 `effect.play` 或 `item.play`
- 当前如果硬塞进通用 `graph.play`，协议会被食物 / 礼物这类特例污染

## 五、全控是否可行

### 5.1 结论

可行，但要明确“全控”到底指什么。

#### 若“全控”定义为：

- 后端可枚举当前角色的展示资源
- 后端可直接点播大部分视觉 graph
- 后端可通过高层行为接口触发复杂交互表现

那么结论是：

- 高可行

#### 若“全控”定义为：

- 当前所有展示能力都直接归并进少量 `motion` / `emotion` 语义词
- 不区分 graph 点播和高层行为

那么结论是：

- 不建议

原因不是做不到，而是这种协议会迅速失真：

- graph 名和行为语义会混在一起
- 换角色就会崩
- 一些行为本来就不是单图
- 后续维护成本会越来越高

### 5.2 可行性的核心依据

#### 依据一：资源可枚举

`GraphCore` 维护：

- `GraphsName`
- `GraphsList`

这已经是天然的 catalog 数据源。

#### 依据二：展示可按名字播放

`Main.Display(string name, AnimatType, ...)` 已经说明：

- 前端并不是只能按 `GraphType` 播
- 只要 graph 存在，就能按名字查找并显示

#### 依据三：说话可附带 graph

`Main.Say(text, graphname, force)` 已具备：

- 说话时附带指定 graph

这意味着说话表情层本身并不需要重新发明新机制。

#### 依据四：复杂行为已有高层方法

以下能力都已在原生代码中具备高层入口：

- `DisplayTouchHead()`
- `DisplayTouchBody()`
- `DisplaySleep()`
- `DisplayRaised()`
- `DisplayToIdel_StateONE()`
- 侧边隐藏检查与探头逻辑

所以扩协议并不要求深改 `GameCore`。

## 六、当前桥接的核心缺口

### 6.1 缺口一：白名单过窄

当前协议只能控制：

- 少量 `motion`
- 少量 `emotion`
- 少量 `mode`

这导致：

- 后端无法感知展示层完整能力
- 很多 graph 实际存在，但永远到不了后端

### 6.2 缺口二：没有展示资源目录

当前后端和联调页面都缺少一个官方入口，来回答：

- 当前角色有哪些 graph
- 每个 graph 支持哪些 `AnimatType`
- 哪些只适合 `Single`
- 哪些适合循环

### 6.3 缺口三：资源点播和行为语义混在一起

例如：

- `walk.left` 是 graph
- `touch_head` 是高层行为
- `peek_left` 是带上下文的交互语义

这三类不应该混在一个简单的 `motion` 字段里。

### 6.4 缺口四：状态回传还没有对“展示目录控制”做准备

当前状态回传足够支撑 phase 1 联调，但还不足以很好服务“展示目录 + 直接点播 + 行为层”的完整闭环。

后续如果进入全控阶段，建议补充：

- `current_graph_name`
- `current_graph_type`
- `current_animat`
- `is_side_hidden`
- `side_hidden_direction`
- `is_peeking`

## 七、推荐的分层方案

### 7.1 第一层：`graph.catalog`

用途：

- 暴露当前角色真实可播放的展示目录

建议返回字段：

- `graph_type`
- `graph_name`
- `animat_types`
- `mode_types`
- `safe_loop`
- `source_role`

最直接的数据来源：

- `Core.Graph.GraphsName`
- `Core.Graph.FindGraphs(...)`

效果：

- 后端不再靠人工记 graph 名
- 调试页可以动态渲染所有可播放项
- 后续换角色也能复用同一套机制

### 7.2 第二层：`graph.play`

用途：

- 按 graph 名和动画阶段直接点播视觉资源

建议协议：

```json
{
  "type": "graph.play",
  "name": "walk.right",
  "animat": "A_Start",
  "reset_after": true
}
```

或：

```json
{
  "type": "graph.play",
  "name": "Shining",
  "graph_type": "Say",
  "animat": "A_Start",
  "loop_mode": "follow_resource"
}
```

适合覆盖：

- `IDEL`
- `MOVE`
- `WORK`
- `Think`
- `Pinch`
- `Music`
- `StartUP`
- `Shutdown`
- `Switch_*`
- `SideHide_*`

### 7.3 第三层：`say.play`

用途：

- 统一“消息 + 指定说话 graph”

建议协议：

```json
{
  "type": "say.play",
  "text": "我想到了。",
  "graph": "Shining",
  "force": true
}
```

说明：

- 它本质上是对 `Main.Say(text, graphname, force)` 的正式封装
- 可以和现有 `bubble.show` 并存
- 如果不想增加新事件，也可以把 `bubble.show(graph=...)` 继续作为 phase 2 的过渡实现

### 7.4 第四层：`behavior.invoke`

用途：

- 触发不适合只靠 graph 点播的复杂高层行为

建议第一批支持：

- `touch_head`
- `touch_body`
- `pinch`
- `sleep`
- `raised`
- `state_one`
- `state_two`
- `sidehide_left`
- `sidehide_right`
- `peek_left`
- `peek_right`
- `recover_from_sidehide`
- `switch_hunger`
- `switch_thirsty`
- `startup`
- `shutdown`
- `music`
- `levelup`

注意：

- 这里的 `startup / shutdown / music / levelup` 是否走 `behavior.invoke` 或 `graph.play`，可根据实现便利性二选一
- 对后端来说，保留“有些是资源点播，有些是行为调用”的边界，比强行统一成一个字段更稳

### 7.5 第五层：`display.reset` 和 `display.report`

建议再补两个工具型事件：

`display.reset`

- 强制回到 `DisplayToNomal()`

`display.report`

- 主动请求一次当前展示状态快照

这两个事件对调试和长链路编排都很有价值。

## 八、与当前 phase 1 协议的关系

这套全控方案不应推翻 `protocol-phase1.md`。

推荐关系如下：

- `protocol-phase1.md`
  - 保持“当前已正式承诺的最小对外协议”
  - 继续强调 `bubble.show / motion.play / mode.switch / emotion.set / window.move`
- 本文
  - 作为“展示层全控专题设计”
  - 服务于下一阶段扩展，不代表当前全部已上线

换句话说：

- phase 1 已承诺协议：保持克制
- phase 2 控制面扩展：按本文推进

## 九、推荐实施顺序

### 第一步：先做 `graph.catalog`

原因：

- 这是所有后续工作的目录基础
- 不做 catalog，后端和调试页仍然只能靠人工记名字

产出：

- 当前角色能力目录
- graph 名到类型 / 动画阶段的映射

### 第二步：做 `graph.play`

原因：

- 这是收益最大的单项扩展
- 可以立刻覆盖大量当前桥接还没暴露的展示资源

预期收益：

- 绝大多数待机 / 移动 / 工作 / 特殊演出 graph 可直接点播

### 第三步：做 `behavior.invoke`

原因：

- 补齐贴边 / 探头 / 交互态 / 拖拽态等复杂行为

重点优先级建议：

- `sidehide_left`
- `sidehide_right`
- `peek_left`
- `peek_right`
- `recover_from_sidehide`
- `touch_head`
- `touch_body`

### 第四步：增强状态回传

原因：

- 没有对应展示状态回传，就无法稳定验证“graph 已播放”还是“行为已进入”

### 第五步：再考虑是否收口旧白名单

到这一层再决定：

- `motion.play` 是否继续保留为小白名单 alias
- `emotion.set` 是否继续保留为小白名单 alias

当前不建议先删，因为：

- 它们仍然是 phase 1 的正式兼容层

## 十、风险与边界

### 10.1 graph 存在，不等于语义稳定

例如：

- `Shining`
- `Shy`
- `Serious`

这些当前角色有，不代表其他角色也有。

所以 catalog 和 `graph.play` 应该是“资源级能力”，不是“跨角色稳定语义能力”。

### 10.2 有些 graph 不适合长期停留

例如：

- 只存在 `Single`
- 或本质上是过渡帧

因此 catalog 最好提供：

- 支持的 `AnimatType`
- 是否建议循环

### 10.3 复杂行为不要假装成简单点播

例如探头：

- 直接播 `SideHide_Left_Rise` 能看到效果
- 但这不等于“已经完成贴边后探头行为”

所以 `peek_left` 仍应属于行为层。

### 10.4 `Eat / Drink / Gift` 建议延后

因为这三类会把“纯展示控制”和“物品演出系统”混在一起。

## 十一、最终建议

对于“让 AI 或后端完整控制 VPet 前端展示层”这个目标，推荐的工程结论是：

- 不要继续把所有新增能力硬塞进 `motion.play` 和 `emotion.set`
- 保留当前 phase 1 最小协议作为稳定兼容层
- 新增：
  - `graph.catalog`
  - `graph.play`
  - `say.play` 或增强版 `bubble.show`
  - `behavior.invoke`
  - `display.reset`
  - `display.report`

这样可以同时满足三类需求：

- 调试：直接点播任何现有 graph
- AI 控制：用高层行为接口表达贴边、探头、触摸、恢复等语义
- 演进：换角色时自动适配资源目录，而不是重写一堆白名单

## 十二、与本轮工作的关系

本轮工作是一次纯探索和沉淀，不包含实现以下新增协议：

- `graph.catalog`
- `graph.play`
- `behavior.invoke`
- `display.reset`
- `display.report`

本轮完成的是：

- 追溯 `VPet` 展示层真实可控范围
- 区分“本体能力”和“桥接暴露面”
- 给出可行的全控扩展路径
- 将结论落盘到当前 mission 的 `spec/`

后续如果进入实现阶段，应以本文作为 phase 2 控制面扩展的专题设计依据。
