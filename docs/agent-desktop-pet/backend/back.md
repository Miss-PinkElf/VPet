后端的 llm 模型配置

- `PET_LLM_BASE_URL=https://codex.hiyo.top/`
- `PET_LLM_API_KEY`：通过环境变量注入，不要写进代码、文档或提交到 git
- 接口协议：标准 OpenAI 兼容格式 `/v1/chat/completions`
- 默认模型优先：`gpt-5.4`，其次 `gpt-5.2`

推荐放在本地 `backend/.env`：

```env
PET_LLM_BASE_URL=https://codex.hiyo.top/
PET_LLM_MODEL=gpt-5.4
PET_LLM_API_KEY=your-local-secret
```
