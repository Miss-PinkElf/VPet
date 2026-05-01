# Handoff: VPet 身体层桥接 context save after sequence/scenario

## Session Metadata
- Created: 2026-03-27
- Project: `D:\Users\Mobius\Desktop\mine\AAA-code\VPet`
- Mission: `.explore/desktop-pet-vpet-body-bridge`
- Branch: `shuowang/dev-vpet`
- Session focus: 保存当前进度，压缩上下文，准备在新对话里继续

## Current Goal

继续把 VPet 作为身体层的第一阶段桥接打磨到“可稳定演示”的程度。当前重点已经从单条事件打通，转到：

1. 让后端 sequence/scenario 编排真正成为联调主入口
2. 收掉标准 `18787` 启动链路中的旧 backend 残留问题
3. 再继续看是否需要少量补充状态字段与 `move.intent` 的退场

## Current State

- `VPet.Plugin.AgentBridge` 仍是唯一桥接实现
- `window.move(dx, dy)` 仍是第一阶段唯一主移动协议
- `move.intent` 只保留最薄 legacy 兼容
- 最小状态快照已扩展到：
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
- `backend-agent` 已新增：
  - `GET /api/dev/scenarios`
  - `POST /api/dev/scenarios/{scenario_id}`
  - `POST /api/dev/sequences`
- `/dev/control` 已新增：
  - 后端驱动的 scenario 目录按钮
  - 自定义 sequence JSON 入口

## What Was Completed

- sequence/scenario 编排已经下沉到后端，不再主要写死在浏览器脚本里
- 迁移文档已更新到当前真实状态：
  - 状态字段集合
  - sequence/scenario 用法
  - `18787` 旧 `uvicorn --reload` 进程残留的已知坑
- `.explore` 已补齐：
  - `state.md`
  - `checkpoints.md`
  - `handoffs/index.md`

## Validation Evidence

- `python -m compileall backend-agent/app` 通过
- 代码级验证通过：
  - `dev_control_page()` HTML 已包含 `sequence-editor`
  - `list_dev_scenarios(...)` 返回 4 个预设场景
  - `trigger_dev_sequence(...)` 返回 `accepted`
- 服务级验证通过：
  - 自定义 sequence 会按延迟顺序写入事件总线
  - 预设 `move-then-motion` 会先发 `window.move` 再发 `motion.play`
- 端口隔离活体验证通过：
  - 在 `18788` 端口直起当前后端时，新接口与新页面可正常访问

## Open Problem

当前唯一明确未收口的问题是：

- 标准 `18787` 启动链路在本会话里仍可能落到旧 `uvicorn --reload` 进程
- 结果是：
  - `http://127.0.0.1:18787/api/dev/scenarios` 可能返回 `404`
  - `http://127.0.0.1:18787/dev/control` 可能继续显示旧页面

这个问题已经记录，但还没有彻底根治。不要把它误判成 sequence/scenario 功能本身没实现。

## Immediate Next Steps

1. 先排查并清理所有 `app.main:app --port 18787` 相关旧进程
2. 重新验证标准 `18787` 链路是否能提供新的 `/api/dev/scenarios` 和 `sequence-editor`
3. 再继续做更长链路 sequence/scenario 编排验证
4. 视情况决定是否补少量桌宠运行态字段，以及 `move.intent` 的最终退场节奏

## Resume Guidance

恢复时按这个顺序读：

1. `.explore/desktop-pet-vpet-body-bridge/state.md`
2. `.explore/desktop-pet-vpet-body-bridge/handoffs/index.md`
3. 本文件
4. `docs/agent-desktop-pet/migration/2026-03-27-vpet-body-bridge-implementation-guide.md`
5. `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`

## Important Gotchas

- 改插件 DLL 前，必须先停掉 VPet
- 如果 `18787` 上看到旧页面，不要先怀疑代码没写进去，先怀疑旧 backend 进程没清掉
- `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/` 是构建产物目录，不应直接进提交
- 当前工作区里有一个无关未跟踪文件 `zzz-cmd.md`，不要误提交它
