from ..memory.base import MemoryStore
from ..schemas.memory import MemoryRecallItem, MemoryRecord


class MemoryService:
    def __init__(self, store: MemoryStore) -> None:
        self._store = store

    async def write_working_memory(self, content: str) -> None:
        await self._store.write(MemoryRecord(category='working', content=content))

    async def recall_for_chat(self, query: str, limit: int = 3) -> list[MemoryRecallItem]:
        return await self._store.recall(query=query, limit=limit)
