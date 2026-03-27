# Handoff: VPet 身体层桥接插件化续接

## 当前目标
- 在已插件化的桥接版本上继续补身体层控制能力，优先做 `window.move` 和最小状态回传。

## 当前进度
- 第一阶段桥接路线已经验证成立。
- 桥接已从主工程内置实现收敛到 `VPet.Plugin.AgentBridge/`。
- 插件已输出到 `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/`。
- `/dev/control` 已改为更适合联调的下拉式页面。
- `bubble.show + touch_head/touch_body/pinch/thinking` 已改为更接近原生的动作+说话编排。

## 关键文件
- `VPet.Plugin.AgentBridge/AgentBridgePlugin.cs`
- `VPet.Plugin.AgentBridge/AgentBridgePoller.cs`
- `VPet.Plugin.AgentBridge/AgentBridgeConfig.cs`
- `VPet-Simulator.Windows/mod/1200_AgentBridge/info.lps`
- `backend-agent/app/api/routes/dev_control.py`
- `docs/agent-desktop-pet/migration/2026-03-27-vpet-bridge-motion-expression-map.md`

## 当前最重要的事实
- 这条链路已经不需要再证明“能不能做身体层”。
- 当前重点是补身体层控制缺口，而不是继续讨论路线。
- `move.intent` 还没有接到 VPet 身体层，所以测试页里这项目前发了不会生效。

## 下一步
1. 补 `window.move`
2. 设计并实现最小状态回传
3. 视需要继续完善 graph 映射与测试页提示

## 恢复指引
1. 先读 `state.md`
2. 再读本 handoff
3. 如需历史上下文，再读 `2026-03-27-001-phase1-import.md`
