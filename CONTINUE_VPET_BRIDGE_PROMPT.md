# VPet Bridge Continue Prompt

把下面整段复制到新对话里即可：

```text
继续 VPet 身体层桥接工作。使用 context-budget-explore。先读取并遵循这些文件，不要重新大范围分析：

1. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\state.md
2. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\decision-log.md
3. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\checkpoints.md
4. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\index.md
5. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\2026-03-29-013-sleep-handoff-after-event-correlation.md
6. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\spec\protocol-phase1.md
7. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.explore\desktop-pet-vpet-body-bridge\quick-tests.json

当前方向已经冻结：
- VPet 是身体层 / 前端执行层
- Python backend-agent 是大脑
- 第一阶段不要深改 GameCore

当前已经完成：
- 桥接已收敛为 MainPlugin 插件：VPet.Plugin.AgentBridge
- /dev/control 与 /dev/quick-test 已可用于联调
- bubble.show / motion.play / mode.switch / emotion.set / window.move 已可用
- window.move 已支持 style=smart|smooth|snap
- quick-tests.json 已成为当前阶段测试目录与结果回写入口
- 移动从“乱走/乱爬”已经收口到可控语义
- sequence 已支持最小 wait_for 门控：
  - event_applied
  - move_complete
  - motion_complete
- 已新增最小事件关联字段：
  - event_id
  - sequence_name
  - step_index
  - last_event_id
  - last_sequence_name
  - last_step_index
- 已新增 6 步 story sequence：
  - sequence-think-speak-move-touch-speak-recover

注意：
- 当前移动协议已经收敛为显式 window.move(dx, dy)
- move.intent 只保留 legacy 兼容，不要再把 follow_cursor 一类 intent 当主方向
- 原生 walk/crawl/fall move graph 不是普通过场动画，而是桌宠自己的 move 系统
- 不要再把 DisplayMove 和桥接显式位移绑在同一次移动里
- 如果修改插件后要重编，先停掉 VPet，否则 DLL 会被锁住
- 不要替我跑真实联调；如果要补测试，只更新 quick-tests.json，真实结果由我自己回写

你接下来直接做：
1. 不要重新做大范围方案分析
2. 不要替我跑真实测试
3. 优先根据我回写的 quick-tests.json 继续收口协议和实现
4. 如果我要继续扩 story sequence，优先用 event_id / sequence_name / step_index 做关联，不要先扩更多工作态字段
5. 每轮结束同步 state.md 和 checkpoints.md；如果有方向性决策，更新 decision-log.md

当前待我自己真实联调的重点测试：
- sequence-think-speak-move-touch-speak-recover

重点观察：
- 时间线能否读出：
  - mode.switch
  - bubble.show
  - window.move
  - motion.play
  - bubble.show
  - mode.switch
- 两次 bubble.show 是否能通过 last_event_id / last_sequence_name / last_step_index 明确区分
- touch_head 完成后再进入第二次 bubble.show

先继续实现和收口，不要停留在纯分析。
```

更短的版本：

```text
继续 VPet 身体层桥接工作。使用 context-budget-explore。先读 state / decision-log / checkpoints / 最新 handoff / protocol-phase1 / quick-tests，然后不要做大范围重分析，也不要替我跑真实测试。当前重点是等待我自己回写 sequence-think-speak-move-touch-speak-recover 的真实结果，再继续收口实现与协议。
```
