from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import chat, dev_control, events, health
from .core.config import get_settings
from .services.app_services import create_app_services


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title='Desktop Pet Backend', version='0.2.0')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.state.services = create_app_services(settings)

    app.include_router(health.router)
    app.include_router(chat.router)
    app.include_router(events.router)
    app.include_router(dev_control.router)
    return app


app = create_app()
