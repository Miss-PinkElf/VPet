import asyncio
import json

from ..schemas.events import PetEvent


class EventBus:
    def __init__(self) -> None:
        self._subscribers: set[asyncio.Queue[PetEvent]] = set()

    def subscribe(self) -> asyncio.Queue[PetEvent]:
        queue: asyncio.Queue[PetEvent] = asyncio.Queue()
        self._subscribers.add(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue[PetEvent]) -> None:
        self._subscribers.discard(queue)

    async def publish(self, event: PetEvent) -> None:
        for queue in list(self._subscribers):
            await queue.put(event)

    @staticmethod
    def format_sse(event: PetEvent) -> str:
        return f'data: {json.dumps(event.model_dump(), ensure_ascii=False)}\n\n'
