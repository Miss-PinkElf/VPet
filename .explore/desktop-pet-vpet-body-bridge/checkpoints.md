# Checkpoints

> [已归档] 2026-03-27 - Mission Migration
> [已归档] 2026-03-27 - Window Move + State Loop
> [已归档] 2026-03-27 - Combo Validation + State Expansion
> [已归档] 2026-03-27 - Sequence / Scenario Entry
> [已归档] 2026-03-27 - Context Save
> [已归档] 2026-03-27 - Standard 18787 Startup Fix + Long Sequence
> [已归档] 2026-03-28 - Sleep Handoff
> [已归档] 2026-03-28 - Timeline Observability + Legacy UI Demotion
> [已归档] 2026-03-30 - Display Control Surface Analysis
> [已归档] 2026-03-28 - Quick Test JSON Catalog Page
> [已归档] 2026-03-28 - Quick Test File-Backed Catalog
> [已归档] 2026-03-28 - Current Phase Test Catalog
> [已归档] 2026-03-28 - Quick Test Result Writeback
> [已归档] 2026-03-28 - Move Instability Root Cause
> [已归档] 2026-03-28 - Sequence Delay Relaxation
> [已归档] 2026-03-28 - Smart Move Style
> [已归档] 2026-03-28 - Sequence Wait-For Gating
> [已归档] 2026-03-29 - Sleep Handoff After Sequence Gating
> [已归档] 2026-03-29 - Real Retest After Event-Applied + Move Tolerance Fix
> [已归档] 2026-03-29 - Event Correlation Fields + Longer Story Sequence
> [已归档] 2026-03-29 - Sleep Handoff After Event Correlation
> [已归档] 2026-03-31 - Focus Quick Test For Story Sequence
> [已归档] 2026-03-31 - Story Sequence Result Triage
> [已归档] 2026-03-31 - Motion Complete Stabilization
> [已归档] 2026-03-31 - Motion Recovered Gate
> [已归档] 2026-03-31 - Tail-Step Relaxation For Story Sequence

## Checkpoint 26 - 2026-03-31 Smart Move Easing Pass

### 当前阶段
- 阶段 3：继续 phase 1，不扩协议面，直接收口 `window.move(style=smart)` 的走路体感

### 本轮完成内容
- 重新核对插件 `window.move` 与原生 move system 的边界，确认：
  - `window.move` 当前只走 `MoveWindows(...)`
  - 原生走路仍是 `DisplayMove() -> A_Start/B_Loop/C_End + MoveTimer`
- 在 `VPet.Plugin.AgentBridge/AgentBridgePoller.cs` 中将 `smart` 平滑位移从：
  - 固定步数 + 固定 45ms 间隔的线性切片
  改为：
  - 距离感知总时长
  - eased 累进位移
  - 按欧氏距离计算的步数
- 本轮没有把 `DisplayMove()` 或原生 `walk/crawl/fall/climb` move graph 重新绑回 `window.move`
- 将 `quick-tests.json` 的当前 focus test 切到：
  - `move-smart-medium-right-80`
- 完成代码级验证：
  - `dotnet build 'VPet.Plugin.AgentBridge/VPet.Plugin.AgentBridge.csproj' -c Debug` 通过
  - `quick-tests.json` 通过 JSON 解析校验

### 本轮决策与原因
- 决策：phase 1 的 `smart move` 继续保持纯显式位移，只优化曲线和节奏
- 原因：当前体验缺口来自“线性拖窗感”，不是协议边界错误；现在回退去混入原生 move system 只会破坏已经收口的分层

### 本轮沉淀经验
- `MoveWindows(...)` 本身只做窗口位移；如果上层再用固定步数和固定间隔去切片，就很容易产生机械滑块感
- 原生走路 graph 确实是独立系统，但这不意味着 phase 1 的体感问题要通过把它重新绑回 `window.move` 来解决
- 先把纯位移曲线做顺，再决定是否需要一个正式分开的 native walk 能力，风险最低

### 待解决问题
- 新 eased `smart move` 在真实 GUI 下是否已经明显减轻“机械滑块感”
- 如果仍不够自然，是否需要单独设计一个和 `window.move(dx, dy)` 分离的原生 walk 能力
- `move.intent` 的运行时薄兼容何时退到纯文档兼容

### 下一步
- 由你在 `/dev/quick-test` 点击：
  - `move-smart-medium-right-80`
- 将新的真实体感结果回写到 `quick-tests.json`
- 我再根据你的反馈决定：
  - 继续微调 pure move 曲线
  - 或单独探索与 `window.move` 分层的原生 walk 能力

### 可以从活跃上下文中移除的内容
- “6 步 story sequence 仍是当前优先测试焦点” 这件事
- “smart move 现在仍只是固定节奏线性切片” 这件事

### 追加真实反馈
- 你对这轮 eased `smart move` 的最新真实反馈是：
  - “其实还是单纯的移动，机械滑块感，没有调用任何动作”

### 反馈解释
- 这说明当前问题已经不是“线性切片是否够顺”
- 而是 `window.move` 这条 pure move 路径根本不带动作层
- 因此下一步不该继续死抠 pure move 曲线，而应转向：
  - 与 `window.move(dx, dy)` 正式语义分开的原生 walk 能力探索

### 追加收口
- 当前最窄的原生 walk 探索入口已确认存在：
  - `motion.play(move)` -> `DisplayMove()`
- 因此下一步不需要先扩新协议字面量
- 先由现有入口验证：
  - 原生 move system 是否值得单独暴露为后续 dev-only 能力

### 新的真实结果
- `motion-native-move` 已得到你的真实反馈：
  - 会触发原生移动系统
  - 可能是爬行，也可能是走路
  - 到屏幕边缘会贴墙爬
  - 还可能出现斜着飞行

### 结果解释
- 这说明 `motion.play(move)` 已经足以证明：
  - 原生 move system 独立存在
  - 它与 `window.move` 的纯位移路径明显不同
- 同时也说明当前这条入口仍然是环境驱动的：
  - 它不是稳定的“固定向左走”或“固定向右走”
  - 而是会按当前触发条件在 `walk/crawl/climb/fall` 之间切换
- 因此下一步不该继续做更多真实点击，而应先在源码里缩圈：
  - 原生 move graph 的选择规则
  - 是否存在可约束方向/类型的最小切入点

### 缩圈结论
- `DisplayMove()` 的真实语义不是“播放 move 动画”，而是：
  - 在 `GraphConfig.Moves` 里随机起点遍历
  - 找到第一个 `Triggered(main)` 为真的 move
  - 然后执行 `move.Display(main)`
- 原生控制台已存在一个更窄的调试入口：
  - 左：`SpeedX < 0 && Checked(...)`
  - 右：`SpeedX > 0 && Checked(...)`
  - 上：`SpeedY < 0 && Checked(...)`
  - 下：`SpeedY > 0 && Checked(...)`
- 这说明后续如果要做最小 dev-only 原生 move 控制，不需要重造整套系统：
  - 最小版可以直接做方向入口
  - 更强控制版可以再做按 `Graph` 名精确选 move

### 本轮实现收口
- 已按缩圈结论落地第一版 dev-only 原生 move 入口：
  - `native.move.direction(left|right|up|down)`
- 当前实现直接复用原生控制台逻辑：
  - `left` 选 `SpeedX < 0 && Checked(...)`
  - `right` 选 `SpeedX > 0 && Checked(...)`
  - `up` 选 `SpeedY < 0 && Checked(...)`
  - `down` 选 `SpeedY > 0 && Checked(...)`
- 已同步更新：
  - backend schema / behavior policy
  - plugin event consume
  - `/dev/control`
  - `quick-tests.json`

### 下一步
- 由你优先测试：
  - `native-move-right`
- 再依次测试：
  - `native-move-left`
  - `native-move-up`
  - `native-move-down`
- 回写时重点区分两类现象：
  - 中间位置方向是否稳定
  - 靠边时切到 climb/fall 是否还能解释

### 新的真实结果
- 四条 `native.move.direction` 都已得到真实结果：
  - `left`
    - 会先冲到顶部，再贴顶向左爬
  - `right`
    - 会先冲到顶部，再贴顶向右爬
  - `up`
    - 会先冲到左边，再贴左向上爬
  - `down`
    - 会先冲到左边，再贴左向下爬

### 结果解释
- 这说明当前第一版 direction 入口虽然已经不随机乱挑正负方向，但筛选仍过宽：
  - 它允许带 `LocateType` 的贴边 move 提前入选
- 结合源码，直接根因是：
  - 当前实现只看 `SpeedX / SpeedY + Checked(...)`
  - 但 `move.Display(main)` 在 `LocateType` 存在时会先 reposition 到对应边缘
- 因此这轮失败不代表 direction 路线错误，而是代表：
  - 下一轮必须把 move 选择优先级收紧

## Checkpoint 27 - 2026-03-31 Native Move Direction Dev-Only Entry

### 当前阶段
- 阶段 3：继续 phase 1，不改正式 `window.move`，新增 dev-only 的原生方向移动入口

### 本轮完成内容
- 在 backend 事件 schema 中新增：
  - `native.move.direction`
- 在 `BehaviorPolicyEngine` 中接入手动构建：
  - `direction = left|right|up|down`
- 在插件中新增消费逻辑：
  - 按 `SpeedX / SpeedY` 方向筛选 `GraphConfig.Moves`
  - 通过 `Checked(...)` 过滤当前环境可触发项
  - 调用 `move.Display(main)` 进入原生 move system
- `/dev/control` 已新增：
  - `native.move.direction` 事件类型
  - `direction` 下拉选择
- `quick-tests.json` 已新增 4 条方向测试：
  - `native-move-left`
  - `native-move-right`
  - `native-move-up`
  - `native-move-down`
  - 并将当前 focus 切到 `native-move-right`

### 本轮决策与原因
- 决策：先落地方向约束，不先做 graph 名精确控制
- 原因：方向层已经足够验证“随机原生 move system 能否被收口到更可控的入口”，同时改动最小

### 本轮沉淀经验
- `motion.play(move)` 只能证明原生 move system 存在，不能证明它可控
- 要让这套系统更可测，最小的新增不是再调 `DisplayMove()`，而是直接绕过它的随机挑选逻辑
- 原生控制台本身就是最佳参考实现，复用其方向筛选逻辑比另起一套猜测策略稳得多

### 验证情况
- `python -m compileall backend-agent/app` 通过
- `quick-tests.json` 通过 JSON 解析校验
- 插件完整 `dotnet build` 未能完成落 DLL：
  - 原因是 `mod/1200_AgentBridge/plugin/VPet.Plugin.AgentBridge.dll` 被运行中的 VPet 锁住
  - 这不构成源码层面的新问题，但意味着真实联调前必须先停掉 VPet

### 下一步
- 由你先停掉 VPet，完成插件重新 build / 启动桥接
- 然后按顺序测试：
  - `native-move-right`
  - `native-move-left`
  - `native-move-up`
  - `native-move-down`
- 每条至少回写：
  - 中间位置表现
  - 靠边位置表现

### 可以从活跃上下文中移除的内容
- “native.move.direction 还只是探索想法” 这件事
- “下一步还没决定测哪几条原生方向测试” 这件事

## Checkpoint 28 - 2026-03-31 Native Move Paused And Return To Mainline

### 当前阶段
- 阶段 3：native move 分支已完成记录并暂停，当前主线切回 phase 1 正式协议

### 本轮完成内容
- 确认 native move 分支的暂停状态已经完整记录到：
  - `state.md`
  - `decision-log.md`
  - `checkpoints.md`
  - `handoffs/2026-03-31-016-native-move-direction-paused.md`
- 将 `handoffs/index.md` 的最新入口切到：
  - `2026-03-31-016-native-move-direction-paused.md`
- 将 `quick-tests.json` 的当前 focus 从 native 分支切回：
  - `sequence-think-speak-move-touch-speak-recover`

### 本轮决策与原因
- 决策：当前不继续 native move 分支，而是把它作为已记录的 paused 旁支保存
- 原因：这条分支已经有足够清晰的恢复点，当前不再是主线目标

### 本轮沉淀经验
- 当一个探索分支已经拿到：
  - 实现
  - 真实测试
  - 根因
  - 明确下一步
  就应该及时冻结为 paused 分支，而不是继续把它挂在主线焦点上

### 下一步
- 当前不需要额外“切换”操作
- 后续只要继续按 phase 1 主线选择新的明确子任务即可
- 如果未来要重开 native move：
  - 直接从 `2026-03-31-016-native-move-direction-paused.md` 恢复

### 可以从活跃上下文中移除的内容
- “当前主线仍然是 native move direction” 这件事
- “还需要继续点 native-move-left/right/up/down” 这件事

