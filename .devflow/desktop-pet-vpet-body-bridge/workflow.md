# 任务工作流

## 任务目标
- 将 VPet 改造成桌宠项目中的身体层 / 前端执行层，通过桥接插件接收 Python backend-agent 的高层事件。

## 范围边界
- 范围内：
  - 维护 VPet 身体层桥接能力
  - 动作 / 表情 / 气泡 / mode 事件联调
  - 插件化收敛
  - `window.move` 与最小状态回传
- 范围外：
  - 深层 `GameCore` 重构
  - 存档体系重写
  - 将记忆系统直接塞入 VPet 内部
  - 回退到 Electron 前端主线

## 成功标准
- VPet 可稳定作为外部大脑驱动的身体层
- 事件桥以 `MainPlugin` 形式独立存在
- 常用动作 / 表情 / 说话编排已完成真实联调
- 补齐 `window.move` 与最小状态回传，形成更完整闭环

## 阶段规划
1. 架构冻结与桥接 POC
2. 真实联调与动作 / 表情映射修正
3. 插件化收敛
4. 补 `window.move` 与最小状态回传
5. 身体层长期维护与论文材料沉淀

## 当前阶段
- 阶段 3：phase 1 正式协议维护；mission 真相源已从 `.explore` 迁移到 `.devflow`
- 当前路径：resume / light migration close

## 退出条件
- `window.move` 可用
- 最小状态回传可用
- `.devflow/desktop-pet-vpet-body-bridge/` 可独立作为后续续接真相源

## 当前记录约定
- 新一轮开发、checkpoint、handoff、quick test 回写默认写入 `.devflow/desktop-pet-vpet-body-bridge/`
- 旧 `.explore/desktop-pet-vpet-body-bridge/` 只作为 legacy 参考，不再作为当前 mission 写入目标
