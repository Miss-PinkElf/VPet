# Handoff: VPet 身体层桥接 Phase 1 续接

## Session Metadata
- Created: 2026-03-27 14:36:07
- Project: E:\Learn\Vs\Code\VPet
- Explore: .codex/explore/desktop-pet-vpet-body-bridge
- Branch: shuowang/dev-vpet
- Session duration: 约 1 个工作会话，涵盖桥接 POC、后端联调入口、一键启动脚本与动作/表情映射扩展

### Recent Commits (for context)
  - 10a64f1a docs: add vpet body bridge implementation notes
  - 9b3cf53e 优化一下skills
  - 2bd3e218 docs: add Windows quickstart command guide
  - e1c23d2a init
  - bbfcf7e7 修复图片错误

## Handoff Chain

- **Continues from**: None (fresh start)
- **Supersedes**: None

> This is the first handoff for this task.

## Current State Summary

本轮已经把“VPet 作为身体层、Python backend-agent 作为大脑”的第一阶段桥接从纯文档推进到可运行代码。VPet 主工程中已内置 `AgentBridge` 轮询器，默认从 `http://127.0.0.1:18787/vpet/events/next` 拉取单条事件；`backend-agent` 已补 `GET /vpet/events/next` 并保留 `/dev/control` 测试页。一键启动脚本和虚拟环境已就绪，VPet 编译通过、后端应用可导入。当前未完成的核心工作不再是实现基础桥，而是实际联调“消息 + 动作 + 表情”组合事件，并在效果确认后把当前主工程内置桥接收敛成 `MainPlugin` 插件。

## Codebase Understanding

### Architecture Overview

当前桥接架构分三层：

- `backend-agent/`：FastAPI 后端，负责大脑和测试页，现已兼容 VPet 轮询消费与原有事件总线
- `VPet-Simulator.Windows/AgentBridge/`：主工程内置临时桥接层，负责把高层事件翻译到 `RunAction(...)`、`Main.Say(...)`、graph 名播放
- `VPet` 本体：继续承担窗口行为、帧动画、交互执行与现成动作播放，不重构深层 `GameCore`

第一阶段仍坚持“先加桥，不先拆心脏”。高层动作优先走 `RunAction(...)`；表情/姿态优先走现成 graph 名，如 `think`、`pinch`；思考态也可以复用 `TalkBox.DisplayThink()` 对应 graph。

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| `VPet-Simulator.Windows/AgentBridge/AgentBridgePoller.cs` | VPet 轮询器与事件分发入口 | 新对话继续桥接实现时的第一入口 |
| `VPet-Simulator.Windows/AgentBridge/AgentBridgeEvent.cs` | VPet 侧事件模型 | 当前已扩展 `motion / expression / graph / mode` |
| `VPet-Simulator.Windows/MainWindow.cs` | 主窗口生命周期与动作入口 | `GameLoaded()` 后启动桥接，`RunAction(...)` 是主动作入口 |
| `VPet-Simulator.Windows/MainWindow.xaml.cs` | 主窗口关闭逻辑 | 关闭时释放轮询器，避免残留后台任务 |
| `backend-agent/app/api/routes/events.py` | 后端事件流与 VPet 轮询出口 | `/api/events` 保留 SSE，`/vpet/events/next` 服务于 VPet |
| `backend-agent/app/api/routes/dev_control.py` | 后端测试页 | 新对话联调时最先打开的页面 |
| `backend-agent/app/schemas/events.py` | 后端事件协议 | 当前组合事件字段以这里为准 |
| `backend-agent/app/services/behavior_policy_engine.py` | 手动测试页请求转事件 | 测试页字段变化必须同步这里 |
| `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md` | 动作 / 表情映射真相源 | 新对话继续前先读，避免再靠猜 |
| `.codex/explore/desktop-pet-vpet-body-bridge/state.md` | 专项当前状态 | 精简恢复上下文入口 |
| `.codex/explore/desktop-pet-graduation-roadmap/state.md` | 毕设全局状态 | 这轮进展已同步到全局主线 |

### Key Patterns Discovered

- 高层动作优先复用 `RunAction(...)`，不要直接深挖 `GameCore`
- 说话优先复用 `Main.Say(text, graphname, force: true)`，graph 名只在已确认时传入
- 表情/姿态与“相册图片名”不是一回事，必须区分“可播放 graph 名”和“图库资源名”
- WPF 侧调用必须回到 `Dispatcher`
- 桥接轮询器只允许主窗口实例启动，避免多开重复消费事件
- 当前 `shy -> pinch` 只是第一阶段近似映射，不是源码级确认的原生情绪语义

## Work Completed

### Tasks Finished

- [x] 在 `VPet-Simulator.Windows` 内置第一阶段最小桥接 POC
- [x] 把桥接启动接到 `MainWindow.GameLoaded()` 后，关闭时释放轮询器
- [x] 增加 `backend-agent` 的 `/vpet/events/next` 轮询出口
- [x] 建立根目录一键启动脚本，并自动处理后端 `.venv`
- [x] 将默认联调端口从 `8787` 切到 `18787`
- [x] 扩展桥接支持更多动作、mode 与表情映射
- [x] 输出动作 / 表情映射清单文档
- [x] 完成 VPet 编译验证与后端应用导入验证

### Files Modified

| File | Changes | Rationale |
|------|---------|-----------|
| `VPet-Simulator.Windows/AgentBridge/AgentBridgeConfig.cs` | 新增桥接配置，默认指向 `18787` | 固定第一阶段联调地址 |
| `VPet-Simulator.Windows/AgentBridge/AgentBridgeEvent.cs` | 扩展事件模型到 `motion / expression / graph / mode` | 支持组合事件 |
| `VPet-Simulator.Windows/AgentBridge/AgentBridgePoller.cs` | 新增 / 扩展桥接轮询与事件映射执行 | 核心桥接实现 |
| `VPet-Simulator.Windows/MainWindow.cs` | 启动桥接与桥接字段接入 | 主窗口生命周期挂点 |
| `VPet-Simulator.Windows/MainWindow.xaml.cs` | 关闭时释放桥接轮询器 | 避免残留资源 |
| `backend-agent/app/api/routes/events.py` | 新增 `/vpet/events/next` | 让 VPet 直接消费后端事件 |
| `backend-agent/app/services/event_bus.py` | 增加轮询队列 | 同时支持 SSE 与 VPet 轮询 |
| `backend-agent/app/schemas/events.py` | 扩展 `bubble.show` 与 `emotion.set` 字段 | 支持消息附带动作/表情 |
| `backend-agent/app/services/behavior_policy_engine.py` | 让测试页请求能生成组合事件 | 联调测试页与桥接协议对齐 |
| `backend-agent/app/api/routes/dev_control.py` | 扩展测试页字段与交互 | 手动测试消息 + 动作 + 表情 |
| `backend-agent/app/core/config.py` | 默认端口改为 `18787` | 避免用户本地 `8787` 冲突 |
| `backend-agent/run-dev.ps1` | 默认端口改为 `18787` | 与桥接统一 |
| `backend-agent/run-dev.sh` | 默认端口改为 `18787` | 与桥接统一 |
| `start-vpet-bridge.ps1` | 根目录一键启动脚本，自动处理 `.venv`、编译、重启 | 提升日常联调效率 |
| `start-vpet-bridge-dev.ps1` | 编译后启动前后端 | 重启联调用 |
| `start-vpet-bridge-fast.ps1` | 跳过编译启动前后端 | 快速联调用 |
| `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md` | 新增动作 / 表情映射清单 | 避免新对话重复扫描资源 |
| `.codex/explore/desktop-pet-graduation-roadmap/state.md` | 同步全局进展 | 保持毕设主线状态一致 |
| `.codex/explore/desktop-pet-graduation-roadmap/decision-log.md` | 追加桥接决策 | 沉淀路线依据 |
| `.codex/explore/desktop-pet-graduation-roadmap/learnings.md` | 追加经验 | 为新对话压缩上下文 |
| `.codex/explore/desktop-pet-vpet-body-bridge/state.md` | 同步专项实现状态 | 专项续接入口 |
| `.codex/explore/desktop-pet-vpet-body-bridge/handoff.md` | 更新精简交接文档 | 新对话恢复入口 |

### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| 第一阶段先内置桥接，不先直接插件化 | 主工程内置、完整插件工程、先重构深层逻辑 | 先证明链路成立，再收敛结构，风险最低 |
| 保留 VPet 为身体层，不把它当业务底座 | 继续 Electron、全面重构 VPet、全新 C# 架构 | VPet 最强的是窗口行为和动画身体层 |
| 后端先用 HTTP 单条轮询出口 | SSE 直连、WebSocket、完整总线 | 先把 VPet 接通最小联调链路 |
| 端口改为 `18787` | 沿用 `8787` | 用户本机 `8787` 已被占用 |
| `shy` 第一阶段近似映射到 `pinch` | 暂不支持、硬猜其它 graph、先跑资源导出 | 当前源码里未确认原生 `shy` graph，`pinch` 是最接近且可稳定播放的现成效果 |

## Pending Work

## Immediate Next Steps

1. 本地运行 `.\start-vpet-bridge-dev.ps1`，打开 `http://127.0.0.1:18787/dev/control`，真实验证 `touch_head / pinch / thinking / bubble.show + shy` 等组合事件，并记录哪些映射效果自然、哪些需要调整。
2. 根据真实联调结果更新 `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`，重点确认 `shy -> pinch` 是否保留，哪些动作应该直接走 graph 名而不是 `RunAction(...)`。
3. 效果稳定后，把 `VPet-Simulator.Windows/AgentBridge/` 从主工程内置实现收敛为 `MainPlugin` 插件，并开始补 `window.move` 与最小状态回传。

### Immediate Next Steps

1. 本地运行 `.\start-vpet-bridge-dev.ps1`，打开 `http://127.0.0.1:18787/dev/control`，真实验证以下事件：
   - `motion.play`: `touch_head`
   - `motion.play`: `pinch`
   - `mode.switch`: `thinking`
   - `bubble.show` + `motion=touch_body` + `expression=shy`
   - `bubble.show` + `graph=think`
2. 根据真实效果调整映射表，重点确认：
   - `shy -> pinch` 是否可接受
   - `thinking` 用 `think` graph 的表现是否稳定
   - 哪些动作需要从“高层 motion”改成“直接 graph”
3. 联调稳定后，把 `VPet-Simulator.Windows/AgentBridge/` 收敛为 `MainPlugin` 插件项目，并开始补 `window.move` / 状态回传

### Blockers/Open Questions

- [ ] `emotion -> graph` 目前仍是人工映射，未做运行时导出，后续可能需要额外工具确认更多 graph 名
- [ ] `shy` 没有源码级确认的原生 graph 名，当前只是临时近似映射
- [ ] 当前还没有完成真实 GUI 端到端截图级验证，只有编译 / 导入级验证
- [ ] `window.move` 和最小状态回传还没进入实现

### Deferred Items

- 插件化收敛：先保证第一阶段联调可用，再避免过早抽象
- `window.move`：这轮优先级低于动作 / 表情 / 说话链路
- 运行时导出 `GraphsName / GraphsList`：对后续表情映射很重要，但本轮先用源码扫描与清单推进
- 更完整的 `emotion -> graph` 语义表：等待联调后按实际效果迭代

## Context for Resuming Agent

## Important Context

新对话继续时，不要重新讨论“VPet 能不能做身体层”或“要不要先重构深层 GameCore”，这些边界都已经冻结。当前重点是基于已完成的第一阶段桥接做真实联调，并把联调结果反馈到动作/表情映射表。一定要记住：高层动作优先走 `RunAction(...)`，表情/姿态优先走已确认 graph 名，如 `think`、`pinch`；图库资源名和可播放 graph 名不能混用。当前后端测试页、轮询出口、一键启动脚本、VPet 编译都已就绪，下一轮的第一动作应该是联调，而不是继续大范围扫仓库。

### Important Context

新对话继续时，不要再从“VPet 到底能不能做身体层”开始讨论，这个方向已经冻结。当前真正的状态是：

- 第一阶段桥接代码已经写完，不是纯分析
- 后端测试页已经可以直接手动发事件
- 当前重点是“联调真实效果”和“收敛为插件”，不是重写架构
- 需要严格区分：
  - 高层动作：优先走 `RunAction(...)`
  - 表情 / 姿态：优先走 graph 名（例如 `think`、`pinch`）
  - 图库 / 相册资源名：不能直接等同于可播放 graph 名

继续工作时，先读：
1. `.codex/explore/desktop-pet-vpet-body-bridge/handoff.md`
2. `.codex/explore/desktop-pet-vpet-body-bridge/state.md`
3. `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`
4. `VPet-Simulator.Windows/AgentBridge/AgentBridgePoller.cs`
5. `backend-agent/app/api/routes/dev_control.py`

然后直接从真实联调开始，不要重新扫描整仓库。

### Assumptions Made

- 假设当前分支仍是 `shuowang/dev-vpet`
- 假设 `backend-agent/.venv` 保持可用
- 假设用户下一轮会在本机真实点击 `/dev/control` 页面验证效果
- 假设第一阶段仍然不允许深改 `GameCore` / 存档

### Potential Gotchas

- PowerShell 的 `$PID` 是只读自动变量，脚本里不能再用 `$pid`
- 子 PowerShell 启动后端时，环境变量赋值要写成 `` `$env:...``，否则会在父进程里先被展开成空字符串
- 用户本机 `8787` 已有别的服务占用，当前默认端口必须记成 `18787`
- `backend-agent` 的测试页现在对 `bubble.show` 同时暴露了 `motion / emotion / graph`，不要把它再改回旧版单字段页面
- `shy -> pinch` 是推断，不是最终答案；如果真实效果不对，优先改映射表而不是重写桥接结构
- `GraphInfo.GraphType` 很多，但不是每个语义值都已经有稳定 graph 名；不要直接把 `happy/angry/sad` 承诺给后端
- `winConsole` 已经是很好的动作真相源，新对话需要核对动作时先看 `VPet-Simulator.Windows/WinDesign/winConsole.xaml`

## Environment State

### Tools/Services Used

- `.NET 8`：用于编译 `VPet-Simulator.Windows`
- `backend-agent/.venv`：已创建并安装 `fastapi / uvicorn / python-dotenv`
- `start-vpet-bridge-dev.ps1`：重新编译并同时拉起前后端
- `start-vpet-bridge-fast.ps1`：跳过编译同时拉起前后端
- `session-handoff` 脚本：已用于生成本 handoff

### Active Processes

- 本 handoff 创建时未主动保留后台服务状态
- 用户之前手动运行过后端并打开新 PowerShell 窗口，因此新对话开始前应默认检查旧的后端 / VPet 是否仍在运行
- 根目录启动脚本已内置“关闭旧 VPet 和占用后端端口的旧进程”逻辑

### Environment Variables

- `PET_BACKEND_HOST`
- `PET_BACKEND_PORT`
- `VPET_AGENT_BRIDGE_URL`
- `VPET_AGENT_BRIDGE_ENABLED`
- `VPET_AGENT_BRIDGE_INTERVAL_MS`
- `VPET_AGENT_BRIDGE_TIMEOUT_MS`
- `PET_LLM_BASE_URL`
- `PET_LLM_MODEL`
- `PET_LLM_API_KEY`
- `OPENAI_API_KEY`

## Related Resources

- `.codex/explore/desktop-pet-graduation-roadmap/state.md`
- `.codex/explore/desktop-pet-graduation-roadmap/decision-log.md`
- `.codex/explore/desktop-pet-graduation-roadmap/learnings.md`
- `.codex/explore/desktop-pet-vpet-body-bridge/state.md`
- `.codex/explore/desktop-pet-vpet-body-bridge/handoff.md`
- `docs/agent-desktop-pet/migration/2026-03-27-vpet-body-bridge-implementation-guide.md`
- `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`
- `VPet-Simulator.Windows/AgentBridge/AgentBridgePoller.cs`
- `backend-agent/app/api/routes/dev_control.py`
- `backend-agent/app/api/routes/events.py`
- `backend-agent/app/schemas/events.py`
- `start-vpet-bridge-dev.ps1`
- `start-vpet-bridge-fast.ps1`

---

**Security Reminder**: Before finalizing, run `validate_handoff.py` to check for accidental secret exposure.
