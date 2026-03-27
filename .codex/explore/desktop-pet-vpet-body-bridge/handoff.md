# 交接文档

## 当前目标
完成 VPet 身体层桥接专项的第一阶段：实现最小外部事件桥 POC。

## 当前进度
- 已完成架构边界确认。
- 已确认现成代码挂点。
- 已形成详细 migration 指南。
- 已在 `VPet-Simulator.Windows/AgentBridge/` 落地最小桥接代码。
- 已把轮询器接入 `MainWindow.GameLoaded()` 之后启动，关闭窗口时释放。
- 已支持 `bubble.show`、`motion.play(idle)`、`motion.play(move)`。
- 已通过 `VPet-Simulator.Windows` x64 Debug 编译。
- 已补 `backend-agent` 轮询出口，测试页可直接驱动 VPet。
- 已新增动作/表情映射清单，可作为后端协议真相源。
- 已扩展支持 `motion.play` 多动作、`mode.switch`、`emotion.set` 以及 `bubble.show` 附带 `motion/expression/graph`。
- 已生成并校验通过的标准 handoff：
  - `.codex/explore/desktop-pet-vpet-body-bridge/handoffs/2026-03-27-143607-vpet-body-bridge-phase1.md`

## 下一步
1. 本地启动 VPet 和 `backend-agent`，用 `/dev/control` 验证“消息 + 动作 + 表情”组合事件。
2. 联调通过后把当前内置桥接收敛为 `MainPlugin` 插件。
3. 再补 `window.move` / 最小状态回传 / 运行时 graph 导出。

## 恢复指引
先看本文件，再读专项 `state.md`，然后打开最新标准 handoff：
` .codex/explore/desktop-pet-vpet-body-bridge/handoffs/2026-03-27-143607-vpet-body-bridge-phase1.md`
最后直接从“本地运行联调”开始。
