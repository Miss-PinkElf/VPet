# 当前状态

## 当前阶段
- 阶段 2：第一阶段最小桥接 POC 已联调并收敛为插件，准备继续补身体层控制

## 已确认的事实
- 当前 VPet 仓库已经可以在本机启动。
- VPet 在毕设中的角色已经冻结为身体层 / 前端执行层。
- `Python backend-agent` 是大脑。
- 第一阶段最小桥接已收敛为独立插件工程 `VPet.Plugin.AgentBridge/`，并产出到 `VPet-Simulator.Windows/mod/1200_AgentBridge/plugin/`。
- 桥接现由 `MainPlugin.GameLoaded()` 启动，`EndGame()` 释放，不再内置在主工程生命周期钩子里。
- 现有 `backend-agent` 已补齐 `GET /vpet/events/next`，并保留原有 `/dev/control` 测试页。
- 当前桥接已扩展支持：
  - `motion.play(idle|move|normal|touch_head|touch_body|sleep|raised|state_one|pinch|thinking)`
  - `mode.switch(thinking|normal)`
  - `emotion.set`
  - `bubble.show` 附带 `motion` / `expression` / `graph`
- 其中 `bubble.show + touch_head/touch_body/pinch/thinking` 已改为更接近 VPet 原生的动作+说话编排。

## 工作假设
- 当前毕设主线已经从“能不能做身体层”转到“怎么继续补身体层能力”。
- 后续记录和续接应统一写入 `.explore/desktop-pet-graduation-roadmap/`。

## 待解决的问题
- `window.move` 和最小状态回传在哪一轮补齐。
- 论文与答辩材料中如何组织“VPet 身体层化”的过程叙事。

## 下一步
- 在插件化版本上继续验证组合事件体感。
- 补 `window.move`。
- 再补最小状态回传，形成更完整闭环。

## 最新 handoff
- 无

## 最小活跃上下文摘要
- 当前方向已冻结：VPet 只做身体层，Python 做大脑。第一阶段桥接已经完成插件化收敛；当前重点是继续补身体层控制能力。
