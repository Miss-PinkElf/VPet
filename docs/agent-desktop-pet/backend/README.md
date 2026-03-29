# 后端协议与联调文档目录

## 1. 这组文档是做什么的

这组文档服务于两类目标：

- 说明当前项目的后端、消息协议和联调工具到底已经做到什么程度
- 把其中可迁移的消息结构和联调思路抽出来，方便复用到别的“后端驱动前端”项目

建议阅读顺序：

1. 先看“后端能力与现状”
2. 再看“通用消息协议”
3. 最后看“联调页面设计”

## 2. 文档列表

### 2.1 后端能力与现状

文件：

- [后端消息协议与能力设计文档.md](D:\Users\Mobius\Desktop\mine\AAA-code\VPet\docs\agent-desktop-pet\backend\后端消息协议与能力设计文档.md)

主要内容：

- 当前后端能做什么
- 当前已经落地的消息类型有哪些
- 聊天、记忆、行为事件、sequence、状态回传分别怎么工作
- 基于当前协议，前端现在能做成什么样
- 当前限制和复用建议

适合什么时候看：

- 想快速了解当前系统状态
- 想知道“现在哪些东西是真的已经做了”
- 想区分设计目标和代码落地情况

### 2.2 通用消息协议

文件：

- [通用前后端消息数据结构协议.md](D:\Users\Mobius\Desktop\mine\AAA-code\VPet\docs\agent-desktop-pet\backend\通用前后端消息数据结构协议.md)

主要内容：

- 把当前项目里的消息结构抽成通用协议
- 聊天消息、记忆结构、行为事件、编排结构、状态回传结构的统一定义
- 每种结构的字段、用途、示例
- 这套协议可以迁移到什么类型的项目

适合什么时候看：

- 想把这套消息结构搬到另一个项目
- 想直接复用 event / state / sequence 结构
- 想做一个独立于 VPet 的通用前后端协议层

### 2.3 联调页面设计

文件：

- [联调页面设计说明.md](D:\Users\Mobius\Desktop\mine\AAA-code\VPet\docs\agent-desktop-pet\backend\联调页面设计说明.md)

主要内容：

- `/dev/control` 怎么设计
- `/dev/quick-test` 怎么设计
- 这两个页面分别解决什么问题
- 为什么需要同时保留“手工联调页”和“JSON 测试目录页”

适合什么时候看：

- 想复用当前联调工具思路
- 想给另一个项目也做一套协议调试页
- 想理解当前开发工作流为什么要拆成两个页面

## 3. 推荐复用方式

如果你后面要把这套东西搬到另一个项目，建议按下面顺序复用。

### 3.1 先复用消息体，不急着复用页面

优先复用：

- `ChatMessage / ChatRequest / ChatResponse`
- `MemoryRecord / MemoryRecallItem`
- `FrontendBehaviorEvent`
- `Sequence`
- `FrontendStateSnapshot`

原因：

- 真正跨项目稳定的是消息结构
- 页面只是调试工具，可以后补

### 3.2 再复用联调工作流

推荐保留两类工具：

- 一个完整联调页，对应 `/dev/control`
- 一个测试目录页，对应 `/dev/quick-test`

原因：

- 一个适合探索
- 一个适合沉淀和回归

### 3.3 最后再根据项目改命名

建议：

- 事件 `type` 尽量不改
- 类名 / 文件名 / 接口路径可以按项目调整

例如：

- `VPetStateSnapshot` 可以改成 `FrontendStateSnapshot`
- `PetEvent` 可以改成 `FrontendBehaviorEvent`

## 4. 一句话入口

如果你只想知道三件事，分别看这里：

- 当前后端到底能做什么：看 [后端消息协议与能力设计文档.md](D:\Users\Mobius\Desktop\mine\AAA-code\VPet\docs\agent-desktop-pet\backend\后端消息协议与能力设计文档.md)
- 消息数据结构怎么抽成通用协议：看 [通用前后端消息数据结构协议.md](D:\Users\Mobius\Desktop\mine\AAA-code\VPet\docs\agent-desktop-pet\backend\通用前后端消息数据结构协议.md)
- `/dev/control` 和 `/dev/quick-test` 为什么这样设计：看 [联调页面设计说明.md](D:\Users\Mobius\Desktop\mine\AAA-code\VPet\docs\agent-desktop-pet\backend\联调页面设计说明.md)
