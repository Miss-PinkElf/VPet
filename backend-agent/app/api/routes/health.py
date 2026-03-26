from fastapi import APIRouter, Depends

from ...schemas.chat import HealthResponse
from ..dependencies import get_services
from ...services.app_services import AppServices

router = APIRouter()


@router.get('/health', response_model=HealthResponse)
async def health_check(services: AppServices = Depends(get_services)) -> HealthResponse:
    return HealthResponse(
        status='ok',
        model=services.settings.llm_model,
        upstream_configured=bool(services.settings.llm_api_key),
    )
