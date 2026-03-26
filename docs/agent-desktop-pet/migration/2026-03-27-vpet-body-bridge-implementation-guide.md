# VPet 作为前端身体层的详细实施指南

## 1. 这份文档解决什么问题

这份文档面向当前仓库的实际情况：

- 你希望把 `VPet` 当成桌宠前端，而不是继续把它当作完整业务系统
- 你不熟悉 `C# / WPF`
- 你需要一份可以长期续接、能指导 AI 实际改仓库的实施手册

一句话目标：

> 保留 `VPet` 的窗口行为和动画表现，把外部 `Python backend-agent` 接进来，让 `Python` 负责大脑，`VPet` 负责身体。

当前阶段的目标不是全面重构 `VPet`，而是先打通：

> 外部事件 -> VPet 执行动作/说话/窗口反馈

## 2. 当前应该如何理解这个仓库

建议把当前系统强制分成三层：

### 2.1 Brain

外部 `Python backend-agent`

负责：

- 对话
- 记忆
- 感知
- 行为策略
- 事件生成

### 2.2 Bridge

新增一层 `AgentBridge`

负责：

- 接收 `Python` 发来的高层事件
- 把事件翻译成 `VPet` 当前能执行的动作
- 回传最小状态给后端

### 2.3 Body

当前 `VPet`

负责：

- 桌宠窗口行为
- 帧动画表现
- 气泡/说话显示
- 拖拽、贴边、移动
- 桌宠状态的执行层

## 3. 这轮代码阅读后确认的关键挂点

以下挂点已经存在，不需要从零发明。

### 3.1 主动作入口

文件：

- `VPet-Simulator.Windows/MainWindow.cs`

关键方法：

- `RunAction(string action)`

当前已支持的动作字符串包括：

- `DisplayNomal`
- `DisplayToNomal`
- `DisplayTouchHead`
- `DisplayTouchBody`
- `DisplayIdel`
- `DisplayIdel_StateONE`
- `DisplaySleep`
- `DisplayRaised`
- `DisplayMove`

这说明第一版桥接完全可以先复用 `RunAction(...)`，不用一开始就深入改 `MainLogic`。

### 3.2 说话入口

文件：

- `VPet-Simulator.Core/Display/MainLogic.cs`

关键方法：

- `Main.Say(string text, string graphname = null, bool force = false, string desc = null)`
- `Main.SayRnd(string text, bool force = false, string desc = null)`

这说明第一版 `bubble.show` / `speak` 事件已经有天然落点。

### 3.3 显示层动作入口

文件：

- `VPet-Simulator.Core/Display/MainDisplay.cs`

当前确认可直接调用或间接触发的能力：

- `DisplayToNomal()`
- `DisplaySleep(bool force = false)`
- `DisplayRaised()`
- `DisplayMove`
- `DisplayIdel`

### 3.4 窗口移动控制

文件：

- `VPet-Simulator.Core/Handle/IController.cs`
- `VPet-Simulator.Windows/Function/MWController.cs`

关键方法：

- `MoveWindows(double X, double Y)`

这意味着第一版可以支持最小的窗口移动事件，而不需要自己重写窗口控制。

### 3.5 插件生命周期

文件：

- `VPet-Simulator.Windows.Interface/MainPlugin.cs`
- `VPet-Simulator.Windows/Function/CoreMOD.cs`

关键点：

- `MainPlugin.LoadPlugin()`
- `MainPlugin.GameLoaded()`
- 主程序会自动扫描 MOD 内 `plugin/*.dll`

这很重要，因为它说明：

> 长期方案应该优先做成插件式桥接，而不是把所有桥接逻辑硬塞进 `MainWindow`。

### 3.6 聊天/思考动画挂点

文件：

- `VPet-Simulator.Windows.Interface/TalkBox.xaml.cs`

关键方法：

- `DisplayThink()`
- `DisplayThinkToSayRnd(...)`

这给了后续 `thinking` 状态一个天然复用点。

## 4. 推荐的改造原则

### 4.1 先加桥，不先拆心脏

当前最不该做的事：

- 先重构 `GameCore`
- 先重构 `MainLogic`
- 先清理所有存档/插件/外围逻辑

当前最该做的事：

- 保持 `VPet` 能正常跑
- 新增一层外部事件入口
- 只做最小协议翻译

### 4.2 先做窄协议，不做万能总线

第一版协议只支持几个确定事件，不要追求完整：

- `bubble.show`
- `motion.play`
- `mode.switch`
- `window.move`
- `status.get`

### 4.3 优先插件化，保留 POC 快捷路径

长期建议：

- 用 `MainPlugin` 做 `AgentBridge`

短期 POC 允许：

- 直接在 `MainWindow` 启动后挂一个桥接轮询器

但 POC 验证通过后，建议尽快回收为插件结构。

### 4.4 不直接让 Python 触碰底层存档状态

第一阶段不要让后端直接改这些内容：

- `Core.Save.Mode`
- `GameSavesData`
- 具体存档字段
- 原始 MOD 加载流程

第一阶段只允许：

- 播放动作
- 显示气泡
- 控制窗口轻量移动
- 上报当前状态

## 5. 推荐架构

推荐结构如下：

```text
backend-agent/
  app/
    api/
    services/
    memory/

VPet.Plugin.AgentBridge/
  AgentBridgePlugin.cs
  AgentBridgePoller.cs
  PetEvent.cs
  PetStatusSnapshot.cs
  AgentBridgeConfig.cs

VPet-Simulator.Windows/mod/1200_AgentBridge/
  info.lps
  plugin/
    VPet.Plugin.AgentBridge.dll
```

说明：

- `backend-agent` 继续作为外部大脑
- `VPet.Plugin.AgentBridge` 是新的桥接项目
- `mod/1200_AgentBridge/` 是桥接插件的 MOD 壳

## 6. 第一版事件协议建议

第一版不要设计得太大，建议先固定成以下几类。

### 6.1 从 Python 发给 VPet

#### 事件 1：显示气泡

```json
{
  "type": "bubble.show",
  "text": "你好，我在。",
  "style": "normal"
}
```

映射：

- `MW.Main.Say(text)`

#### 事件 2：播放动作

```json
{
  "type": "motion.play",
  "name": "idle"
}
```

第一版只建议支持：

- `idle`
- `move`
- `sleep`

映射建议：

- `idle` -> `MW.RunAction("DisplayIdel")`
- `move` -> `MW.RunAction("DisplayMove")`
- `sleep` -> `MW.RunAction("DisplaySleep")`

#### 事件 3：切换模式

```json
{
  "type": "mode.switch",
  "name": "thinking"
}
```

第一版只建议支持：

- `thinking`
- `normal`

映射建议：

- `thinking` -> 复用 `TalkBox.DisplayThink()` 的逻辑，或者直接显示 `think` 动画
- `normal` -> `MW.RunAction("DisplayToNomal")`

#### 事件 4：窗口轻量移动

```json
{
  "type": "window.move",
  "dx": 20,
  "dy": 0
}
```

映射：

- `MW.Core.Controller.MoveWindows(dx, dy)`

### 6.2 从 VPet 回给 Python

建议只回最小状态，不做重日志：

```json
{
  "mode": "Nomal",
  "working_state": "Nomal",
  "display_type": "Default",
  "position": {
    "left": 100,
    "top": 200
  }
}
```

第一版只要满足后端知道：

- 当前在不在思考/说话/默认态
- 当前窗口位置
- 当前基础模式

就够了。

## 7. 推荐的实施顺序

下面这套顺序是按“你不懂 `C#`，主要靠 AI 持续推进”的现实情况设计的。

### 阶段 0：冻结目标，不再继续发散

本阶段只做以下事情：

- 明确 `VPet` 是身体层，不是大脑
- 明确第一阶段只做事件桥
- 明确不先重构深层逻辑

验收标准：

- 你和 AI 后续都使用同一套说法
- 文档里不再混淆“主项目底座”和“身体层验证分支”

### 阶段 1：做最小桥接 POC

目标：

- 后端能发一个事件
- `VPet` 能执行一个动作或说一句话

推荐只实现这 3 个事件：

- `bubble.show`
- `motion.play(name=idle)`
- `motion.play(name=move)`

实现建议：

1. 先在 `VPet-Simulator.Windows` 内部临时加一个 `AgentBridgePoller`
2. 在 `Main` 初始化完成后启动轮询
3. 从本地 HTTP 拉取一条事件
4. 按事件类型调用 `MW.Main.Say(...)` 或 `MW.RunAction(...)`

验收标准：

- 程序启动后不崩
- 后端发出一条事件
- 桌宠能说一句话
- 桌宠能切到一次 `idle` 或 `move`

### 阶段 2：把 POC 收敛为插件

目标：

- 不再把桥接逻辑写死在主工程里

实现建议：

1. 新建 `VPet.Plugin.AgentBridge` 项目
2. 让主类继承 `MainPlugin`
3. 在 `LoadPlugin()` 或 `GameLoaded()` 启动轮询器
4. 插件内部持有 `MW`
5. 所有命令都通过 `MW.Main` / `MW.Core.Controller` / `MW.RunAction(...)` 完成

验收标准：

- 删除主工程中的临时桥接代码后仍能工作
- 插件单独控制桌宠动作成功

### 阶段 3：补最小状态回传

目标：

- 后端不只是盲发事件，也知道桌宠当前在做什么

建议回传：

- 当前 `Mode`
- 当前 `WorkingState`
- 当前 `DisplayType`
- 当前窗口位置

验收标准：

- 后端能根据 `VPet` 当前状态决定是否继续发动作

### 阶段 4：接简单对话闭环

目标：

- Python 返回一句话
- `VPet` 显示思考态
- `VPet` 输出气泡内容

此时可逐步复用：

- `TalkBox.DisplayThink()`
- `TalkBox.DisplayThinkToSayRnd(...)`
- `Main.Say(...)`

## 8. 为什么推荐“先内置 POC，再插件化”

因为你现在最大的风险不是“结构不够优雅”，而是“直接在抽象上耗死”。

如果一开始就同时做：

- 新项目
- 新协议
- 新插件
- 新后端接口
- 新测试工具

很容易直接失控。

更稳的顺序是：

1. 先在主工程里验证调用链成立
2. 证明外部事件能驱动 `VPet`
3. 再抽成插件

这个顺序更适合当前毕设节奏。

## 9. 第一阶段不要碰的内容

下面这些在第一阶段都不该主动动：

- `GameCore` 数据结构重构
- 存档体系
- `Core.Save` 大量字段写入
- MOD 总加载流程
- UI 总体重做
- 全量聊天系统替换
- 记忆系统直接塞进 `VPet`

原因：

- 这些都不是“证明路线成立”的必要条件
- 每一项都会显著放大风险

## 10. 后续具体会新增哪些文件

推荐最终新增这些文件。

### 10.1 文档文件

- `docs/agent-desktop-pet/migration/2026-03-27-vpet-body-bridge-implementation-guide.md`

### 10.2 记录文件

- `.codex/explore/desktop-pet-graduation-roadmap/*`
- `.codex/explore/desktop-pet-vpet-body-bridge/*`

### 10.3 代码文件

第二阶段建议新增：

- `VPet.Plugin.AgentBridge/VPet.Plugin.AgentBridge.csproj`
- `VPet.Plugin.AgentBridge/AgentBridgePlugin.cs`
- `VPet.Plugin.AgentBridge/AgentBridgePoller.cs`
- `VPet.Plugin.AgentBridge/PetEvent.cs`
- `VPet.Plugin.AgentBridge/PetStatusSnapshot.cs`
- `VPet.Plugin.AgentBridge/AgentBridgeConfig.cs`

### 10.4 MOD 壳

- `VPet-Simulator.Windows/mod/1200_AgentBridge/info.lps`
- `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/`

## 11. 你后面和 AI 协作时应该怎么下指令

因为你不懂 `C#`，所以最有效的方式不是让 AI 讲概念，而是让 AI按阶段直接落地。

你后面可以直接这样说：

### 11.1 做 POC

```text
按照 migration 文档，先做第一阶段最小桥接 POC。
目标只做 bubble.show、motion.play(idle)、motion.play(move)。
直接修改仓库并告诉我验证命令。
```

### 11.2 收敛为插件

```text
按照 migration 文档，把现在主工程里的桥接代码收敛成 MainPlugin 插件。
不要动深层 GameCore。
```

### 11.3 接简单对话闭环

```text
按照 migration 文档，接入 Python 后端返回文本后的 thinking -> speak 最小闭环。
```

## 12. 你每次要做的验证动作

你本地通常只需要做这几个动作：

```powershell
dotnet build .\VPet-Simulator.Windows\VPet-Simulator.Windows.csproj -c Debug -p:Platform=x64
cmd /c .\VPet-Simulator.Windows\mklink.bat
.\VPet-Simulator.Windows\bin\x64\Debug\net8.0-windows\VPet-Simulator.Windows.exe
```

如果这轮接了后端，再额外跑后端。

然后你反馈给 AI 的内容尽量固定成：

1. 你执行了哪个命令
2. 桌宠有没有启动
3. 事件有没有生效
4. 完整报错文本
5. 你的预期和实际结果

## 13. 当前建议的最近三步

如果继续推进，最合理的顺序是：

1. 先由 AI 在仓库里做第一版 `AgentBridge` POC
2. 只打通 `say / idle / move`
3. 通过后再收敛成插件项目

一句话总结：

> 当前阶段最重要的不是把 `VPet` 解耦得多漂亮，而是先证明外部 Python 可以稳定驱动 `VPet` 的动作和说话。
