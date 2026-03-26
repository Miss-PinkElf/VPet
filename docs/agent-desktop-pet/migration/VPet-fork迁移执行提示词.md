# VPet Fork 迁移执行提示词

这份文档的目的，是给 fork 后的 `VPet` 仓库里的 Codex 直接执行。

使用方式：

1. 打开你 fork 后的 `VPet` 仓库
2. 切到你刚建好的分支
3. 把下面“完整提示词”整段复制给 Codex
4. 根据你本机实际路径，只改 `SOURCE_REPO` 和 `TARGET_REPO`

---

## 完整提示词

你现在在我 fork 后的 `VPet` 仓库里工作。请不要直接重构业务逻辑，先帮我完成“迁移当前桌宠项目资料到 fork 仓库”的工作。

### 任务目标

把我旧仓库中的一部分文档、后端代码和 agent 配置迁移到当前这个 fork 的 `VPet` 仓库中，为后续“VPet 身体层 + Python 大脑”的重构验证做准备。

### 总原则

1. 不要破坏 `VPet` 原有核心工程结构。
2. 不要删除 `VPet` 关键代码，除非我明确要求。
3. 这一步主要做“迁移和整理”，不是直接重写 `VPet`。
4. 迁移完成后，要给我一个明确的变更总结，说明复制了什么、放到了哪里、哪些没有复制。
5. 如果发现源路径或目标路径不存在，先停下来报告。
6. 复制配置文件时要谨慎，尤其是 `.gitignore`，优先合并，不要盲目覆盖。

### 当前背景

这个 fork 仓库的目标不是继续原始 `VPet` 路线，而是做一个新的验证方向：

- 保留 `VPet` 的强桌宠感、窗口行为和帧动画体系
- 把外部 Python 后端接进来
- 后续通过事件桥把 Python 行为事件映射到 `VPet` 的动作状态

当前阶段先不要深挖 `GameCore` 等内部逻辑，先把资料、后端和工作流迁过来。

### 源仓库路径

请先使用下面这个源仓库路径，如果路径不存在，再停下来问我：

`SOURCE_REPO = E:\Learn\Vs\Code\agent-desktop-pet.worktrees\agent-desktop-pet-expore`

### 目标仓库路径

当前工作目录就是目标仓库，如果你需要记录，可以记为：

`TARGET_REPO = 当前仓库根目录`

### 需要先做的事

先按顺序完成以下动作：

1. 检查当前仓库根目录结构。
2. 检查 `SOURCE_REPO` 是否存在。
3. 检查下面列出的源文件和目录是否存在。
4. 如果都存在，再开始创建目标目录并复制内容。

### 目标目录结构

请在当前 fork 仓库中创建下面这些目录，如果已存在就不要重复创建：

```text
docs/agent-desktop-pet/research
docs/agent-desktop-pet/backend
docs/agent-desktop-pet/requirements
docs/agent-desktop-pet/migration
backend-agent
```

### 必须复制的内容

请复制下面这些内容：

1. 目录：
   - `SOURCE_REPO\backend` -> `TARGET_REPO\backend-agent`

2. 文档：
   - `SOURCE_REPO\zzz-doc\桌宠技术路线探索总结.md` -> `TARGET_REPO\docs\agent-desktop-pet\research\桌宠技术路线探索总结.md`
   - `SOURCE_REPO\zzz-doc\back.md` -> `TARGET_REPO\docs\agent-desktop-pet\backend\back.md`
   - `SOURCE_REPO\zzz-doc\记忆相关.md` -> `TARGET_REPO\docs\agent-desktop-pet\backend\记忆相关.md`
   - `SOURCE_REPO\zzz-doc\zzz-prompt-debug\plan\桌宠项目详细PRD.md` -> `TARGET_REPO\docs\agent-desktop-pet\requirements\桌宠项目详细PRD.md`
   - `SOURCE_REPO\zzz-doc\VPet-fork迁移执行提示词.md` -> `TARGET_REPO\docs\agent-desktop-pet\migration\VPet-fork迁移执行提示词.md`
   - `SOURCE_REPO\.claude\handoffs\2026-03-26-vpet-fork-execution-guide.md` -> `TARGET_REPO\docs\agent-desktop-pet\migration\2026-03-26-vpet-fork-execution-guide.md`

3. OpenSpec 路线文档：
   - `SOURCE_REPO\openspec\changes\desktop-pet-companion-roadmap\proposal.md` -> `TARGET_REPO\docs\agent-desktop-pet\requirements\desktop-pet-companion-roadmap-proposal.md`
   - `SOURCE_REPO\openspec\changes\desktop-pet-companion-roadmap\design.md` -> `TARGET_REPO\docs\agent-desktop-pet\requirements\desktop-pet-companion-roadmap-design.md`
   - `SOURCE_REPO\openspec\changes\desktop-pet-companion-roadmap\tasks.md` -> `TARGET_REPO\docs\agent-desktop-pet\requirements\desktop-pet-companion-roadmap-tasks.md`

4. Agent 配置文件：
   - `SOURCE_REPO\.codex\AGENTS.md` -> `TARGET_REPO\.codex\AGENTS.md`
   - `SOURCE_REPO\.claude\CLAUDE.md` -> `TARGET_REPO\.claude\CLAUDE.md`

### 建议复制的内容

如果这些文件存在，也一起复制过去：

- `SOURCE_REPO\前端需求.md` -> `TARGET_REPO\docs\agent-desktop-pet\requirements\前端需求.md`
- `SOURCE_REPO\zzz-doc\桌宠项目交互控制设计稿.md` -> `TARGET_REPO\docs\agent-desktop-pet\requirements\桌宠项目交互控制设计稿.md`
- `SOURCE_REPO\zzz-doc\桌宠毕设过程记录指南.md` -> `TARGET_REPO\docs\agent-desktop-pet\migration\桌宠毕设过程记录指南.md`

### 配置文件处理要求

#### `.gitignore`

不要直接覆盖目标仓库现有 `.gitignore`。

请这样处理：

1. 读取 `SOURCE_REPO\.gitignore`
2. 读取 `TARGET_REPO\.gitignore`
3. 只把与本地缓存、Python、Node、agent 工作目录相关且目标仓库还没有的忽略规则追加进去
4. 在追加区域前加一个简短注释，例如：

```text
# Added for desktop-pet backend/docs migration
```

#### `.codex` 和 `.claude`

不要整目录复制。

只确保下面这些最小文件存在：

- `.codex\AGENTS.md`
- `.claude\CLAUDE.md`

如果目标仓库里已经存在同名文件：

- 先读取并比较
- 优先保留目标仓库已有内容
- 再把源仓库中有价值的补充内容合并进去
- 不要粗暴覆盖

### 明确不要复制的内容

不要复制下面这些：

- `SOURCE_REPO\frontend`
- `SOURCE_REPO\node_modules`
- `SOURCE_REPO\.electron-cache`
- `SOURCE_REPO\.pnpm-store`
- `SOURCE_REPO\electron-v40.4.1-win32-x64.zip`
- `SOURCE_REPO\.claude\settings.local.json`
- 任何本地缓存、依赖目录、构建产物、临时文件

### 执行方式要求

请按下面流程执行：

1. 先列出你准备复制的文件清单。
2. 检查源文件是否都存在。
3. 创建目标目录。
4. 复制必须复制的内容。
5. 再复制建议复制的内容。
6. 合并 `.gitignore`。
7. 最后输出总结。

### 最终输出要求

完成后请明确告诉我：

1. 复制了哪些目录和文件
2. 它们各自放到了哪里
3. 哪些建议项因为不存在而没有复制
4. `.gitignore` 合并了哪些规则
5. 当前 fork 仓库下一步最适合做什么

### 下一步建议

迁移完成后，不要直接开始大规模重构。请先建议我做下面这个最小 POC：

1. 保证 fork 后的 `VPet` 原工程能跑起来
2. 为 `VPet` 增加一个最小外部事件入口
3. 让外部事件能驱动几个动作状态切换，例如：
   - `idle`
   - `thinking`
   - `remind`
   - `dragged`

---

## 备注

如果你想更稳一点，也可以在把上面的完整提示词发给新仓库里的 Codex 之前，自己先手工替换这两个值：

- `SOURCE_REPO`
- `TARGET_REPO`

如果你懒得改，通常只保留 `SOURCE_REPO` 就够了，因为目标仓库就是 Codex 当前工作目录。

