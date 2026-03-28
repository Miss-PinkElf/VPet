# Design

## Design Focus

本 mission 的设计重点已经从“桥接能否成立”收口到“VPet 作为前端执行层时，第一阶段正式对外协议是什么”。

## Core Decisions

- `VPet` 只做身体层 / 前端执行层
- `Python backend-agent` 做大脑
- 第一阶段不深改 `GameCore`
- 移动协议正式收敛为显式 `window.move(dx, dy)`
- `move.intent` 只保留 legacy 兼容，不再作为正式主调用面
- 后端负责 sequence/behavior 编排，VPet 负责执行和状态回传
- sequence 对关键步骤补最小 `wait_for` 门控，优先覆盖 `window.move` 和短动作完成判断

## Contract Source

第一阶段正式对外协议清单见：

- [protocol-phase1.md](D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\spec\protocol-phase1.md)

## Supporting References

现阶段实现与迁移真相主要在：
- `VPet.Plugin.AgentBridge/`
- `docs/agent-desktop-pet/migration/2026-03-27-vpet-body-bridge-implementation-guide.md`
- `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`
