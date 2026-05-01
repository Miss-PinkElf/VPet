# DevFlow Migration Plan

- 改动文件：`.devflow/desktop-pet-vpet-body-bridge/*`、`CONTINUE_VPET_BRIDGE_PROMPT.md`、`backend-agent/app/api/routes/dev_control.py`
- 方案：保留旧 `.explore/desktop-pet-vpet-body-bridge/` 作为 legacy 记录，将完整 mission 复制到 `.devflow/desktop-pet-vpet-body-bridge/` 并把后续续接、quick test 回写和状态记录切到 devflow。
- 状态：已完成

