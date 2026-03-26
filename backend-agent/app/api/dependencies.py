from fastapi import Request

from ..services.app_services import AppServices


def get_services(request: Request) -> AppServices:
    return request.app.state.services
