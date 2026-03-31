# Example：复杂改动

## 用户请求

“做一个新的 dashboard 区块，带筛选、异步加载、空状态处理，还要比较两种交互设计，我现在还不确定哪种更好。”

## 预期路径

标准路径：

```txt
Classify -> Align -> Propose -> Apply -> Review -> Verify -> Archive
```

## Align 产出

- 澄清目标用户与关键操作
- 至少比较两种布局或交互方案
- 确认 loading、empty、error 的预期

## Artifact 形态

- `proposal.md`：范围、非目标、边界场景、上线风险
- `design.md`：页面结构、数据流、筛选模型、API 假设
- `tasks.md`：脚手架、数据层、UI 状态、交互、review、验证
