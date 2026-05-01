继续 VPet 身体层桥接工作。先读取并遵循这些文件，不要重新大范围分析：

1. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\state.md
2. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\checkpoints.md
3. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\index.md
4. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\2026-03-28-010-smart-move-and-sequence-gating-next.md
5. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\spec\protocol-phase1.md
6. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\quick-tests.json

当前方向已经冻结：
- VPet 是身体层 / 前端执行层
- Python backend-agent 是大脑
- 第一阶段不要深改 GameCore

当前已经完成：
- 桥接已收敛为 MainPlugin 插件：VPet.Plugin.AgentBridge
- /dev/control 与 /dev/quick-test 已可用于真实联调
- bubble.show / motion.play / mode.switch / emotion.set / window.move 已可用
- window.move 已支持 style=smart|smooth|snap
- quick-tests.json 已成为当前阶段测试目录与结果回写入口
- 移动从“乱走/乱爬”已经收口到可控语义
- 当前主要问题已经从“协议错”收口到“sequence 仍然是 delay 编排，动作没做完就进下一步”

注意：
- 当前移动协议已经收敛为显式 window.move(dx, dy)
- move.intent 只保留 legacy 兼容，不要再把 follow_cursor 一类 intent 当主方向
- 原生 walk/crawl/fall move graph 不是普通过场动画，而是桌宠自己的 move 系统
- 不要再把 DisplayMove 和桥接显式位移绑在同一次移动里
- 修改插件后，先停掉 VPet，再重编，否则 DLL 会被锁住

你接下来直接做：
1. 不再继续单纯猜 delay
2. 优先探索并实现 sequence 的“动作完成门控”
3. 目标是让关键步骤能做到“上一步完成后再进入下一步”
4. 如有必要，再讨论是否引入 native_walk 一类由原生 move 系统独占移动权的模式
5. 更新 .explore 下的 state / checkpoints / handoff

先继续实现，不要停留在纯分析。
