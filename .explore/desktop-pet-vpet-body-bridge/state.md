# 当前状态

## 当前阶段
- 阶段 3：插件桥接已补上 `window.move` 与最小状态回传，形成基础闭环

## 已确认的事实
- VPet 在本项目中的角色已经冻结为身体层 / 前端执行层。
- Python `backend-agent` 是大脑，不在第一阶段深改 `GameCore`。
- 当前桥接已收敛到 `VPet.Plugin.AgentBridge/`。
- 插件由 `MainPlugin.GameLoaded()` 启动，在 `EndGame()` 中释放轮询器。
- 当前桥接通过 HTTP 轮询 `http://127.0.0.1:18787/vpet/events/next` 获取单条事件。
- 当前已打通：
  - `bubble.show`
  - `motion.play`
  - `mode.switch`
  - `emotion.set`
  - `window.move`
- `bubble.show + touch_head/touch_body/pinch/thinking` 已改为更接近 VPet 原生的动作+说话编排。
- 插件 DLL 已输出到 `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/`。
- `/dev/control` 已改成更适合联调的下拉式表单。
- `/dev/control` 已切到显式 `window.move(dx, dy)` 协议，并展示最新状态快照。
- 插件当前会向 `POST /vpet/state` 回传最小状态：
  - `left`
  - `top`
  - `zoom_ratio`
  - `display_name`
  - `display_type`
  - `mode`
  - `last_event_type`
- 2026-03-27 本地联调已验证一次真实 `window.move`：
  - 发送 `dx=120, dy=-40`
  - 状态从 `left=1105.6, top=1188.8` 变为 `left=1225.6, top=1148.8`
  - 实际增量与请求一致：`delta_left=120, delta_top=-40`
- `shy -> pinch` 仍是临时近似映射。

## 工作假设
- 当前优先级已从“补移动/回传”切到“继续扩状态消费与更完整身体层协议”。
- 现阶段不需要回退到主工程内置桥接。
- 当前 `.explore/desktop-pet-vpet-body-bridge/` 将作为新的 mission 真相源，旧 `.codex/explore/desktop-pet-vpet-body-bridge/` 仅保留为 legacy 参考。

## 待解决的问题
- 最小状态回传后续是否要补更多工作态字段，而不只是位置和 display。
- `move.intent` 的 legacy 兼容要保留多久，何时只保留 `window.move`。
- `emotion -> graph` 是否需要继续做运行时导出，而不是只靠人工映射。

## 下一步
- 在 `/dev/control` 上继续验证 `window.move + bubble/motion` 的组合体感。
- 决定最小状态回传是否要继续补充边界距离或工作态字段。
- 评估是否需要把 `move.intent` 明确降级为 legacy 文档层兼容。

## 最新 handoff
- [2026-03-27-004-window-move-state-loop.md](E:\Learn\Vs\Code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\2026-03-27-004-window-move-state-loop.md)

## 最小活跃上下文摘要
- 当前重点不是再证明路线成立，而是在已具备 `window.move + state` 闭环的插件桥接上继续扩身体层能力与状态消费。
