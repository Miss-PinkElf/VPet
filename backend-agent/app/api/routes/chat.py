from fastapi import APIRouter, Depends

from ...schemas.chat import ChatRequest, ChatResponse
from ...services.app_services import AppServices
from ..dependencies import get_services

router = APIRouter()


@router.post('/api/chat', response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    services: AppServices = Depends(get_services),
) -> ChatResponse:
    return await services.chat_orchestrator.chat(chat_request)
