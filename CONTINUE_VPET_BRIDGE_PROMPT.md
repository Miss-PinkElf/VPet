# VPet Bridge Continue Prompt

把下面整段复制到新对话里即可：

```text
继续 VPet 身体层桥接工作。使用 context-budget-explore，并把 `.explore/desktop-pet-vpet-body-bridge/` 作为当前 mission 真相源。先读取并遵循这些文件，不要重新大范围分析：

1. E:\Learn\Vs\Code\VPet\.explore\desktop-pet-vpet-body-bridge\state.md
2. E:\Learn\Vs\Code\VPet\.explore\desktop-pet-vpet-body-bridge\decision-log.md
3. E:\Learn\Vs\Code\VPet\.explore\desktop-pet-vpet-body-bridge\checkpoints.md
4. E:\Learn\Vs\Code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\index.md
5. E:\Learn\Vs\Code\VPet\.explore\desktop-pet-vpet-body-bridge\handoffs\2026-03-31-015-phase1-sequence-acceptable-walk-next.md
6. E:\Learn\Vs\Code\VPet\.explore\desktop-pet-vpet-body-bridge\spec\protocol-phase1.md
7. E:\Learn\Vs\Code\VPet\.explore\desktop-pet-vpet-body-bridge\spec\display-control-surface-and-full-control-plan.md
8. E:\Learn\Vs\Code\VPet\.explore\desktop-pet-vpet-body-bridge\quick-tests.json

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
  - motion_recovered
- 已新增最小事件关联字段：
  - event_id
  - sequence_name
  - step_index
  - last_event_id
  - last_sequence_name
  - last_step_index
- 已新增 6 步 story sequence：
  - sequence-think-speak-move-touch-speak-recover
- 这条 6 步 sequence 已在多轮收口后达到可接受范围：
  - 当前结果可视为 pass
  - 最新真实反馈是“还行流畅度可以，只有一点点卡顿，可以接受”
- 已完成一轮新的源码级梳理：
  - 当前桥接暴露面远小于 VPet 展示层本体真实能力
  - 已产出展示层全控专题设计文档
  - 如果后续要扩控制面，优先方向是：
    - graph.catalog
    - graph.play
    - behavior.invoke

注意：
- 当前移动协议已经收敛为显式 window.move(dx, dy)
- move.intent 只保留 legacy 兼容，不要再把 follow_cursor 一类 intent 当主方向
- 原生 walk/crawl/fall move graph 不是普通过场动画，而是桌宠自己的 move 系统
- 不要再把 DisplayMove 和桥接显式位移绑在同一次移动里
- 不要把 `display-control-surface-and-full-control-plan.md` 误当成“当前已经实现的正式协议”
- `protocol-phase1.md` 才是当前已正式承诺的最小边界
- 如果修改插件后要重编，先停掉 VPet，否则 DLL 会被锁住
- 不要替我跑真实联调；如果要补测试，只更新 quick-tests.json，真实结果由我自己回写
- 不要把原生 `DisplayMove()` 重新绑回 `window.move`

你接下来直接做：
1. 不要重新做大范围方案分析
2. 不要替我跑真实测试
3. 当前先继续 phase 1，不要提前进入 phase 2
4. 不要再优先死抠 6 步 story sequence；它已经是当前可接受基线
5. 直接把主焦点转向：
   - `window.move(style=smart)` 的走路体感为什么仍然生硬
6. 如果要探索原生走路能力：
   - 必须和 `window.move(dx, dy)` 正式语义分开
   - 不要把原生 move graph 和桥接显式位移重新绑在同一次移动里
7. phase 2 仍保持冻结：
   - `graph.catalog`
   - `graph.play`
   - `behavior.invoke`
8. 每轮结束同步 state.md 和 checkpoints.md；如果有方向性决策，更新 decision-log.md

除非我明确要求，否则不要重新做大范围路线比较；直接在当前 mission 上继续推进和落盘。
```

更短的版本：

```text
继续 VPet 身体层桥接工作。使用 context-budget-explore。先读 state / decision-log / checkpoints / 最新 handoff / protocol-phase1 / display-control-surface-and-full-control-plan / quick-tests，然后不要做大范围重分析，也不要替我跑真实测试。当前先继续 phase 1，不要再死抠 6 步 story sequence，直接转向 window.move(style=smart) 的走路体感问题；phase 2 的 graph.catalog / graph.play / behavior.invoke 先别提前展开。
```
