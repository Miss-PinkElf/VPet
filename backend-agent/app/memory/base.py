from abc import ABC, abstractmethod

from ..schemas.memory import MemoryRecallItem, MemoryRecord


class MemoryStore(ABC):
    @abstractmethod
    async def write(self, record: MemoryRecord) -> None:
        raise NotImplementedError

    @abstractmethod
    async def recall(self, query: str, limit: int = 3) -> list[MemoryRecallItem]:
        raise NotImplementedError
