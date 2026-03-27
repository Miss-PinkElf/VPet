# Handoff: VPet 身体层桥接最小 sequence/scenario 联调入口

## Session Metadata
- Created: 2026-03-27
- Project: `D:\Users\Mobius\Desktop\mine\AAA-code\VPet`
- Mission: `.explore/desktop-pet-vpet-body-bridge`
- Branch: `shuowang/dev-vpet`
- Session focus: 在 `backend-agent` 中补最小 sequence/scenario 入口，并同步完善联调与迁移文档

## Current State Summary

这一轮的主目标已经完成：组合编排不再主要写死在 `/dev/control` 前端脚本里，而是下沉到了后端 `backend-agent`。当前后端新增了三个入口：`GET /api/dev/scenarios`、`POST /api/dev/scenarios/{scenario_id}`、`POST /api/dev/sequences`。联调页已经改成读取后端 scenario 目录，并提供一个最小自定义 sequence JSON 入口。迁移文档也同步更新，纳入了扩展后的状态字段与 sequence/scenario 用法。

## Work Completed

### Code Changes

- `backend-agent/app/schemas/events.py`
  - 新增：
    - `DevSequenceStepRequest`
    - `DevSequenceRequest`
    - `DevSequenceDispatchResponse`
    - `DevScenarioSummary`
    - `DevScenarioListResponse`
- `backend-agent/app/services/dev_sequence_orchestrator.py`
  - 新增最小编排层
  - 支持预设 scenario 目录与自定义 sequence
  - 复用既有 `DevEventRequest -> PetEvent` 转换
- `backend-agent/app/services/app_services.py`
  - 注入 `DevSequenceOrchestrator`
- `backend-agent/app/api/routes/dev_control.py`
  - 新增 `/api/dev/scenarios`
  - 新增 `/api/dev/scenarios/{scenario_id}`
  - 新增 `/api/dev/sequences`
  - `/dev/control` 改成后端驱动的 scenario 按钮
  - `/dev/control` 新增自定义 sequence JSON 入口
- `start-vpet-bridge.ps1`
  - 补充对 `uvicorn --reload` 父子进程的额外清理

### Documentation Changes

- `docs/agent-desktop-pet/migration/2026-03-27-vpet-body-bridge-implementation-guide.md`
  - 补 sequence/scenario 联调入口
  - 更新状态回传示例
- `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`
  - 把状态字段更新到当前真实集合
  - 补 sequence/scenario 用法说明

## Validation Evidence

- Python 语法检查通过：
  - `python -m compileall backend-agent/app`
- 代码级路由与页面验证通过：
  - `dev_control_page()` 返回的 HTML 已包含 `sequence-editor`
  - `list_dev_scenarios(...)` 返回 4 个预设场景
  - `trigger_dev_sequence(...)` 返回 `status=accepted`
- 服务级编排验证通过：
  - 自定义 sequence 下发后，事件总线按顺序收到：
    - `bubble.show`
    - `window.move`
  - 预设 `move-then-motion` 下发后，事件总线按顺序收到：
    - `window.move`
    - `motion.play(touch_head)`
- 端口隔离活体验证通过：
  - 在 `18788` 端口直起当前后端后，`GET /api/dev/scenarios` 返回新接口数据
  - `GET /dev/control` 页面中可见 `sequence-editor`

## Open Questions / Risks

- 本会话里标准 `18787` 启动链路仍可能被旧 `uvicorn --reload` 进程劫持，导致 `/dev/control` 继续显示旧页面
- 这不影响当前 sequence/scenario 代码本身已实现，但会影响默认联调体验
- 现有状态字段是否已经足够支撑更长链路编排验证，仍待下一轮判断

## Immediate Next Steps

1. 排查并修复标准 `18787` 启动链路的旧 backend 残留问题
2. 基于新的 sequence/scenario 入口继续验证更长链路的组合编排
3. 判断是否还要补少量桌宠运行态字段，以及 `move.intent` 的最终退场节奏

## Context for Resuming Agent

### Important Context

- 当前 `.explore/desktop-pet-vpet-body-bridge/` 仍是唯一真相源
- `window.move(dx, dy)` 仍是第一阶段唯一主移动协议
- 组合场景现在优先走后端 `sequence/scenario` 入口，不再依赖前端脚本里的本地数组
- 文档已经同步到当前真实字段和入口，不要再沿用旧的“最小状态只有 left/top/display”描述

### Potential Gotchas

- `start-vpet-bridge.ps1` 已尝试补 `uvicorn --reload` 家族进程清理，但本会话里 18787 仍可能落到旧后端
- 如果要验证标准端口链路，先把所有 `app.main:app --port 18787` 相关进程清理干净，再重试
- 插件 DLL 仍会被运行中的 VPet 锁住；改插件前先停 VPet 再编译
