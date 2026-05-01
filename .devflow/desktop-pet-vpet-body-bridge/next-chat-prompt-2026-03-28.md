# 下个新对话提示词

继续 VPet 身体层桥接工作。使用 `context-budget-explore`，不要重新大范围分析，先读取并遵循这些文件：

1. `D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\state.md`
2. `D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\index.md`
3. `D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\2026-03-28-008-sleep-resume-ready.md`
4. `D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-graduation-roadmap\state.md`
5. `D:\Users\Mobius\Desktop\mine\AAA-code\VPet\docs\agent-desktop-pet\migration\2026-03-27-vpet-body-bridge-implementation-guide.md`
6. `D:\Users\Mobius\Desktop\mine\AAA-code\VPet\docs\agent-desktop-pet\migration\2026-03-27-vpet-bridge-motion-expression-map.md`

当前方向已经冻结：
- VPet 是身体层 / 前端执行层
- Python backend-agent 是大脑
- 第一阶段不要深改 GameCore

当前最新状态：
- `start-vpet-bridge.ps1` 已收口标准 `18787` 启动链路，默认不再走 `uvicorn --reload`
- `backend-agent` 当前已有 6 个 scenario，其中新增两个 4 步长链路：
  - `thinking-walk-think`
  - `bubble-move-touch-recover`
- `/dev/control` 默认 sequence 示例也已经升级成 4 步

下一步目标：
1. 继续在真实 VPet 运行态上联调 4 步 sequence/scenario
2. 采样状态时间线，而不只看后端事件顺序
3. 判断是否还要补少量桌宠运行态字段
4. 决定 `move.intent` 的最终退场方式

注意：
- 直接继续实现和联调，不要停留在纯分析
- 不要误提交 `.codex/AGENTS.md`、`zzz-cmd.md`、`VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/`

