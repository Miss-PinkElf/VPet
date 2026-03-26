# 交接文档

## 当前目标
把当前 VPet 仓库推进成“桌宠身体层 + 外部 Python 大脑”的验证仓库，并以最小桥接 POC 为下一步实现目标。

## 当前进度
- 已完成架构方向冻结。
- 已确认低耦合代码挂点。
- 已新增详细实施指南：`docs/agent-desktop-pet/migration/2026-03-27-vpet-body-bridge-implementation-guide.md`。
- 已建立全局和专项的 explore 记录目录。

## 关键文件/产物
- `docs/agent-desktop-pet/migration/2026-03-27-vpet-body-bridge-implementation-guide.md`
- `.codex/explore/desktop-pet-graduation-roadmap/*`
- `.codex/explore/desktop-pet-vpet-body-bridge/*`

## 已做的决策（摘要）
- VPet 固定为身体层，不作为完整业务底座。
- 长期桥接方案优先使用 `MainPlugin`。
- 第一阶段只做窄事件协议。
- 第一阶段不碰深层存档和 GameCore 解耦。

## 立即要做的下一步
1. 在仓库内实现最小桥接 POC。
2. 第一版只打通 `bubble.show`、`motion.play(idle)`、`motion.play(move)`。
3. 完成后再考虑插件化收敛。

## 恢复指引
1. 先读本文件。
2. 再读 `state.md` 了解当前阶段和下一步。
3. 再读 `learnings.md`，避免重复讨论已经确认的边界。
4. 最后按 migration 实施指南继续实现。
