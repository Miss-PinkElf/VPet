# 当前状态

## 当前阶段
- 阶段 2：第一阶段桥接已形成 `window.move + state` 闭环，并开始打磨组合体感

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
  - `window.move(dx, dy)`
- 其中 `bubble.show + touch_head/touch_body/pinch/thinking` 已改为更接近 VPet 原生的动作+说话编排。
- 最小状态回传已经打通，并在本轮扩到更适合组合联调的字段集合。

## 工作假设
- 当前毕设主线已经从“能不能做身体层”转到“怎么继续补身体层能力”。
- 后续记录和续接应统一写入 `.explore/desktop-pet-graduation-roadmap/`。

## 待解决的问题
- 组合编排是否要继续往场景层收敛，而不只停留在单条事件。
- 论文与答辩材料中如何组织“VPet 身体层化”的过程叙事。

## 下一步
- 在插件化版本上继续验证组合事件体感与状态可观测性。
- 判断第一阶段身体层协议是否已经足够支撑论文演示。
- 继续沉淀“VPet 作为身体层、Python 作为大脑”的迁移叙事。

## 最新 handoff
- 无

## 最小活跃上下文摘要
- 当前方向已冻结：VPet 只做身体层，Python 做大脑。第一阶段桥接已经完成插件化收敛与基础闭环；当前重点是继续打磨组合编排和演示可观测性。
