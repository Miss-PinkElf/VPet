# 明日续接提示词

把下面整段直接复制到新对话里即可：

```text
继续 VPet 身体层桥接工作。

先读取并遵循以下文件，然后直接开始做第一阶段最小桥接 POC，不要停留在纯分析：

1. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.codex\explore\desktop-pet-graduation-roadmap\handoff.md
2. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.codex\explore\desktop-pet-graduation-roadmap\state.md
3. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\.codex\explore\desktop-pet-vpet-body-bridge\handoff.md
4. D:\Users\Mobius\Desktop\mine\AAA-code\VPet\docs\agent-desktop-pet\migration\2026-03-27-vpet-body-bridge-implementation-guide.md

目标固定为：
- 把 VPet 当成身体层 / 前端执行层
- 把 Python backend-agent 当成大脑
- 第一阶段不要重构深层 GameCore

这轮直接进入实现，优先做第一阶段最小桥接 POC，只实现下面 3 个能力：
- `bubble.show`
- `motion.play(idle)`
- `motion.play(move)`

实现要求：
- 先阅读仓库现有挂点，再直接改代码
- 优先复用现有入口，例如 `RunAction(...)`、`Main.Say(...)`、`MoveWindows(...)`
- 不要先做完整总线，不要先做深度解耦
- 先完成最小可运行链路，再考虑插件化收敛

完成后请输出：
1. 改了什么
2. 改了哪些文件
3. 我本地要执行的验证命令
4. 还剩下哪些下一步
```

如果明天你只想发一句更短的，也可以用这个：

```text
继续 VPet 身体层桥接工作，先读根目录 CONTINUE_VPET_BRIDGE_PROMPT.md 里引用的 handoff 和实施指南，然后直接开始第一阶段 POC。
```
