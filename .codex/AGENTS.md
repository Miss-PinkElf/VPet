### 基本要求
1. 必须使用简体中文
2. 每次完成之后，修改代码，之后需要询问我需不需要提交代码
3. 需要使用这个skills：context-budget-explore ，判断一下需要修改或者更新文档吗
4. 我来做测试，你给我测试quick test这个页面的测试json即可
5. 走context-budget-explore这个流程的时候，里面有superspec，记得头脑风暴一下，咱俩讨论一下
6. 创建plan的时候，在zzz-doc\zzz-prompt-debug\plan这个文件夹下，文件名和这次需求相关
7. 文档和写的plan都需要在 zzz-doc下面
8. 不需要全局进行es的校验，另外不影响运行的ts错误不需要管，修改ts错误需要向我确认
9. zzz-doc/桌宠前端开发问题修复清单.md，当你修复问题，或者记录问题的时候，记得把问题的原因，解决方案写进去，不断完善这个文档
10. 你产出superspec，或者handoff，或是openspec，创建skills时的文档，反正你产出文档的时候默认使用简体中文，禁止使用英文
11. commit的时候 提交的消息也使用中文
12. 使用context-budget-explore这个skills进行探索和记录
13. 记得使用superspec
14. 我的后端有虚拟环境在backend\.venv这个下面，不需要用全局的py
15. 每次完成之后，修改代码，之后需要询问我需不需要提交代码
16. 本仓库的文件必须使用相对路径
### 记录要求
- 对这个项目里长期进行的身体层桥接、架构、实现、续接类任务，默认优先使用 `context-budget-explore` skill，尤其是用户提到“继续上次”“边做边记录”“保存进度”“沉淀设计过程”“这是个长期任务”时。
- 续接任务时，优先读取：
  - `.explore/<mission>/state.md`
  - `.explore/<mission>/decision-log.md`
  - `.explore/<mission>/checkpoints.md`
  - `.explore/<mission>/handoffs/index.md`
  - 最新 handoff
- 如果 mission 真相文件已经存在，且用户是在“继续”，不要重新做大范围分析。
- 不要只改代码；对有实质推进的一轮，必须同步更新 `.explore` 记录。
- 最低记录要求：
  - 更新 `state.md`
  - 更新 `checkpoints.md`
  - 如果出现会影响后续判断的方向性决策，更新 `decision-log.md`
- `decision-log.md` 只记录决策，不记录普通进度流水账。
- 如果任务暂停，或上下文明显变重，需要创建或更新 handoff，并同步 `handoffs/index.md`。

