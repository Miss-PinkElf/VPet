import asyncio

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse, StreamingResponse

from ...schemas.events import VPetStateResponse, VPetStateSnapshot
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


@router.get('/vpet/events/next')
async def poll_next_event(services: AppServices = Depends(get_services)) -> Response:
    event = await services.event_bus.poll_next()
    if event is None:
        return Response(status_code=204)

    return JSONResponse(content=event.model_dump())


@router.post('/vpet/state', response_model=VPetStateResponse)
async def update_vpet_state(
    snapshot: VPetStateSnapshot,
    services: AppServices = Depends(get_services),
) -> VPetStateResponse:
    state = services.vpet_state_store.update(snapshot)
    return VPetStateResponse(status='ok', state=state)


@router.get('/api/dev/state', response_model=VPetStateResponse)
async def get_vpet_state(services: AppServices = Depends(get_services)) -> VPetStateResponse:
    return VPetStateResponse(status='ok', state=services.vpet_state_store.get_latest())
