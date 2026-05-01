# VPet Bridge Continue Prompt

把下面整段复制到新对话里即可：

```text
继续 VPet 身体层桥接工作。使用 $devflow，并把 `.devflow/desktop-pet-vpet-body-bridge/` 作为当前 mission 真相源。先走 devflow 的 resume 路径读取并遵循这些文件，不要重新大范围分析：

1. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.devflow\desktop-pet-vpet-body-bridge\state.md
2. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.devflow\desktop-pet-vpet-body-bridge\workflow.md
3. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.devflow\desktop-pet-vpet-body-bridge\decision-log.md
4. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.devflow\desktop-pet-vpet-body-bridge\checkpoints.md
5. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.devflow\desktop-pet-vpet-body-bridge\handoffs\index.md
6. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.devflow\desktop-pet-vpet-body-bridge\handoffs\2026-05-01-018-devflow-migration.md
7. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.devflow\desktop-pet-vpet-body-bridge\spec\protocol-phase1.md
8. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.devflow\desktop-pet-vpet-body-bridge\spec\display-control-surface-and-full-control-plan.md
9. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.devflow\desktop-pet-vpet-body-bridge\quick-tests.json

当前方向已经冻结：
- VPet 是身体层 / 前端执行层
- Python backend-agent 是大脑
- 第一阶段不要深改 GameCore
- 旧 `.explore/desktop-pet-vpet-body-bridge/` 只作为 legacy 参考，后续新记录、新 checkpoint、新 handoff、quick test 回写都写 `.devflow/desktop-pet-vpet-body-bridge/`

当前已经完成：
- 桥接已收敛为 MainPlugin 插件：VPet.Plugin.AgentBridge
- /dev/control 与 /dev/quick-test 已可用于联调
- /dev/quick-test 现在读写 `.devflow/desktop-pet-vpet-body-bridge/quick-tests.json`
- bubble.show / motion.play / mode.switch / emotion.set / window.move 已可用
- window.move 已支持 style=smart|smooth|snap
- sequence 已支持最小 wait_for 门控：
  - event_applied
  - move_complete
  - motion_complete
  - motion_recovered
- phase 1 的 emotion alias 边界已收口：
  - 正式 stable alias 继续只认 think / thinking / pinch
  - shy 只保留 legacy≈pinch 兼容
- quick-tests.json 已新增 3 条 emotion 回归项：
  - emotion-thinking
  - emotion-pinch
  - emotion-shy-legacy
- 6 步 story sequence 已达到可接受范围：
  - sequence-think-speak-move-touch-speak-recover = pass
  - 最新真实反馈是“还行流畅度可以，只有一点点卡顿，可以接受”

当前暂停状态非常重要：
- native move 分支已经记录完成并暂停
- 不要默认继续 native.move.direction
- 如果用户没有明确说“继续 native move 分支”，就不要把它当当前主线

注意：
- 当前移动协议已经收敛为显式 window.move(dx, dy)
- move.intent 只保留 legacy 兼容，不再作为主方向
- 不要把 DisplayMove 和桥接显式位移绑在同一次移动里
- 不要把 display-control-surface-and-full-control-plan.md 误当成“当前已经实现的正式协议”
- protocol-phase1.md 才是当前已正式承诺的最小边界
- 如果修改插件后要重编，先停掉 VPet，否则 DLL 会被锁住
- 不要替我跑真实联调；如果要补测试，只更新 quick-tests.json，真实结果由我自己回写
- phase 2 仍保持冻结：graph.catalog / graph.play / behavior.invoke

你接下来直接做：
1. 不要重新做大范围方案分析
2. 不要替我跑真实测试
3. 当前先继续 phase 1，不要提前进入 phase 2
4. native move 分支当前视为 paused，除非我明确要求，否则不要继续修
5. 当前主线以 phase 1 正式协议与稳定基线为准
6. 当前优先让我自己在 `/dev/quick-test` 回写：
   - emotion-thinking
   - emotion-pinch
   - emotion-shy-legacy
7. 回写后再判断 phase 1 的 `emotion -> graph` 这一小块是否可视为已收口
8. 每轮结束同步 `.devflow/.../state.md` 和 `.devflow/.../checkpoints.md`；如果有方向性决策，更新 `.devflow/.../decision-log.md`
```

更短的版本：

```text
继续 VPet 身体层桥接工作。使用 $devflow。先读 .devflow/desktop-pet-vpet-body-bridge 下的 state / workflow / decision-log / checkpoints / 最新 handoff / protocol-phase1 / display-control-surface-and-full-control-plan / quick-tests。旧 .explore 只作 legacy；native move 分支当前已暂停，不要默认继续；当前主线回到 phase 1 正式协议与稳定基线，不要替我跑真实测试，也不要提前进入 phase 2。
```
