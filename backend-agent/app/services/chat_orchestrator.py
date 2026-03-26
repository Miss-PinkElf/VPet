import asyncio

from ..core.config import Settings
from ..schemas.chat import ChatMessage, ChatRequest, ChatResponse
from ..schemas.memory import MemoryRecallItem
from .llm_service import LlmService
from .memory_service import MemoryService


class ChatOrchestrator:
    def __init__(
        self,
        settings: Settings,
        llm_service: LlmService,
        memory_service: MemoryService,
    ) -> None:
        self._settings = settings
        self._llm_service = llm_service
        self._memory_service = memory_service

    async def chat(self, chat_request: ChatRequest) -> ChatResponse:
        recalled_memories = await self._memory_service.recall_for_chat(chat_request.message)
        prompt_messages = self._build_prompt_messages(chat_request, recalled_memories)
        reply_text = await asyncio.to_thread(self._llm_service.complete_chat, prompt_messages)
        await self._memory_service.write_working_memory(chat_request.message.strip())
        await self._memory_service.write_working_memory(reply_text)
        return ChatResponse(
            reply=reply_text,
            model=self._llm_service.get_model_name(),
        )

    def _build_prompt_messages(
        self,
        chat_request: ChatRequest,
        recalled_memories: list[MemoryRecallItem],
    ) -> list[ChatMessage]:
        history_messages = [
            ChatMessage(role=message.role, content=message.content.strip())
            for message in chat_request.history[-self._settings.max_history_items:]
            if message.content.strip()
        ]

        memory_messages: list[ChatMessage] = []
        if recalled_memories:
            memory_summary = '\n'.join(f'- {item.content}' for item in recalled_memories)
            memory_messages.append(
                ChatMessage(
                    role='system',
                    content=f'这是当前可用的相关记忆，请仅在自然相关时参考：\n{memory_summary}',
                ),
            )

        return [
            ChatMessage(role='system', content=self._settings.system_prompt),
            *memory_messages,
            *history_messages,
            ChatMessage(role='user', content=chat_request.message.strip()),
        ]
