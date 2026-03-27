# VPet Bridge Continue Prompt

把下面整段复制到新设备上的新对话里即可：

```text
继续 VPet 身体层桥接工作。先读取并遵循这些文件，不要重新大范围分析：

1. E:\Learn\Vs\Code\VPet\.explore\desktop-pet-vpet-body-bridge\state.md
2. E:\Learn\Vs\Code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\index.md
3. E:\Learn\Vs\Code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\2026-03-27-004-window-move-state-loop.md
4. E:\Learn\Vs\Code\VPet\.explore\desktop-pet-graduation-roadmap\state.md
5. E:\Learn\Vs\Code\VPet\docs\agent-desktop-pet\migration\2026-03-27-vpet-bridge-motion-expression-map.md

当前方向已经冻结：
- VPet 是身体层 / 前端执行层
- Python backend-agent 是大脑
- 第一阶段不要深改 GameCore

当前已经完成：
- 桥接已收敛为 MainPlugin 插件：VPet.Plugin.AgentBridge
- /dev/control 已可用于真实联调
- bubble.show / motion.play / mode.switch / emotion.set 已可用
- bubble.show + touch_head/touch_body/pinch/thinking 已改为更接近原生的动作+说话编排
- window.move 已接到 VPet 身体层
- 最小状态回传已打通：/vpet/state + /api/dev/state
- 已做过一次真实联调：window.move dx=120 dy=-40，状态增量与请求一致
- .explore 已成为新的 mission 真相源

注意：
- 当前移动协议已经收敛为显式 window.move(dx, dy)
- move.intent 只保留 legacy 兼容，不要再把 follow_cursor 一类 intent 当成第一阶段主方向
- 如果本地联调时事件队列不消费，先检查运行中的 Setting.lps 是否启用了 onmod:|agentbridge:|
- 修改插件后，先停掉 VPet，再重编，否则 DLL 会被锁住

你接下来直接做：
1. 继续验证 window.move 与 bubble.show / motion.play 的组合体感
2. 评估最小状态回传是否要补边界距离或更多工作态字段
3. 决定 move.intent 是否进一步降级为纯 legacy 文档兼容
4. 更新 .explore 下的 state / checkpoints / handoff

先继续实现和联调，不要停留在纯分析。
```

更短的版本：

```text
继续 VPet 身体层桥接工作，先读根目录 CONTINUE_VPET_BRIDGE_PROMPT.md 里列出的 .explore/state/handoff 和迁移文档，然后直接从 window.move 已打通后的下一步开始实现与联调。
```
