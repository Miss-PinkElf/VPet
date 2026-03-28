# Proposal

## Goal

将 `VPet` 收敛为桌宠系统中的前端执行层 / 身体层，由外部 `Python backend-agent` 作为大脑驱动。

第一阶段目标不是深改 `GameCore`，而是在插件化桥接前提下，稳定对外暴露一组最小、明确、可联调、可集成的前端执行协议。

## Scope

- 保留并收口第一阶段正式执行能力
- 明确 legacy 协议的降级位置
- 明确后端应该如何调用 VPet，而不是继续依赖 dev 页面
- 将状态回传字段收口到足以支撑第一阶段联调与集成验证的范围
- 为关键 sequence 步骤补最小完成门控，而不是继续长期依赖猜 delay

## Out Of Scope

- 深改 `GameCore`
- 扩完整行为树或任务系统
- 承诺任意 emotion 到 graph 的自动映射
- 扩大量桌宠内部工作态字段

## Current Contract Artifact

第一阶段正式对外协议清单见：

- [protocol-phase1.md](D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\spec\protocol-phase1.md)
