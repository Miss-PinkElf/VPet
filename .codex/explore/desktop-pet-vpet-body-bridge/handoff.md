# 交接文档

## 当前目标
完成 VPet 身体层桥接专项第一阶段，并在此基础上继续补身体层控制能力。

## 当前进度
- 已完成架构边界确认。
- 已确认现成代码挂点。
- 已形成详细 migration 指南。
- 已在 `VPet.Plugin.AgentBridge/` 收敛出独立插件工程。
- 已由 `MainPlugin.GameLoaded()` 接管桥接启动，`EndGame()` 负责释放。
- 已支持 `bubble.show`、`motion.play(idle)`、`motion.play(move)`。
- 已通过 `VPet-Simulator.Windows` x64 Debug 编译。
- 已补 `backend-agent` 轮询出口，测试页可直接驱动 VPet。
- 已新增动作/表情映射清单，可作为后端协议真相源。
- 已扩展支持 `motion.play` 多动作、`mode.switch`、`emotion.set` 以及 `bubble.show` 附带 `motion/expression/graph`。
- 已把 `/dev/control` 的 `motion / emotion / graph / mode / intent` 改为下拉框，便于真实联调。
- 已把 `bubble.show + touch_head/touch_body/pinch/thinking` 调整为更接近原生的动作+说话编排。
- 插件 DLL 已产出到 `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/VPet.Plugin.AgentBridge.dll`。
- 已生成并校验通过的标准 handoff：
  - `.codex/explore/desktop-pet-vpet-body-bridge/handoffs/2026-03-27-143607-vpet-body-bridge-phase1.md`

## 下一步
1. 在插件化版本上继续验证 `bubble.show + touch_head/touch_body/pinch/thinking` 的体感是否稳定。
2. 补 `window.move`。
3. 再补最小状态回传 / 运行时 graph 导出。

## 恢复指引
先看本文件，再读专项 `state.md`，然后打开最新标准 handoff：
` .codex/explore/desktop-pet-vpet-body-bridge/handoffs/2026-03-27-143607-vpet-body-bridge-phase1.md`
最后直接从“插件化版本继续联调”开始。
