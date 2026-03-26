# Design

## Overview

- Chosen approach:
  - 使用单一 change workspace 管理“桌宠项目路线拆分”这一变更，工件层面固定为 `proposal.md`、`design.md` 和 `tasks.md`。
  - 设计上采用“一个产品主线，三个实现阶段，多个原子任务”的结构。
  - 第一阶段只实现最小闭环：桌宠展示、基础交互、文本聊天、基础记忆、轻量上下文感知和可演示脚本。
  - 第一阶段的前端交互细化为：hover 出现高亮边框和右侧竖向 toolbar，离开后延迟隐藏；顶部拖拽把手负责移动窗口；右下角缩放手柄负责同步改变窗口尺寸和模型比例；点击对话按钮后展开最小聊天面板。
  - 本轮对话闭环采用“本地 HTTP + 后端 LLM 代理”方案：前端 React 直接调用本地 Python `FastAPI` 服务；后端统一封装 OpenAI 兼容 `chat/completions`，前端不接触模型密钥。
  - 后端结构重构为 `app/api + app/services + app/memory + app/schemas + app/core`，让对话编排、事件分发和记忆接口分层清晰。
  - 事件协议扩展为完整高层结构：`emotion.set`、`motion.play`、`bubble.show`、`mode.switch`、`move.intent`；前端新增最小 `Pet Controller` 统一分发这些事件。
  - 第二阶段强化体验和可扩展架构，第三阶段再探索长期陪伴与关系记忆。
- Why this approach:
  - 这样可以避免每次实现都重新解析整份 PRD。
  - 这样能将“毕设优先”和“长期产品目标”放入同一路线图而不互相冲突。
  - 这样能让任务切片更小，更适合在有限上下文内单独推进和验证。
  - 将 hover 态、拖拽和缩放拆分为独立交互层，可以避免 Electron 原生拖拽区域与 React 按钮点击互相冲突。
  - 对话入口先走本地 HTTP，而不是主进程桥接，可以更快固定接口契约，并为后续记忆和上下文接口留出标准化 API 层。
  - 用统一宽度基准派生 UI 尺寸，可以避免外框变化而 toolbar 仍保持固定像素，导致整体割裂。

## Structure

- Affected pages or components:
  - `backend/main.py`: 保留为兼容入口，转发到模块化后的 `app.main`。
  - `backend/app/main.py`: 创建 `FastAPI` 应用并装配服务容器。
  - `backend/app/api/routes/*`: 承载健康检查、聊天、事件流、联调控制页等 HTTP 路由。
  - `backend/app/services/*`: 承载对话编排、LLM 调用、事件总线、行为策略和记忆服务。
  - `backend/app/memory/*`: 承载低耦合记忆抽象和占位实现。
  - `backend/app/schemas/*`: 承载聊天、完整 `PetEvent` 协议和记忆数据结构。
  - `backend/app/core/config.py`: 承载环境变量和运行配置。
  - `backend/run-dev.sh`: 提供后端单独启动脚本，便于只启动 Python 服务做联调。
  - `backend/run-dev.ps1`: 提供 Windows / PowerShell 的后端单独启动脚本。
  - `backend/requirements.txt`: 固定后端最小依赖。
  - `frontend/src/App.tsx`: 负责 hover 态、toolbar 渲染、拖拽移动、右下角缩放、聊天面板状态、独立对话气泡状态、后端事件订阅和消息发送流程。
  - `frontend/src/App.module.scss`: 负责边框、toolbar、缩放手柄、聊天面板和独立对话气泡视觉样式。
  - `frontend/src/petBackend.ts`: 封装前端访问后端 HTTP 服务和订阅后端事件流的接口层。
  - `frontend/src/petController.ts`: 提供最小前端控制层，统一分发高层事件并维护当前桌宠状态。
  - `frontend/src/components/Live2DWidget/index.tsx`: 消费最小 `Pet Controller` 的表情状态，执行基础表情映射。
  - `frontend/src/main.ts`: 继续负责透明窗口创建、最小尺寸约束，以及通过 IPC 暴露窗口 bounds 查询与更新能力。
  - `frontend/src/preload.ts`: 继续暴露 `petWindow` 桥接 API 给渲染层。
  - `package.json`: 提供统一启动入口，可同时启动前端和后端。
  - `scripts/start-dev.js`: 负责并行拉起前后端开发进程并在退出时清理子进程。
  - `frontend/src/components/Live2DWidget/*`: 负责 PIXI 画布尺寸变化后的模型重新适配。
  - `openspec/changes/desktop-pet-companion-roadmap/*`: 同步补充变更范围、实现设计与任务验收。
- New modules or files:
  - `frontend/src/petBackend.ts`
  - `scripts/start-dev.js`
  - `backend/.env.example`
  - `backend/run-dev.sh`
  - `backend/run-dev.ps1`
- Reused modules or files:
  - [桌宠项目详细PRD.md](/Users/mobius/Documents/111AAA-code/agent-desktop-pet/zzz-doc/zzz-prompt-debug/plan/桌宠项目详细PRD.md)
  - [1.md](/Users/mobius/Documents/111AAA-code/agent-desktop-pet/zzz-doc/zzz-prompt-debug/origin/1.md)
  - [原始PRD.md](/Users/mobius/Documents/111AAA-code/agent-desktop-pet/zzz-doc/zzz-prompt-debug/origin/原始PRD.md)
  - [前端需求.md](/Users/mobius/Documents/111AAA-code/agent-desktop-pet/zzz-doc/zzz-prompt-debug/origin/前端需求.md)
  - [桌宠前端开发问题修复清单.md](/Users/mobius/Documents/111AAA-code/agent-desktop-pet/zzz-doc/桌宠前端开发问题修复清单.md)
  - [记忆相关.md](/Users/mobius/Documents/111AAA-code/agent-desktop-pet/zzz-doc/记忆相关.md)

## Data And State Flow

- Inputs:
  - 现有 PRD、原始需求文档、前端兼容性说明、记忆方案调研结论。
  - 用户确认的产品目标：可陪伴、尽可能像一个人、但前期以毕业设计交付为优先。
  - 用户补充的视觉稿，明确了右侧 toolbar 和右下角缩放手柄布局。
  - 用户提供的后端 LLM 文档，明确上游服务采用 OpenAI 兼容接口，并优先使用 `gpt-5.4` / `gpt-5.2`。
- State ownership:
  - `proposal.md` 持有业务目标、范围边界、约束和风险。
  - `design.md` 持有阶段划分思路、模块边界和后续预期结构。
  - `tasks.md` 持有按阶段拆解后的可执行任务清单与验收标准。
  - `App.tsx` 持有 hover 显隐、边框延迟隐藏、当前窗口尺寸、活动按钮、拖拽起点、缩放起点、聊天面板显隐、独立对话气泡、消息列表、输入值、请求状态和后端推送事件消费状态，并基于当前窗口宽高推导统一 UI 缩放比例与模型可视区尺寸。
  - `frontend/src/petBackend.ts` 持有前端与本地 HTTP 后端的请求契约，以及完整 `PetEvent` 订阅接口。
  - `frontend/src/petController.ts` 持有当前情绪、模式、动作、移动意图等前端本地状态，并把后端高层事件翻译为前端可执行状态。
  - `backend/app/services/chat_orchestrator.py` 持有对话主链路，但只依赖抽象化的 `memory_service` 和 `llm_service`。
  - `backend/app/services/memory_service.py` 持有记忆服务接口层，对底层存储适配器做隔离。
  - `backend/app/memory/*` 持有具体记忆实现，本轮先用低耦合占位实现，不把 `mem0` 写死在主链路中。
  - `useLive2DModel.ts` 持有模型实例，并根据模型可视区尺寸重新计算模型缩放与居中位置。
- Side effects:
  - 形成新的真相源，后续 Apply 阶段应以这些工件为准，而不是继续依赖聊天上下文。
  - 前端通过 preload 暴露的 IPC 接口调用主进程更新窗口位置和尺寸。
  - 前端通过 `fetch` 调用本地 Python HTTP 服务，后端再代理上游 OpenAI 兼容模型接口。
  - 前端通过后端事件流订阅完整 `PetEvent` 协议，接收来自后端测试页或后续行为引擎的主动推送。
  - 根目录启动脚本会并行拉起 Electron 前端和 Python 后端。
  - React 侧同时监听真实窗口 `resize` 事件，并重新读取主进程 bounds，保证边框拖拽和系统级尺寸变化也能触发联动缩放。
  - 窗口尺寸变化后，PIXI renderer 与 Live2D 模型会重新适配，保持视觉稿中的完整展示效果。
  - `PIXI.Application` 在窗口缩放场景中必须保持单例，只允许 resize，不允许因为 viewport 变化反复 destroy/recreate。
  - 主进程同时对最小宽高和最大宽高做钳制，避免窗口被拉到不可用或视觉失衡的区间。
- Output rendering path:
  - 用户鼠标进入桌宠区域 -> `App.tsx` 置为 hover visible -> 展示边框与 toolbar。
  - 用户按住顶部拖拽把手 -> renderer 计算屏幕坐标偏移 -> preload IPC -> 主进程更新窗口位置。
  - 用户按住右下角缩放手柄或触发真实窗口 resize -> renderer / 浏览器窗口触发尺寸变化 -> React 重新同步 bounds -> Live2D 画布、模型、toolbar 与边框按同一组布局 token 重算。
  - 用户点击 toolbar 中的对话按钮 -> `App.tsx` 展开聊天面板并聚焦输入框。
  - 用户发送文本 -> `frontend/src/petBackend.ts` 请求本地 `POST /api/chat` -> `backend/main.py` 调用上游 `chat/completions` -> 返回回复文本 -> 前端更新消息列表、状态标签，并触发与聊天面板分离的独立对话气泡，气泡数秒后自动消失。
  - 联调人员打开后端测试页 -> 选择一种高层事件并点击 `Send` -> 后端生成对应 `PetEvent` -> 前端事件流监听到推送 -> `Pet Controller` 分发事件 -> 更新独立对话气泡、当前情绪、模式、动作或移动意图。

## Interfaces

- APIs or services:
  - `petWindow.getBounds()`: 从主进程读取当前窗口位置和尺寸。
  - `petWindow.updateBounds(nextBounds)`: 允许渲染层更新窗口 `x / y / width / height`，并在主进程执行最小尺寸保护。
  - `GET /health`: 返回后端健康状态、模型名和是否已配置上游密钥。
  - `POST /api/chat`: 接收用户消息和最近消息历史，返回桌宠回复文本。
  - `GET /api/events`: 前端订阅后端推送事件流。
  - `GET /dev/control`: 返回后端测试页。
  - `POST /api/dev/messages`: 从测试页向前端推送一条桌宠消息。
- Types or data contracts:
  - `PetWindowBounds`: 窗口位置与尺寸结构，供渲染层与主进程共享。
  - `ToolbarActionKey`: toolbar 按钮标识，区分设置、缩放及占位按钮。
  - `DragStartPosition`: 顶部拖拽把手的起点状态。
  - `ResizeStartPosition`: 右下角缩放手柄的起点状态。
  - `ConversationMessage`: `{ id, role, content, status }`
  - `ChatRequest`: `{ message, history }`
  - `ChatResponse`: `{ reply, model }`
  - `ChatErrorResponse`: `{ detail }`
  - `PetEvent`
    - `bubble.show`: `{ type, text, duration_ms, source }`
    - `emotion.set`: `{ type, emotion, source }`
    - `motion.play`: `{ type, motion, priority, source }`
    - `mode.switch`: `{ type, mode, source }`
    - `move.intent`: `{ type, intent, source }`

## Risks

- Implementation risk:
  - 如果拖拽层和按钮层没有明确分离，容易出现 toolbar 无法点击、窗口误移动的问题。
  - 如果缩放只修改窗口大小而不重新适配模型，会出现模型裁切、偏移或留白。
  - 如果 hover 延迟隐藏时间过短，用户体验会接近“闪现闪退”，无法稳定操作边框和 toolbar。
  - 如果后端把上游错误原样泄漏到前端，用户会看到难以理解的供应商级报错。
  - 如果记忆接口和对话编排没有隔离，后续接入 `mem0` 或其他实现时会出现大面积返工。
- Migration or regression risk:
  - 后续如果直接跳过这些工件去编码，聊天上下文和代码实现会重新分叉。
  - 若未来更换记忆底层或模型供应商，没有接口层约束会导致大面积返工。
  - 若后续将 toolbar 上未实现按钮直接接入功能，需要继续保持视觉布局与 hover 交互稳定，不应破坏当前拖拽、缩放和聊天入口行为。
