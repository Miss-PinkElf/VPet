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
- `window.move`
- 最小状态回传
