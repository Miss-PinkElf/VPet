# 当前状态

## 当前阶段
- 阶段 3：桥接已完成联调并收敛为 `MainPlugin` 插件

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
- `bubble.show + touch_head/touch_body/pinch/thinking` 已改为更接近 VPet 原生的动作+说话编排。
- 插件 DLL 已输出到 `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/`。
- `/dev/control` 已改成更适合联调的下拉式表单。
- `shy -> pinch` 仍是临时近似映射。

## 工作假设
- 先补 `window.move` 和最小状态回传，比继续扩动作语义更重要。
- 现阶段不需要回退到主工程内置桥接。
- 当前 `.explore/desktop-pet-vpet-body-bridge/` 将作为新的 mission 真相源，旧 `.codex/explore/desktop-pet-vpet-body-bridge/` 仅保留为 legacy 参考。

## 待解决的问题
- `window.move` 如何从高层 intent 收敛到 `MW.Core.Controller.MoveWindows(...)`。
- 最小状态回传要暴露哪些字段最合适。
- `emotion -> graph` 是否需要继续做运行时导出，而不是只靠人工映射。

## 下一步
- 在插件化版本上继续验证组合事件体感。
- 补 `window.move`。
- 再补最小状态回传，形成更完整的身体层闭环。

## 最新 handoff
- [2026-03-27-003-explore-migration-resume.md](E:\Learn\Vs\Code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\2026-03-27-003-explore-migration-resume.md)

## 最小活跃上下文摘要
- 当前重点不是再证明路线成立，而是在插件化后的桥接版本上继续补身体层控制能力，优先做 `window.move` 和最小状态回传。
