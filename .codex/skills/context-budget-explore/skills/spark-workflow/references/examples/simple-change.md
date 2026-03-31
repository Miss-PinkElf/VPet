# Example：简单改动

## 用户请求

“把现有支付表单的提交按钮状态和辅助文案调整一下，页面其他部分保持不变。”

## 预期路径

轻量路径：

```txt
Classify -> Mini Align -> Propose -> Apply -> Verify
```

## Align 产出

- 确认按钮在什么条件下禁用
- 确认新的文案内容
- 确认 loading 与 error 文案是否也要改

## Artifact 形态

- `proposal.md`：聚焦单个已有页面、明确 UX 小改动、列出受影响状态
- `design.md`：说明按钮状态逻辑和辅助文案渲染路径
- `tasks.md`：拆分文案调整、交互逻辑调整、验证
