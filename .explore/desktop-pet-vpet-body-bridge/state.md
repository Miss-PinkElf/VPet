# 当前状态

## 当前阶段
- 阶段 3：插件桥接已补上最小 sequence/scenario 联调入口，进入编排层打磨与启动链路收口

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
- `/dev/control` 现已不再把组合步骤硬编码在浏览器侧，而是调用后端 `sequence/scenario` 入口。
- 插件当前会向 `POST /vpet/state` 回传最小状态：
  - `left`
  - `top`
  - `zoom_ratio`
  - `display_name`
  - `display_type`
  - `mode`
  - `last_event_type`
- 本轮已把状态快照扩到更适合组合联调的字段：
  - `right`
  - `bottom`
  - `display_animat`
  - `working_state`
  - `work_name`
  - `work_type`
  - `bubble_visible`
- 2026-03-27 本地联调已验证一次真实 `window.move`：
  - 发送 `dx=120, dy=-40`
  - 状态从 `left=1105.6, top=1188.8` 变为 `left=1225.6, top=1148.8`
  - 实际增量与请求一致：`delta_left=120, delta_top=-40`
- 2026-03-27 本轮继续完成了组合体感联调：
  - `move -> bubble` 在约 `450ms` 间隔下可稳定出现说话气泡
  - `bubble -> move` 体感稳定，移动时 `bubble_visible=true`
  - `move -> motion.play(touch_head)` 体感稳定，状态可见 `last_event_type=motion.play`
  - `move -> bubble.touch_body` 也可用，但切进原生触摸态比 plain bubble 更慢
- `move.intent` 仍保持最薄运行时兼容，但已在 `/dev/control` 中明确降级为 legacy 入口，不再作为第一阶段主验证路径。
- `start-vpet-bridge.ps1` 已自动确保运行目录 `Setting.lps` 包含 `onmod:|agentbridge:|`，本地联调少一个常见前置坑。
- `backend-agent` 本轮新增了最小编排层：
  - `GET /api/dev/scenarios`
  - `POST /api/dev/scenarios/{scenario_id}`
  - `POST /api/dev/sequences`
- `/dev/control` 本轮新增了：
  - 后端维护的 scenario 目录按钮
  - 自定义 sequence JSON 入口
- 2026-03-27 本轮已验证：
  - 代码级路由与 HTML 内容包含新的 sequence/scenario 入口
  - `DevSequenceOrchestrator` 会按延迟顺序把事件写入事件总线
  - 在 18788 端口直起当前后端时，新接口可正常访问
- 2026-03-27 本轮暴露出一个工具链问题：
  - 标准 18787 启动链路在本会话里仍可能落到旧 `uvicorn --reload` 进程
  - 因此 18787 上的 `/dev/control` 可能继续显示旧页面
  - 这已经被记录为后续排查项，不影响当前 sequence/scenario 代码本身已实现并通过隔离验证
- `shy -> pinch` 仍是临时近似映射。

## 工作假设
- 当前优先级已从“补移动/回传”切到“用后端编排层和更可观测状态继续打磨身体层协议”。
- 现阶段不需要回退到主工程内置桥接。
- 当前 `.explore/desktop-pet-vpet-body-bridge/` 将作为新的 mission 真相源，旧 `.codex/explore/desktop-pet-vpet-body-bridge/` 仅保留为 legacy 参考。

## 待解决的问题
- 现有状态字段是否已经足够支撑第一阶段联调，还是还要继续补 `topmost / hitthrough` 一类桌宠工作态。
- `move.intent` 的运行时薄兼容要保留多久，是否下一轮就从手动联调 UI 中进一步隐藏。
- `emotion -> graph` 是否需要继续做运行时导出，而不是只靠人工映射。
- 为什么标准 18787 启动链路在本会话里仍可能被旧 `uvicorn --reload` 进程劫持，以及如何彻底清理它。

## 下一步
- 基于后端 sequence/scenario 入口继续验证更长链路的组合编排，而不只看单条事件。
- 判断当前状态集合是否已经足够，还是要再补少量桌宠运行态字段。
- 决定 `move.intent` 是继续保留运行时薄兼容，还是进入下一轮彻底退到文档兼容。
- 排查并修复标准 18787 启动链路的旧 `uvicorn --reload` 残留问题。

## 最新 handoff
- [2026-03-27-007-context-save-sequence-state.md](D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\2026-03-27-007-context-save-sequence-state.md)

## 最小活跃上下文摘要
- 当前重点不是再证明桥接能不能跑，而是借助后端 sequence/scenario 入口、扩展状态快照和真实组合场景，把第一阶段身体层编排打磨到足够稳定，同时收掉标准启动链路里的旧后端残留问题。
