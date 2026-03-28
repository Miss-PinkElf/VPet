# Protocol Phase 1

## Purpose

本清单定义 `VPet` 作为前端执行层 / 身体层时，第一阶段正式对外暴露的协议边界。

目标是让后端把 `VPet` 当作可调用的前端执行端，而不是继续依赖联调页面或模糊 intent。

## Role Split

- `VPet`：前端执行层 / 身体层
- `Python backend-agent`：大脑 / 编排与决策层

## Officially Supported Commands

### `bubble.show`

用途：
- 显示气泡文本
- 可附带有限表情或 graph

正式参数：
- `text`
- `duration_ms`
- `expression` 可选
- `graph` 可选
- `motion` 可选

说明：
- `touch_head / touch_body / pinch / thinking` 已按更接近 VPet 原生的动作+说话顺序编排

### `motion.play`

用途：
- 触发单独动作

正式参数：
- `motion`
- `priority` 可选

第一阶段承诺动作：
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

### `mode.switch`

用途：
- 切换高层模式态

正式参数：
- `mode`

第一阶段承诺模式：
- `thinking`
- `normal`

### `emotion.set`

用途：
- 切到有限表情 / graph

正式参数：
- `emotion`
- `graph` 可选

说明：
- 只承诺当前已确认映射
- 不承诺任意语义值都能稳定播放

### `window.move`

用途：
- 显式窗口位移

正式参数：
- `dx`
- `dy`
- `style` 可选

说明：
- 这是第一阶段唯一正式移动协议
- 当前支持的 `style`：
  - `smart`
  - `smooth` / `walk`
  - `snap` / `teleport`
- 当前默认建议：
  - 短距离：`smart`，表现为平滑走位
  - 长距离：`smart`，表现为直接跳位
- 当前还没有正式承诺稳定的“开门闪现”专项视觉 graph

## Official State Contract

`VPet` 会向后端回传以下状态字段：

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

第一阶段推荐后端真正依赖的字段：

- `left`
- `top`
- `right`
- `bottom`
- `display_name`
- `display_animat`
- `bubble_visible`
- `last_event_type`
- `last_event_at`

说明：

- `left / top / right / bottom` 用于验证显式位移与边界关系
- `display_name / display_animat` 用于观察动作与视觉阶段
- `bubble_visible` 用于观察气泡视觉残留
- `last_event_type / last_event_at` 用于观察事件消费时序

## Legacy Compatibility

### `move.intent`

当前状态：
- 只保留最薄运行时兼容
- 不再是正式主协议
- 不再在 `/dev/control` 中作为联调主入口暴露

仅剩 legacy 兼容范围：
- `dock_left`
- `dock_right`
- `dock_top`
- `dock_bottom`

## Explicitly Not Committed In Phase 1

以下能力不属于第一阶段正式承诺范围：

- `follow_cursor` 一类抽象移动 intent
- 深改 `GameCore`
- 任意 emotion 自动映射任意 graph
- 把 `/dev/control` 作为正式业务入口
- 依赖更多桌宠内部工作态做主判断
- 将 `move.intent` 与 `window.move` 并列使用
- 承诺“所有 sequence 步骤都已具备完整动作完成门控”

## Current Limitation

当前 `sequence/scenario` 已经不再只靠 `delay_ms`。

这意味着：

- 当前可以对关键步骤加最小完成门控：
  - `wait_for=move_complete`
  - `wait_for=motion_complete`
  - `wait_for=event_applied`
- 当前最适合先门控的步骤是：
  - `window.move`
  - `motion.play(touch_head/touch_body/pinch)` 这一类短动作
- 还没有承诺“所有 graph / mode / bubble 生命周期都已具备稳定完成门控”

## Backend Calling Guidance

后端应这样调用 `VPet`：

1. 使用高层执行事件驱动前端表现
2. 使用显式参数，避免模糊 intent
3. 将复杂交互拆成 2 到 5 步 sequence
4. 使用状态回传确认执行结果

推荐调用分工：

- 说话：`bubble.show`
- 单动作：`motion.play`
- 模式切换：`mode.switch`
- 表情 / graph：`emotion.set` 或 `bubble.show(graph=...)`
- 位移：`window.move(dx, dy)`

## Backend Anti-Patterns

后端不应这样调用：

- 优先使用 `move.intent`
- 将模糊语义直接压给 `VPet` 自行猜测执行方式
- 依赖 `/dev/control` 页面完成正式业务控制
- 依赖未文档化 graph 名
- 把“联调页能点通”当成“正式协议成立”

## Recommended Examples

### `window.move`

```json
{
  "type": "window.move",
  "dx": 120,
  "dy": -20,
  "style": "smart"
}
```

### `motion.play`

```json
{
  "type": "motion.play",
  "motion": "touch_head",
  "priority": 50
}
```

### `mode.switch`

```json
{
  "type": "mode.switch",
  "mode": "thinking"
}
```

### `bubble.show`

```json
{
  "type": "bubble.show",
  "text": "我先想一下，再回答你。",
  "duration_ms": 5000,
  "graph": "think"
}
```

### Recommended Sequence

```json
{
  "steps": [
    {
      "event": {
        "type": "mode.switch",
        "mode": "thinking"
      }
    },
    {
      "event": {
        "type": "window.move",
        "dx": 90,
        "dy": -20,
        "style": "smart"
      },
      "wait_for": "move_complete",
      "wait_timeout_ms": 5000,
      "settle_ms": 120
    },
    {
      "event": {
        "type": "bubble.show",
        "text": "我先想一下，再边移动边回答。",
        "duration_ms": 5000,
        "graph": "think"
      }
    },
    {
      "event": {
        "type": "mode.switch",
        "mode": "normal"
      }
    }
  ]
}
```

## Phase 1 Summary

第一阶段正式对外协议可压缩为以下结论：

- 正式保留：`bubble.show / motion.play / mode.switch / emotion.set / window.move / state report`
- 正式移动协议：只承诺 `window.move(dx, dy)`
- 正式移动风格：支持 `style=smart|smooth|snap`
- legacy 兼容：`move.intent`
- 编排职责：后端负责行为编排，`VPet` 负责执行和状态回传
