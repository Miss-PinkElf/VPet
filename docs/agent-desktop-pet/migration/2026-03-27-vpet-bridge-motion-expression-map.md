# VPet 桥接动作与表情映射清单

这份清单只记录当前仓库中已经确认可复用、适合第一阶段桥接的能力。

## 1. 已确认稳定的高层动作映射

这些映射直接复用 `MainWindow.RunAction(...)` 或现有现成方法。

| 后端事件值 | VPet 执行入口 | 说明 |
| --- | --- | --- |
| `idle` | `RunAction("DisplayIdel")` | 基础待机动作 |
| `move` | `RunAction("DisplayMove")` | 基础移动动作 |
| `normal` | `RunAction("DisplayToNomal")` | 回到默认状态 |
| `touch_head` | `RunAction("DisplayTouchHead")` | 摸头交互 |
| `touch_body` | `RunAction("DisplayTouchBody")` | 摸身体交互 |
| `sleep` | `RunAction("DisplaySleep")` | 睡觉动作 |
| `raised` | `RunAction("DisplayRaised")` | 抬起/拖拽状态 |
| `state_one` | `RunAction("DisplayIdel_StateONE")` | 待机模式 1 |
| `pinch` | `DisplayPinch()` | 捏脸动作，源码中已有专门实现 |
| `thinking` | `Display("think", ...)` | 走现成 `think` graph |

## 2. 已确认稳定的 mode 映射

| 后端事件值 | VPet 执行入口 | 说明 |
| --- | --- | --- |
| `thinking` | `Display("think", ...)` | 进入思考态 |
| `normal` | `RunAction("DisplayToNomal")` | 退出思考/自定义态并回归默认 |

## 3. 当前桥接支持的消息附加能力

`bubble.show` 现在除了 `text` 之外，还支持：

| 字段 | 作用 |
| --- | --- |
| `motion` | 协议里仍保留，但当前联调不建议和 `bubble.show` 混用 |
| `expression` | 说话时附带一个表情映射 |
| `graph` | 直接指定 VPet 的 graph 名，优先级高于 `expression` |

当前联调结论：

- 直接同帧执行 `bubble.show + 高层 motion` 观感不稳定，容易被 `Say(...)` 的说话态覆盖。
- 当前桥接对 `touch_head / touch_body / pinch / thinking` 已改成更接近 VPet 原生的编排：
  `DisplayStopForce(...) -> Say(text, 原生 graph, force: true)`。
- 其他未特化的 `bubble.motion` 仍走“先动作、再说话”的回退顺序。
- 如果想要更明显、更完整的动作表现，仍建议拆成单独的 `motion.play`。

## 4. 已确认稳定的表情 / graph 映射

这些是当前从源码挂点中确认可直接驱动的 graph 名。

| 语义值 | graph 名 | 说明 |
| --- | --- | --- |
| `think` | `think` | 现成思考态 |
| `thinking` | `think` | `think` 的同义写法 |
| `pinch` | `pinch` | 现成捏脸表情/动作 |

## 5. 当前的临时推断映射

这些映射不是从源码里直接看到语义名，而是为了第一阶段联调先给出的近似映射。

| 语义值 | graph 名 | 说明 |
| --- | --- | --- |
| `shy` | `pinch` | 当前仓库里没有直接确认的 `shy` graph 名，先用 `pinch` 做“害羞/别闹”近似效果 |

## 6. 当前不建议直接承诺的能力

- 不能把相册/图片资源里的“害羞”“羞愧”名称直接当作可播放动画名使用。
- 未扫描出源码级稳定 graph 名之前，不要直接承诺 `happy/angry/sad` 一定能播放。
- 这类语义后续建议通过“graph 名白名单”或运行时导出清单进一步补齐。

## 7. 当前推荐的后端事件写法

### 7.1 消息 + 顺序动作 + 表情

```json
{
  "type": "bubble.show",
  "text": "你突然这么说，我会害羞的……",
  "motion": "touch_body",
  "expression": "shy"
}
```

说明：当前桥接会先执行 `touch_body`，再延迟说话，不再和说话态同帧硬切。

### 7.2 单独动作

```json
{
  "type": "motion.play",
  "motion": "touch_body"
}
```

### 7.3 消息 + 表情

```json
{
  "type": "bubble.show",
  "text": "你突然这么说，我会害羞的……",
  "expression": "shy"
}
```

### 7.4 进入思考态

```json
{
  "type": "mode.switch",
  "mode": "thinking"
}
```

### 7.5 直接指定 graph

```json
{
  "type": "bubble.show",
  "text": "我在思考。",
  "graph": "think"
}
```

## 8. 这份清单的边界

这份清单服务于“第一阶段最小桥接 POC”，目标是先让 Python 后端稳定驱动 VPet 的身体层。
后续如果要把 VPet 作为长期身体层，还应继续补：

- 运行时导出当前 `GraphsName` / `GraphsList` 的工具
- 更完整的 `emotion -> graph` 映射表
- 更完整的状态回传

## 9. 已收敛的窗口移动协议

`move.intent` 在测试页阶段暴露过，但它的语义过虚，难以稳定落到 VPet 的具体位移能力上。
当前桥接已经收敛为更明确的 `window.move`：

```json
{
  "type": "window.move",
  "dx": 120,
  "dy": 0
}
```

说明：

- `dx / dy` 是传给 `MW.Core.Controller.MoveWindows(...)` 的逻辑位移量
- VPet 内部会再乘以当前 `ZoomRatio`
- 正值表示向右 / 向下，负值表示向左 / 向上

兼容层：

- 插件仍暂时接受 `move.intent`
- `/dev/control` 联调页已不再暴露 `move.intent`，避免继续把它当作第一阶段主验证路径
- 当前只保留 `dock_left / dock_right / dock_top / dock_bottom` 这类可明确收敛到边界位移的 intent
- `follow_cursor` 这类需要更深交互语义的 intent 不再作为第一阶段承诺能力

## 10. 最小状态回传

当前最小状态回传用于联调闭环验证，VPet 插件会把以下字段 POST 回后端：

- `left`
- `top`
- `right`
- `bottom`
- `zoom_ratio`
- `display_name`
- `display_type`
- `display_animat`
- `mode`
- `working_state`
- `work_name`
- `work_type`
- `bubble_visible`
- `last_event_type`
- `last_event_at`

说明：

- `left / top / right / bottom` 都是按当前 `ZoomRatio` 归一化后的逻辑距离，便于直接和 `window.move(dx, dy)` 或边界吸附结果对比
- `display_animat` 和 `bubble_visible` 用来判断“事件已消费”和“视觉状态真正切换”之间的时间差
- `last_event_at` 用来区分“最近一次事件被插件消费的时刻”和“当前这份状态何时被回传”
- `working_state / work_name / work_type` 是第一阶段里够用但不深改 `GameCore` 的工作态补充
- 当前测试页会展示最新一份状态快照，用来验证 `window.move`、动作切换和组合场景的实际效果

## 11. 当前最小 sequence/scenario 联调入口

为了继续验证“说话 + 位移 + 动作”的组合编排，当前 `backend-agent` 已提供两类联调入口：

### 11.1 预设 scenario

- `GET /api/dev/scenarios`
  - 返回当前联调页可直接触发的预设组合场景目录
- `POST /api/dev/scenarios/{scenario_id}`
  - 触发一个由后端负责调度的预设场景

说明：

- 场景的步骤与延迟现在由后端维护
- `/dev/control` 页面不再自己保存组合步骤
- 当前默认预设包括：
  - `move-then-bubble`
  - `bubble-then-move`
  - `move-then-motion`
  - `move-then-bubble-touch`
  - `thinking-walk-think`
  - `bubble-move-touch-recover`

### 11.2 自定义 sequence

- `POST /api/dev/sequences`
  - 触发一条最小 sequence，请求体包含 `steps`

当前联调页默认示例已经升级成 4 步长链路；一个等价示例如下：

```json
{
  "name": "thinking-walk-speak-normal",
  "steps": [
    {
      "event": {
        "type": "mode.switch",
        "mode": "thinking"
      }
    },
    {
      "delay_ms": 420,
      "event": {
        "type": "window.move",
        "dx": 90,
        "dy": -20
      }
    },
    {
      "delay_ms": 480,
      "event": {
        "type": "bubble.show",
        "text": "我先想一下，再边移动边回答。",
        "duration_ms": 5000,
        "expression": "thinking",
        "graph": "think"
      }
    },
    {
      "delay_ms": 520,
      "event": {
        "type": "mode.switch",
        "mode": "normal"
      }
    }
  ]
}
```

说明：

- `delay_ms` 表示该步执行前的等待时间
- 每一步的 `event` 仍复用现有单事件协议
- 第一阶段推荐继续优先使用显式 `window.move`，不要在 sequence 中重新扩散 `move.intent`
