继续 VPet 身体层桥接工作。先读取并遵循这些文件，不要重新大范围分析：

1. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\state.md
2. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\checkpoints.md
3. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\index.md
4. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\2026-03-29-012-sleep-handoff-after-sequence-gating.md
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
- sequence 已支持最小 wait_for 门控：
  - event_applied
  - move_complete
  - motion_complete
- thinking-walk-think 与 bubble-move-touch-recover 已切到关键步显式门控

注意：
- 当前移动协议已经收敛为显式 window.move(dx, dy)
- move.intent 只保留 legacy 兼容，不要再把 follow_cursor 一类 intent 当主方向
- 原生 walk/crawl/fall move graph 不是普通过场动画，而是桌宠自己的 move 系统
- 不要再把 DisplayMove 和桥接显式位移绑在同一次移动里
- 修改插件后，先停掉 VPet，再重编，否则 DLL 会被锁住

你接下来直接做：
1. 不要重新做大范围方案分析
2. 先拉起真实联调链路
3. 最小复测两条核心 sequence：
   - thinking-walk-think
   - bubble-move-touch-recover
4. 最小复测三条 window.move(style=smart) 单测
5. 直接把真实结果回写到 quick-tests.json
6. 根据真实结果判断：
   - 当前 wait_for 门控是否已经解决“动作没做完就进下一步”
   - 是否还需要把 motion_complete 下探到原生回调
   - 是否需要 native_walk

先继续实现和验证，不要停留在纯分析。
