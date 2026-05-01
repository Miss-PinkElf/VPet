# 下一次对话提示词：desktop-pet-vpet-body-bridge

把下面整段复制到新对话即可：

```text
继续 VPet 身体层桥接工作。使用 $devflow，并把 `.devflow/desktop-pet-vpet-body-bridge/` 作为当前 mission 真相源。先走 devflow resume 路径，不要重新大范围方案分析。

优先读取：
1. `.devflow/desktop-pet-vpet-body-bridge/state.md`
2. `.devflow/desktop-pet-vpet-body-bridge/checkpoints.md`
3. `.devflow/desktop-pet-vpet-body-bridge/handoffs/index.md`
4. `.devflow/desktop-pet-vpet-body-bridge/handoffs/2026-05-01-019-session-close-after-devflow-migration.md`
5. `.devflow/desktop-pet-vpet-body-bridge/spec/protocol-phase1.md`
6. `.devflow/desktop-pet-vpet-body-bridge/spec/display-control-surface-and-full-control-plan.md`
7. `.devflow/desktop-pet-vpet-body-bridge/quick-tests.json`

当前进度：
- VPet bridge mission 已从 `context-budget-explore` / `.explore` 迁移到 `devflow` / `.devflow`
- 迁移相关文档与必要路径改动已提交：
  - `3a53f16a docs: 迁移 VPet bridge mission 到 devflow`
- `/dev/quick-test` 已改为读写 `.devflow/desktop-pet-vpet-body-bridge/quick-tests.json`
- phase 1 最小协议与关键 wait_for 门控已稳定
- 6 步 story sequence 已通过到可接受范围
- native move 分支当前 paused，不要默认继续
- phase 2 继续冻结，不要提前进入 `graph.catalog / graph.play / behavior.invoke`

未完成任务：
- 让我自己在 `/dev/quick-test` 回写：
  - `emotion-thinking`
  - `emotion-pinch`
  - `emotion-shy-legacy`
- 回写后判断 phase 1 的 `emotion -> graph` 是否可以视为收口

注意事项：
- 旧 `.explore/desktop-pet-vpet-body-bridge/` 只作为 legacy 参考；新记录、新 checkpoint、新 handoff、quick test 结果都写 `.devflow/desktop-pet-vpet-body-bridge/`
- `protocol-phase1.md` 是当前正式协议边界
- `display-control-surface-and-full-control-plan.md` 是 phase 2 预研，不是已实现协议
- 不要替我跑真实 VPet GUI 联调
- 如果要修改插件并重编，先确认 VPet 未运行，否则 DLL 可能被锁住
- 恢复后先看 `git status`，当前对话收尾前工作树里还有未跟踪文件不属于本次 devflow migration 提交

建议下次优先处理：
1. 等我回写三条 emotion quick test 真实结果
2. 根据结果更新 `.devflow/.../quick-tests.json`、`state.md`、`checkpoints.md`
3. 如果三条稳定，再把 phase 1 emotion alias 收口从开放项移到完成项
```

