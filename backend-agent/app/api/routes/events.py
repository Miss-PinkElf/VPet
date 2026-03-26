import asyncio

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from ...services.app_services import AppServices
from ..dependencies import get_services

router = APIRouter()


@router.get('/api/events')
async def stream_events(services: AppServices = Depends(get_services)) -> StreamingResponse:
    event_queue = services.event_bus.subscribe()

    async def event_generator():
        try:
            while True:
                event = await event_queue.get()
                yield services.event_bus.format_sse(event)
        except asyncio.CancelledError:
            raise
        finally:
            services.event_bus.unsubscribe(event_queue)

    return StreamingResponse(
        event_generator(),
        media_type='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        },
    )
