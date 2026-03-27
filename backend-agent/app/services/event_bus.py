import asyncio
import json

from ..schemas.events import PetEvent


class EventBus:
    def __init__(self) -> None:
        self._subscribers: set[asyncio.Queue[PetEvent]] = set()
        self._poll_queue: asyncio.Queue[PetEvent] = asyncio.Queue()

    def subscribe(self) -> asyncio.Queue[PetEvent]:
        queue: asyncio.Queue[PetEvent] = asyncio.Queue()
        self._subscribers.add(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue[PetEvent]) -> None:
        self._subscribers.discard(queue)

    async def publish(self, event: PetEvent) -> None:
        await self._poll_queue.put(event)
        for queue in list(self._subscribers):
            await queue.put(event)

    async def poll_next(self) -> PetEvent | None:
        try:
            return self._poll_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None

    @staticmethod
    def format_sse(event: PetEvent) -> str:
        return f'data: {json.dumps(event.model_dump(), ensure_ascii=False)}\n\n'
