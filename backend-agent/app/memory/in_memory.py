from collections import deque

from ..schemas.memory import MemoryRecallItem, MemoryRecord
from .base import MemoryStore


class InMemoryStore(MemoryStore):
    def __init__(self, max_items: int = 50) -> None:
        self._records: deque[MemoryRecord] = deque(maxlen=max_items)

    async def write(self, record: MemoryRecord) -> None:
        self._records.append(record)

    async def recall(self, query: str, limit: int = 3) -> list[MemoryRecallItem]:
        normalized_query = query.strip()
        if not normalized_query:
            return []

        matched_records: list[MemoryRecallItem] = []
        for record in reversed(self._records):
            if normalized_query in record.content:
                matched_records.append(
                    MemoryRecallItem(
                        content=record.content,
                        category=record.category,
                    ),
                )

            if len(matched_records) >= limit:
                break

        return matched_records
